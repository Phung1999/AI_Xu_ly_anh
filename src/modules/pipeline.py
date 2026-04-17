"""
Pipeline Scheduler - Task 3.1
Phase 3: Batch Processing Engine

Workflow engine for batch image processing.
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import json
import time

from src.modules.image_processor import ImageProcessor
from src.modules.levels import LevelsAdjustment
from src.modules.white_balance import WhiteBalance
from src.modules.sharpening import HighPassSharpening
from src.modules.clahe import CLAHEProcessor
from src.ai.enhancement import ImageEnhancer
from src.ai.auto_enhance import AutoEnhancer


class PipelineStepType(Enum):
    """Types of pipeline steps."""
    LOAD = "load"
    SAVE = "save"
    PROCESS = "process"
    ENHANCE = "enhance"
    TRANSFORM = "transform"
    CONDITION = "condition"


@dataclass
class PipelineStep:
    """A single step in the processing pipeline."""
    name: str
    step_type: PipelineStepType
    params: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "step_type": self.step_type.value,
            "params": self.params,
            "enabled": self.enabled,
        }


@dataclass
class PipelineResult:
    """Result of a pipeline execution."""
    success: bool
    image: Optional[np.ndarray] = None
    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0


class PipelineScheduler:
    """
    Workflow scheduler for batch image processing.

    Manages execution order, dependencies, and error handling.
    """

    def __init__(self):
        self.steps: List[PipelineStep] = []
        self.processor = ImageProcessor()
        self.levels = LevelsAdjustment()
        self.wb = WhiteBalance()
        self.sharp = HighPassSharpening()
        self.clahe = CLAHEProcessor()
        self.enhancer = ImageEnhancer()
        self.auto_enhancer = AutoEnhancer()

    def add_step(self, step: PipelineStep) -> "PipelineScheduler":
        """Add a step to the pipeline."""
        self.steps.append(step)
        logger.info(f"Added step: {step.name} ({step.step_type.value})")
        return self

    def remove_step(self, name: str) -> bool:
        """Remove a step by name."""
        for i, step in enumerate(self.steps):
            if step.name == name:
                self.steps.pop(i)
                logger.info(f"Removed step: {name}")
                return True
        return False

    def clear_steps(self):
        """Clear all steps."""
        self.steps.clear()
        logger.info("Pipeline cleared")

    def get_step(self, name: str) -> Optional[PipelineStep]:
        """Get a step by name."""
        for step in self.steps:
            if step.name == name:
                return step
        return None

    def reorder_steps(self, from_index: int, to_index: int):
        """Reorder steps."""
        if 0 <= from_index < len(self.steps) and 0 <= to_index < len(self.steps):
            step = self.steps.pop(from_index)
            self.steps.insert(to_index, step)
            logger.info(f"Reordered step from {from_index} to {to_index}")

    def execute(self, image: np.ndarray, context: Optional[Dict] = None) -> PipelineResult:
        """
        Execute the pipeline on an image.

        Args:
            image: Input image
            context: Optional context dictionary

        Returns:
            PipelineResult with processed image
        """
        start_time = time.time()
        result = PipelineResult(success=True)

        try:
            current = image.copy()

            for step in self.steps:
                if not step.enabled:
                    continue

                current = self._execute_step(step, current, context)
                if current is None:
                    raise ValueError(f"Step {step.name} returned None")

            result.image = current
            result.duration = time.time() - start_time

        except Exception as e:
            result.success = False
            result.error = str(e)
            result.duration = time.time() - start_time
            logger.error(f"Pipeline error: {e}")

        return result

    def _execute_step(
        self, step: PipelineStep, image: np.ndarray, context: Optional[Dict]
    ) -> Optional[np.ndarray]:
        """Execute a single step."""
        params = step.params

        if step.step_type == PipelineStepType.LOAD:
            path = params.get("path")
            return self.processor.load_image(path)

        elif step.step_type == PipelineStepType.SAVE:
            path = params.get("path")
            self.processor.save_image(image, path)
            return image

        elif step.step_type == PipelineStepType.PROCESS:
            processor_type = params.get("type")

            if processor_type == "levels":
                return self.levels.adjust(
                    image,
                    shadows=params.get("shadows", 0),
                    midtones=params.get("midtones", 1.0),
                    highlights=params.get("highlights", 255),
                )

            elif processor_type == "white_balance":
                return self.wb.adjust(
                    image,
                    temperature=params.get("temperature", 0),
                    tint=params.get("tint", 0),
                )

            elif processor_type == "sharpening":
                return self.sharp.apply(
                    image,
                    radius=params.get("radius", 1.0),
                    amount=params.get("amount", 1.0),
                    blend_mode=params.get("blend_mode", "soft_light"),
                )

            elif processor_type == "clahe":
                return self.clahe.apply(
                    image,
                    clip_limit=params.get("clip_limit", 2.0),
                    tile_size=params.get("tile_size", 8),
                )

        elif step.step_type == PipelineStepType.ENHANCE:
            enhance_type = params.get("type")

            if enhance_type == "auto":
                mode = params.get("mode", "moderate")
                return self.auto_enhancer.auto_enhance(image, mode=mode)

            elif enhance_type == "denoise":
                return self.enhancer._denoise(image)

            elif enhance_type == "sharpen":
                return self.enhancer._sharpen(image)

            elif enhance_type == "upscale":
                scale = params.get("scale", 2)
                return self.enhancer.sr_model.upscale(image, scale)

        elif step.step_type == PipelineStepType.TRANSFORM:
            transform_type = params.get("type")

            if transform_type == "resize":
                return self.processor.resize(
                    image,
                    width=params.get("width"),
                    height=params.get("height"),
                    scale=params.get("scale"),
                )

            elif transform_type == "crop":
                return self.processor.crop(
                    image,
                    x=params.get("x", 0),
                    y=params.get("y", 0),
                    width=params.get("width"),
                    height=params.get("height"),
                )

            elif transform_type == "brightness":
                return self.processor.adjust_brightness(
                    image, params.get("factor", 1.0)
                )

            elif transform_type == "contrast":
                return self.processor.adjust_contrast(
                    image, params.get("factor", 1.0)
                )

        return image

    def to_json(self) -> str:
        """Export pipeline to JSON."""
        return json.dumps(
            {"steps": [s.to_dict() for s in self.steps]},
            indent=2,
        )

    def from_json(self, json_str: str):
        """Load pipeline from JSON."""
        data = json.loads(json_str)
        self.steps = []
        for step_data in data.get("steps", []):
            step = PipelineStep(
                name=step_data["name"],
                step_type=PipelineStepType(step_data["step_type"]),
                params=step_data.get("params", {}),
                enabled=step_data.get("enabled", True),
            )
            self.steps.append(step)
        logger.info(f"Loaded pipeline with {len(self.steps)} steps")


class PresetPipeline:
    """Pre-built pipeline presets."""

    @staticmethod
    def auto_enhance_pipeline(mode: str = "moderate") -> PipelineScheduler:
        """Create auto enhancement pipeline."""
        pipeline = PipelineScheduler()
        pipeline.add_step(
            PipelineStep(
                name="auto_enhance",
                step_type=PipelineStepType.ENHANCE,
                params={"type": "auto", "mode": mode},
            )
        )
        return pipeline

    @staticmethod
    def professional_pipeline() -> PipelineScheduler:
        """Create professional photo editing pipeline."""
        pipeline = PipelineScheduler()
        pipeline.add_step(
            PipelineStep(
                name="white_balance",
                step_type=PipelineStepType.PROCESS,
                params={"type": "white_balance", "temperature": 10, "tint": 5},
            )
        )
        pipeline.add_step(
            PipelineStep(
                name="levels",
                step_type=PipelineStepType.PROCESS,
                params={"shadows": 10, "midtones": 1.05, "highlights": 245},
            )
        )
        pipeline.add_step(
            PipelineStep(
                name="clahe",
                step_type=PipelineStepType.PROCESS,
                params={"clip_limit": 1.5, "tile_size": 8},
            )
        )
        pipeline.add_step(
            PipelineStep(
                name="sharpening",
                step_type=PipelineStepType.PROCESS,
                params={"type": "sharpening", "radius": 1.0, "amount": 0.3, "blend_mode": "soft_light"},
            )
        )
        return pipeline

    @staticmethod
    def denoise_upscale_pipeline(scale: int = 2) -> PipelineScheduler:
        """Create denoise and upscale pipeline."""
        pipeline = PipelineScheduler()
        pipeline.add_step(
            PipelineStep(
                name="denoise",
                step_type=PipelineStepType.ENHANCE,
                params={"type": "denoise"},
            )
        )
        pipeline.add_step(
            PipelineStep(
                name="upscale",
                step_type=PipelineStepType.ENHANCE,
                params={"type": "upscale", "scale": scale},
            )
        )
        return pipeline
