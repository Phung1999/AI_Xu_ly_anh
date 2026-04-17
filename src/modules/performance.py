"""
Performance Optimization Module - Task 5.1
Phase 5: Polish & Production

Profile and optimize the image processing pipeline.
"""

import time
import functools
from typing import Callable, Any, Optional
from loguru import logger
import numpy as np


class PerformanceMonitor:
    """Monitor performance metrics for image processing operations."""

    def __init__(self):
        self.metrics = {}
        self.call_counts = {}

    def record(self, name: str, duration: float):
        """Record a performance metric."""
        if name not in self.metrics:
            self.metrics[name] = []
            self.call_counts[name] = 0
        self.metrics[name].append(duration)
        self.call_counts[name] += 1

    def get_stats(self, name: str) -> dict:
        """Get statistics for a metric."""
        if name not in self.metrics:
            return {}

        durations = self.metrics[name]
        return {
            "count": self.call_counts[name],
            "total": sum(durations),
            "mean": sum(durations) / len(durations),
            "min": min(durations),
            "max": max(durations),
        }

    def get_all_stats(self) -> dict:
        """Get all statistics."""
        return {name: self.get_stats(name) for name in self.metrics}

    def print_report(self):
        """Print performance report."""
        logger.info("=" * 60)
        logger.info("PERFORMANCE REPORT")
        logger.info("=" * 60)

        for name, stats in self.get_all_stats().items():
            if stats:
                logger.info(
                    f"{name}: "
                    f"count={stats['count']}, "
                    f"total={stats['total']:.3f}s, "
                    f"avg={stats['mean']*1000:.2f}ms, "
                    f"min={stats['min']*1000:.2f}ms, "
                    f"max={stats['max']*1000:.2f}ms"
                )

        logger.info("=" * 60)


def profile(func: Callable) -> Callable:
    """Decorator to profile function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.debug(f"{func.__name__} took {duration*1000:.2f}ms")
        return result
    return wrapper


def cached(func: Callable) -> Callable:
    """Decorator to cache results for immutable inputs."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    wrapper.clear_cache = lambda: cache.clear()
    return wrapper


class ImageCache:
    """LRU cache for processed images."""

    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []

    def get(self, key: str) -> Optional[np.ndarray]:
        """Get cached image."""
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key].copy()
        return None

    def put(self, key: str, image: np.ndarray):
        """Put image in cache."""
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]

        self.cache[key] = image.copy()
        self.access_order.append(key)

    def clear(self):
        """Clear cache."""
        self.cache.clear()
        self.access_order.clear()

    def size(self) -> int:
        """Get cache size."""
        return len(self.cache)


class BatchOptimizer:
    """Optimize batch processing operations."""

    @staticmethod
    def estimate_processing_time(
        image_count: int,
        avg_time_per_image: float,
        num_workers: int = 1,
    ) -> float:
        """Estimate total processing time."""
        total_time = image_count * avg_time_per_image
        if num_workers > 1:
            total_time /= num_workers
        return total_time

    @staticmethod
    def optimal_tile_size(image_size: int, target_tiles: int = 16) -> int:
        """Calculate optimal tile size for processing."""
        import math
        return int(math.sqrt(image_size / target_tiles))

    @staticmethod
    def suggest_parallel_workers(cpu_count: int, image_count: int) -> int:
        """Suggest optimal number of parallel workers."""
        if image_count < 4:
            return 1
        return min(cpu_count, image_count // 2)
