"""
Levels Adjustment Module - Photoshop Levels Clone
Phase 1 - Task 1.3

Implements Photoshop-style Levels adjustment with LUT-based correction.
"""

import numpy as np
import cv2
from typing import Tuple, Optional


class LevelsAdjustment:
    """
    Photoshop Levels adjustment implementation.

    Adjusts shadows, midtones (gamma), and highlights using Lookup Table.
    """

    def __init__(self):
        self._lut = self._create_identity_lut()

    def _create_identity_lut(self) -> np.ndarray:
        """Create identity LUT (no change)."""
        return np.arange(256, dtype=np.uint8)

    def adjust(
        self,
        image: np.ndarray,
        shadows: int = 0,
        midtones: float = 1.0,
        highlights: int = 255,
        shadow_output: int = 0,
        highlight_output: int = 255,
    ) -> np.ndarray:
        """
        Apply levels adjustment.

        Args:
            image: Input RGB image
            shadows: Input shadow point (0-255)
            midtones: Gamma value (1.0 = no change)
            highlights: Input highlight point (0-255)
            shadow_output: Output shadow value
            highlight_output: Output highlight value

        Returns:
            np.ndarray: Adjusted image
        """
        lut = self._calculate_lut(shadows, midtones, highlights, shadow_output, highlight_output)

        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        adjusted = cv2.LUT(img_bgr, lut)
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)

    def _calculate_lut(
        self,
        shadows: int,
        gamma: float,
        highlights: int,
        shadow_out: int,
        highlight_out: int,
    ) -> np.ndarray:
        """
        Calculate Lookup Table for levels adjustment.

        Args:
            shadows: Input shadow point
            gamma: Gamma value for midtones
            highlights: Input highlight point
            shadow_out: Output shadow value
            highlight_out: Output highlight value

        Returns:
            np.ndarray: 256-element LUT
        """
        lut = np.zeros(256, dtype=np.float32)

        for i in range(256):
            if i <= shadows:
                lut[i] = shadow_out
            elif i >= highlights:
                lut[i] = highlight_out
            else:
                normalized = (i - shadows) / (highlights - shadows)
                lut[i] = shadow_out + (highlight_out - shadow_out) * (normalized ** gamma)

        return lut.astype(np.uint8)

    def auto_levels(self, image: np.ndarray) -> Tuple[int, int]:
        """
        Calculate automatic levels values.

        Args:
            image: Input image

        Returns:
            Tuple of (shadow, highlight) values
        """
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        total = hist.sum()

        shadow = 0
        cumulative = 0
        for i in range(256):
            cumulative += hist[i]
            if cumulative >= total * 0.005:
                shadow = i
                break

        highlight = 255
        cumulative = 0
        for i in range(255, -1, -1):
            cumulative += hist[i]
            if cumulative >= total * 0.005:
                highlight = i
                break

        return shadow, highlight
