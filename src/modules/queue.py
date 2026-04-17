"""
Queue System - Task 3.2
Phase 3: Batch Processing Engine

Progress tracking and queue management for batch processing.
"""

import time
import threading
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import json

from src.modules.pipeline import PipelineScheduler


class QueueStatus(Enum):
    """Status of a queue item."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class QueueItem:
    """A single item in the processing queue."""
    id: str
    input_path: str
    output_path: str
    status: QueueStatus = QueueStatus.PENDING
    progress: float = 0.0
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> Optional[float]:
        """Get processing duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "status": self.status.value,
            "progress": self.progress,
            "error": self.error,
            "duration": self.duration,
            "metadata": self.metadata,
        }


@dataclass
class QueueStats:
    """Statistics for the queue."""
    total: int = 0
    pending: int = 0
    processing: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0
    total_duration: float = 0.0

    @property
    def progress_percentage(self) -> float:
        """Get overall progress percentage."""
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "pending": self.pending,
            "processing": self.processing,
            "completed": self.completed,
            "failed": self.failed,
            "cancelled": self.cancelled,
            "progress_percentage": self.progress_percentage,
            "total_duration": self.total_duration,
        }


class ProgressCallback:
    """Callback interface for progress updates."""

    def on_start(self, item: QueueItem):
        """Called when processing starts."""
        pass

    def on_progress(self, item: QueueItem, progress: float):
        """Called with progress updates."""
        pass

    def on_complete(self, item: QueueItem):
        """Called when processing completes."""
        pass

    def on_error(self, item: QueueItem, error: str):
        """Called when processing fails."""
        pass

    def on_batch_complete(self, stats: QueueStats):
        """Called when batch processing completes."""
        pass


class ProcessingQueue:
    """
    Queue manager for batch image processing.

    Handles queue management, progress tracking, and threading.
    """

    def __init__(self, pipeline: Optional[PipelineScheduler] = None):
        self.pipeline = pipeline or PipelineScheduler()
        self.items: List[QueueItem] = []
        self.stats = QueueStats()
        self.callbacks: List[ProgressCallback] = []
        self._stop_requested = False
        self._processing = False
        self._lock = threading.Lock()

    def add_item(
        self,
        input_path: str,
        output_path: str,
        metadata: Optional[Dict] = None,
    ) -> QueueItem:
        """Add an item to the queue."""
        item = QueueItem(
            id=f"item_{len(self.items) + 1}",
            input_path=input_path,
            output_path=output_path,
            metadata=metadata or {},
        )

        with self._lock:
            self.items.append(item)
            self.stats.total += 1
            self.stats.pending += 1

        logger.info(f"Added to queue: {input_path}")
        return item

    def add_items(
        self,
        items: List[tuple[str, str]],
    ) -> List[QueueItem]:
        """Add multiple items to the queue."""
        queue_items = []
        for input_path, output_path in items:
            item = self.add_item(input_path, output_path)
            queue_items.append(item)
        return queue_items

    def add_from_directory(
        self,
        input_dir: str,
        output_dir: str,
        extensions: List[str] = None,
    ) -> List[QueueItem]:
        """Add all images from a directory."""
        if extensions is None:
            extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        items = []
        for ext in extensions:
            for img_path in input_path.glob(f"*{ext}"):
                out_path = output_path / img_path.name
                item = self.add_item(str(img_path), str(out_path))
                items.append(item)

        logger.info(f"Added {len(items)} images from directory")
        return items

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the queue."""
        with self._lock:
            for i, item in enumerate(self.items):
                if item.id == item_id:
                    if item.status == QueueStatus.PENDING:
                        self.items.pop(i)
                        self.stats.pending -= 1
                        self.stats.total -= 1
                        return True
        return False

    def clear_queue(self):
        """Clear all pending items."""
        with self._lock:
            self.items = [
                item for item in self.items
                if item.status not in [QueueStatus.PENDING, QueueStatus.PROCESSING]
            ]
            self._update_stats()

    def get_item(self, item_id: str) -> Optional[QueueItem]:
        """Get an item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def add_callback(self, callback: ProgressCallback):
        """Add a progress callback."""
        self.callbacks.append(callback)

    def remove_callback(self, callback: ProgressCallback):
        """Remove a progress callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _notify_start(self, item: QueueItem):
        """Notify callbacks of start."""
        for callback in self.callbacks:
            callback.on_start(item)

    def _notify_progress(self, item: QueueItem, progress: float):
        """Notify callbacks of progress."""
        for callback in self.callbacks:
            callback.on_progress(item, progress)

    def _notify_complete(self, item: QueueItem):
        """Notify callbacks of completion."""
        for callback in self.callbacks:
            callback.on_complete(item)

    def _notify_error(self, item: QueueItem, error: str):
        """Notify callbacks of error."""
        for callback in self.callbacks:
            callback.on_error(item, error)

    def _notify_batch_complete(self):
        """Notify callbacks of batch completion."""
        for callback in self.callbacks:
            callback.on_batch_complete(self.stats)

    def process_next(self) -> bool:
        """Process the next item in the queue."""
        with self._lock:
            item = None
            for i, queue_item in enumerate(self.items):
                if queue_item.status == QueueStatus.PENDING:
                    item = queue_item
                    item.status = QueueStatus.PROCESSING
                    item.start_time = time.time()
                    self.stats.pending -= 1
                    self.stats.processing += 1
                    break

        if item is None:
            return False

        self._notify_start(item)

        try:
            self._notify_progress(item, 0.1)

            image = self.pipeline.processor.load_image(item.input_path)
            self._notify_progress(item, 0.3)

            result = self.pipeline.execute(image)
            self._notify_progress(item, 0.8)

            if result.success:
                Path(item.output_path).parent.mkdir(parents=True, exist_ok=True)
                self.pipeline.processor.save_image(result.image, item.output_path)

                item.status = QueueStatus.COMPLETED
                item.result = result
                item.progress = 1.0

                with self._lock:
                    self.stats.processing -= 1
                    self.stats.completed += 1
                    if result.duration:
                        self.stats.total_duration += result.duration

                self._notify_progress(item, 1.0)
                self._notify_complete(item)
            else:
                raise ValueError(result.error)

        except Exception as e:
            item.status = QueueStatus.FAILED
            item.error = str(e)
            item.end_time = time.time()

            with self._lock:
                self.stats.processing -= 1
                self.stats.failed += 1

            self._notify_error(item, str(e))
            logger.error(f"Processing failed for {item.input_path}: {e}")

        finally:
            item.end_time = time.time()

        return True

    def process_all(self, stop_on_error: bool = False) -> QueueStats:
        """
        Process all items in the queue.

        Args:
            stop_on_error: Stop processing if an item fails

        Returns:
            QueueStats with final statistics
        """
        self._stop_requested = False
        self._processing = True

        while not self._stop_requested:
            with self._lock:
                has_pending = any(
                    item.status == QueueStatus.PENDING for item in self.items
                )

            if not has_pending:
                break

            success = self.process_next()
            if not success:
                break

            if stop_on_error:
                with self._lock:
                    has_failed = any(
                        item.status == QueueStatus.FAILED for item in self.items
                    )
                if has_failed:
                    self._stop_requested = True

        self._processing = False
        self._notify_batch_complete()

        return self.stats

    def process_threaded(self, num_workers: int = 2):
        """Process queue in separate threads."""
        def worker():
            while not self._stop_requested:
                with self._lock:
                    has_pending = any(
                        item.status == QueueStatus.PENDING for item in self.items
                    )
                if not has_pending:
                    break
                self.process_next()

        threads = []
        for _ in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self._processing = False
        self._notify_batch_complete()

    def stop(self):
        """Stop processing."""
        self._stop_requested = True

    def get_stats(self) -> QueueStats:
        """Get current statistics."""
        self._update_stats()
        return self.stats

    def _update_stats(self):
        """Update statistics from items."""
        self.stats.total = len(self.items)
        self.stats.pending = sum(1 for i in self.items if i.status == QueueStatus.PENDING)
        self.stats.processing = sum(1 for i in self.items if i.status == QueueStatus.PROCESSING)
        self.stats.completed = sum(1 for i in self.items if i.status == QueueStatus.COMPLETED)
        self.stats.failed = sum(1 for i in self.items if i.status == QueueStatus.FAILED)
        self.stats.cancelled = sum(1 for i in self.items if i.status == QueueStatus.CANCELLED)

    def to_json(self) -> str:
        """Export queue state to JSON."""
        return json.dumps(
            {
                "stats": self.stats.to_dict(),
                "items": [item.to_dict() for item in self.items],
            },
            indent=2,
        )

    def save_state(self, path: str):
        """Save queue state to file."""
        with open(path, "w") as f:
            f.write(self.to_json())
        logger.info(f"Queue state saved to {path}")

    def load_state(self, path: str):
        """Load queue state from file."""
        with open(path, "r") as f:
            data = json.loads(f.read())

        self.items = []
        for item_data in data.get("items", []):
            item = QueueItem(
                id=item_data["id"],
                input_path=item_data["input_path"],
                output_path=item_data["output_path"],
                status=QueueStatus(item_data["status"]),
                progress=item_data.get("progress", 0.0),
                error=item_data.get("error"),
                metadata=item_data.get("metadata", {}),
            )
            self.items.append(item)

        self._update_stats()
        logger.info(f"Queue state loaded from {path}")
