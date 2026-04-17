"""
Auto Enhancement Logic - Task 2.4
Phase 2: AI Foundation

Intelligent image enhancement based on AI analysis.
Combines IQA, image processing, and AI models.
"""

import numpy as np
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from loguru import logger

from src.modules.levels import LevelsAdjustment
from src.modules.white_balance import WhiteBalance
from src.modules.sharpening import HighPassSharpening
from src.modules.clahe import CLAHEProcessor
from src.modules.iqa import ImageQualityAssessment
from src.ai.enhancement import ImageEnhancer


@dataclass
class EnhancementSettings:
    """Settings for auto enhancement."""
    temperature: int = 0
    tint: int = 0
    shadows: int = 0
    highlights: int = 255
    midtones: float = 1.0
    sharpness: float = 0.0
    contrast: float = 0.0
    clahe_clip: float = 2.0
    clahe_tile: int = 8
    denoise: bool = False
    upscale: bool = False
    scale: int = 2


class AutoEnhancer:
    """
    Intelligent Auto Enhancement System.

    Analyzes image quality and automatically applies appropriate enhancements.
    """

    def __init__(self):
        self.levels = LevelsAdjustment()
        self.wb = WhiteBalance()
        self.sharp = HighPassSharpening()
        self.clahe = CLAHEProcessor()
        self.iqa = ImageQualityAssessment()
        self.enhancer = ImageEnhancer()

    def analyze(self, image: np.ndarray) -> Dict:
        """
        Comprehensive image analysis.

        Args:
            image: Input RGB image

        Returns:
            Dictionary with quality metrics and recommendations
        """
        analysis = self.enhancer.analyze_image(image)

        shadow, highlight = self.levels.auto_levels(image)
        temp, tint = self.wb.auto_white_balance(image)

        analysis["levels"] = {
            "shadow": shadow,
            "highlight": highlight,
            "range": highlight - shadow,
        }

        analysis["white_balance"] = {
            "temperature": temp,
            "tint": tint,
        }

        return analysis

    def auto_enhance(
        self,
        image: np.ndarray,
        mode: Literal["conservative", "moderate", "aggressive"] = "moderate",
        target_score: float = 75.0,
    ) -> np.ndarray:
        """
        Automatically enhance image to reach target quality score.

        Args:
            image: Input RGB image
            mode: Enhancement mode (conservative, moderate, aggressive)
            target_score: Target CQE score to achieve

        Returns:
            Enhanced image
        """
        current = image.copy()
        max_iterations = 10 if mode == "aggressive" else 5 if mode == "moderate" else 3

        mode_multipliers = {
            "conservative": 0.3,
            "moderate": 0.6,
            "aggressive": 1.0,
        }

        multiplier = mode_multipliers[mode]

        for i in range(max_iterations):
            scores = self.iqa.evaluate(image, current)
            cqe = scores.get("cqe", 0)

            if cqe >= target_score:
                logger.info(f"Target score {target_score} reached at iteration {i}")
                break

            current = self._apply_iteration(current, multiplier)

        return current

    def _apply_iteration(self, image: np.ndarray, multiplier: float) -> np.ndarray:
        """Apply one iteration of enhancement."""
        result = image.copy()

        shadow, highlight = self.levels.auto_levels(result)
        if highlight - shadow < 200:
            shadow_adj = max(0, shadow - int(10 * multiplier))
            highlight_adj = min(255, highlight + int(10 * multiplier))
            result = self.levels.adjust(result, shadows=shadow_adj, highlights=highlight_adj, midtones=1.0 + 0.1 * multiplier)

        temp, tint = self.wb.auto_white_balance(result)
        if abs(temp) > 10 or abs(tint) > 10:
            result = self.wb.adjust(result, temperature=int(temp * multiplier * 0.5), tint=int(tint * multiplier * 0.5))

        result = self.clahe.apply(result, clip_limit=2.0 * multiplier, tile_size=8)

        if multiplier >= 0.5:
            result = self.sharp.apply(result, radius=1.0, amount=0.3 * multiplier, blend_mode="soft_light")

        return result

    def enhance_with_preset(
        self,
        image: np.ndarray,
        preset: EnhancementSettings,
    ) -> np.ndarray:
        """
        Apply specific enhancement preset.

        Args:
            image: Input RGB image
            preset: EnhancementSettings preset

        Returns:
            Enhanced image
        """
        result = image.copy()

        if preset.temperature != 0 or preset.tint != 0:
            result = self.wb.adjust(result, preset.temperature, preset.tint)

        if preset.shadows != 0 or preset.highlights != 255 or preset.midtones != 1.0:
            result = self.levels.adjust(
                result,
                shadows=preset.shadows,
                midtones=preset.midtones,
                highlights=preset.highlights,
            )

        if preset.sharpness > 0:
            result = self.sharp.apply(result, radius=1.0, amount=preset.sharpness, blend_mode="soft_light")

        if preset.contrast > 0:
            result = self._adjust_contrast(result, preset.contrast)

        if preset.clahe_clip > 0:
            result = self.clahe.apply(result, clip_limit=preset.clahe_clip, tile_size=preset.clahe_tile)

        if preset.denoise:
            result = self.enhancer._denoise(result)

        if preset.upscale:
            result = self.enhancer.sr_model.upscale(result, preset.scale)

        return result

    def _adjust_contrast(self, image: np.ndarray, amount: float) -> np.ndarray:
        """Adjust contrast."""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        return processor.adjust_contrast(image, 1.0 + amount)

    def create_preset_from_analysis(self, image: np.ndarray) -> EnhancementSettings:
        """
        Create preset settings based on image analysis.

        Args:
            image: Input image

        Returns:
            EnhancementSettings preset
        """
        analysis = self.analyze(image)

        preset = EnhancementSettings()

        if "white_balance" in analysis:
            wb = analysis["white_balance"]
            preset.temperature = int(wb["temperature"] * 0.3)
            preset.tint = int(wb["tint"] * 0.3)

        if "levels" in analysis:
            levels = analysis["levels"]
            if levels["range"] < 200:
                preset.shadows = levels["shadow"]
                preset.highlights = levels["highlight"]
                preset.midtones = 1.05

        if "sharpness" in analysis and analysis["sharpness"] < 50:
            preset.sharpness = 0.3

        if "brightness" in analysis:
            if analysis["brightness"] < 40:
                preset.midtones = 1.2
            elif analysis["brightness"] > 80:
                preset.midtones = 0.8

        return preset

    def batch_analyze(self, images: List[np.ndarray]) -> List[Dict]:
        """
        Analyze multiple images.

        Args:
            images: List of images

        Returns:
            List of analysis results
        """
        results = []
        for img in images:
            analysis = self.analyze(img)
            results.append(analysis)
        return results

    def smart_compare(
        self,
        original: np.ndarray,
        enhanced: np.ndarray,
    ) -> Dict:
        """
        Compare original and enhanced with detailed metrics.

        Args:
            original: Original image
            enhanced: Enhanced image

        Returns:
            Comparison results
        """
        scores = self.iqa.evaluate(original, enhanced)

        original_analysis = self.analyze(original)
        enhanced_analysis = self.analyze(enhanced)

        comparison = {
            "quality_scores": scores,
            "original_metrics": {
                "brightness": original_analysis.get("brightness", 0),
                "sharpness": original_analysis.get("sharpness", 0),
                "contrast": original_analysis.get("contrast", 0),
            },
            "enhanced_metrics": {
                "brightness": enhanced_analysis.get("brightness", 0),
                "sharpness": enhanced_analysis.get("sharpness", 0),
                "contrast": enhanced_analysis.get("contrast", 0),
            },
            "improvements": {
                "brightness": enhanced_analysis.get("brightness", 0) - original_analysis.get("brightness", 0),
                "sharpness": enhanced_analysis.get("sharpness", 0) - original_analysis.get("sharpness", 0),
                "contrast": enhanced_analysis.get("contrast", 0) - original_analysis.get("contrast", 0),
            },
        }

        return comparison
