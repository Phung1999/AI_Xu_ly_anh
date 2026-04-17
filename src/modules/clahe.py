"""
CLAHE Module - Contrast Limited Adaptive Histogram Equalization
Phase 1 - Task 1.6

Implements CLAHE for local contrast enhancement.
"""

import numpy as np
import cv2
from typing import Tuple


class CLAHEProcessor:
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) processor.
    """

    def __init__(self):
        self.clip_limit = 2.0
        self.tile_size = 8

    def apply(
        self,
        image: np.ndarray,
        clip_limit: float = 2.0,
        tile_size: int = 8,
    ) -> np.ndarray:
        """
        Apply CLAHE to RGB image.

        Args:
            image: Input RGB image
            clip_limit: Contrast limiting parameter
            tile_size: Size of grid for histogram equalization

        Returns:
            np.ndarray: Enhanced image
        """
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))

        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    def apply_grayscale(
        self,
        image: np.ndarray,
        clip_limit: float = 2.0,
        tile_size: int = 8,
    ) -> np.ndarray:
        """
        Apply CLAHE to grayscale image.

        Args:
            image: Input grayscale image
            clip_limit: Contrast limiting parameter
            tile_size: Size of grid

        Returns:
            np.ndarray: Enhanced grayscale image
        """
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
        return clahe.apply(image)

    def dual_gamma(
        self,
        image: np.ndarray,
        gamma1: float = 1.0,
        gamma2: float = 1.0,
        threshold: float = 0.5,
    ) -> np.ndarray:
        """
        Dual Gamma Correction.

        Apply different gamma to dark and bright regions.

        Args:
            image: Input RGB image
            gamma1: Gamma for dark regions
            gamma2: Gamma for bright regions
            threshold: Threshold to separate dark/bright

        Returns:
            np.ndarray: Gamma-corrected image
        """
        result = image.copy().astype(np.float32) / 255.0

        dark_mask = result < threshold
        bright_mask = ~dark_mask

        result[dark_mask] = np.power(result[dark_mask] / threshold, gamma1) * threshold
        result[bright_mask] = np.power(
            (result[bright_mask] - threshold) / (1 - threshold), gamma2
        ) * (1 - threshold) + threshold

        return np.clip(result * 255, 0, 255).astype(np.uint8)

    def adaptive_sharpen(
        self,
        image: np.ndarray,
        sigma: float = 1.0,
        amount: float = 1.0,
    ) -> np.ndarray:
        """
        Adaptive sharpening based on local contrast.

        Args:
            image: Input image
            sigma: Gaussian blur sigma
            amount: Sharpening amount

        Returns:
            np.ndarray: Adaptively sharpened image
        """
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        blurred = cv2.GaussianBlur(img_bgr, (0, 0), sigma)
        laplacian = cv2.subtract(img_bgr, blurred)

        sharpened = cv2.addWeighted(img_bgr, 1 + amount, laplacian, -amount, 0)

        return cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
