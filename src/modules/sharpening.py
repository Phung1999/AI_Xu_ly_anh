"""
High Pass Sharpening Module
Phase 1 - Task 1.5

Implements Photoshop High Pass filter with Soft Light/Overlay blending.
"""

import numpy as np
import cv2
from typing import Literal


class HighPassSharpening:
    """
    High Pass filter sharpening with blend mode support.
    """

    def __init__(self):
        self.radius = 1.0
        self.amount = 1.0
        self.threshold = 0

    def apply(
        self,
        image: np.ndarray,
        radius: float = 1.0,
        amount: float = 1.0,
        blend_mode: Literal["soft_light", "overlay", "normal"] = "soft_light",
    ) -> np.ndarray:
        """
        Apply high pass sharpening.

        Formula: hpf = original_img - GaussianBlur(img) + 127

        Args:
            image: Input RGB image
            radius: Blur radius for high pass
            amount: Sharpening amount
            blend_mode: Blending mode

        Returns:
            np.ndarray: Sharpened image
        """
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        blur_size = int(radius * 3) | 1
        blurred = cv2.GaussianBlur(img_bgr, (blur_size, blur_size), 0)

        hpf = img_bgr.astype(np.float32) - blurred.astype(np.float32) + 127
        hpf = np.clip(hpf, 0, 255).astype(np.uint8)

        if blend_mode == "soft_light":
            result = self._soft_light_blend(img_bgr, hpf, amount)
        elif blend_mode == "overlay":
            result = self._overlay_blend(img_bgr, hpf, amount)
        else:
            result = cv2.addWeighted(img_bgr, 1, hpf, amount, 0)

        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    def _soft_light_blend(self, base: np.ndarray, overlay: np.ndarray, amount: float) -> np.ndarray:
        """Soft Light blending mode."""
        base_f = base.astype(np.float32) / 255
        overlay_f = overlay.astype(np.float32) / 255

        result = np.where(
            overlay_f < 0.5,
            2 * base_f * overlay_f + base_f ** 2 * (1 - 2 * overlay_f),
            2 * base_f * (1 - base_f) + np.sqrt(base_f) * (2 * overlay_f - 1),
        )

        return np.clip(base + (result - base_f) * amount * 255, 0, 255).astype(np.uint8)

    def _overlay_blend(self, base: np.ndarray, overlay: np.ndarray, amount: float) -> np.ndarray:
        """Overlay blending mode."""
        base_f = base.astype(np.float32) / 255
        overlay_f = overlay.astype(np.float32) / 255

        result = np.where(
            base_f < 0.5,
            2 * base_f * overlay_f,
            1 - 2 * (1 - base_f) * (1 - overlay_f),
        )

        return np.clip(base + (result - base_f) * amount * 255, 0, 255).astype(np.uint8)

    def unsharp_mask(
        self,
        image: np.ndarray,
        amount: float = 1.5,
        radius: float = 1.0,
        threshold: int = 0,
    ) -> np.ndarray:
        """
        Classic Unsharp Mask sharpening.

        Args:
            image: Input image
            amount: Sharpening amount
            radius: Blur radius
            threshold: Minimum difference to apply sharpening

        Returns:
            np.ndarray: Sharpened image
        """
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        blur_size = int(radius * 3) | 1
        blurred = cv2.GaussianBlur(img_bgr, (blur_size, blur_size), 0)

        diff = cv2.subtract(img_bgr, blurred)

        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY)

        sharpened = cv2.addWeighted(img_bgr, 1 + amount, blurred, -amount, 0)

        result = np.where(mask[:, :, np.newaxis] == 255, sharpened, img_bgr)

        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
