"""
White Balance Module
Phase 1 - Task 1.4

Adjusts color temperature (warm/cool) and tint (green/magenta).
"""

import numpy as np
import cv2
from typing import Tuple


class WhiteBalance:
    """
    White balance adjustment with Temperature and Tint controls.

    Temperature: -100 (cool/blue) to +100 (warm/yellow)
    Tint: -100 (green) to +100 (magenta)
    """

    def __init__(self):
        self.temperature = 0
        self.tint = 0

    def adjust(self, image: np.ndarray, temperature: int = 0, tint: int = 0) -> np.ndarray:
        """
        Apply white balance adjustment.

        Args:
            image: Input RGB image
            temperature: -100 to +100 (cool to warm)
            tint: -100 to +100 (green to magenta)

        Returns:
            np.ndarray: Adjusted image
        """
        result = image.copy().astype(np.float32)

        temp_factor = temperature / 100.0
        tint_factor = tint / 100.0

        result[:, :, 0] += temp_factor * 30 - tint_factor * 15
        result[:, :, 1] += tint_factor * 10
        result[:, :, 2] += temp_factor * 30 + tint_factor * 15

        result = np.clip(result, 0, 255).astype(np.uint8)
        return result

    def auto_white_balance(self, image: np.ndarray) -> Tuple[int, int]:
        """
        Calculate automatic white balance.

        Uses gray world assumption.

        Args:
            image: Input image

        Returns:
            Tuple of (temperature, tint)
        """
        avg_b = image[:, :, 0].mean()
        avg_g = image[:, :, 1].mean()
        avg_r = image[:, :, 2].mean()

        gray = (avg_b + avg_g + avg_r) / 3

        if gray < 1.0:
            return 0, 0

        temperature = int((avg_r - avg_b) / gray * 50)
        tint = int((avg_g - (avg_r + avg_b) / 2) / gray * 50)

        temperature = max(-100, min(100, temperature))
        tint = max(-100, min(100, tint))

        return temperature, tint

    def gray_world(self, image: np.ndarray) -> np.ndarray:
        """
        Apply gray world white balance.

        Args:
            image: Input RGB image

        Returns:
            np.ndarray: Corrected image
        """
        result = image.copy().astype(np.float32)

        avg_b = result[:, :, 0].mean()
        avg_g = result[:, :, 1].mean()
        avg_r = result[:, :, 2].mean()

        gray = (avg_b + avg_g + avg_r) / 3

        result[:, :, 0] *= gray / avg_b if avg_b > 0 else 1
        result[:, :, 1] *= gray / avg_g if avg_g > 0 else 1
        result[:, :, 2] *= gray / avg_r if avg_r > 0 else 1

        return np.clip(result, 0, 255).astype(np.uint8)
