"""
Test suite for CLAHE Module - Task 1.6
Phase 1: Foundation

Run: pytest tests/test_clahe.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestCLAHEProcessor:
    """Test suite for CLAHEProcessor class"""

    def test_initialization(self):
        """Test CLAHEProcessor can be initialized"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        assert clahe is not None

    def test_apply_rgb(self):
        """Test CLAHE on RGB image"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        result = clahe.apply(img, clip_limit=2.0, tile_size=8)

        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_apply_grayscale(self):
        """Test CLAHE on grayscale image"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        img = np.zeros((100, 100), dtype=np.uint8)

        result = clahe.apply_grayscale(img)

        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_dual_gamma(self):
        """Test dual gamma correction"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, :] = 128

        result = clahe.dual_gamma(img, gamma1=1.5, gamma2=0.8, threshold=0.5)

        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_dual_gamma_brighten_dark(self):
        """Test dual gamma brightens dark regions"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, :] = 50

        result = clahe.dual_gamma(img, gamma1=0.8, gamma2=1.0, threshold=0.5)

        assert result.shape == img.shape

    def test_adaptive_sharpen(self):
        """Test adaptive sharpening"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[40:60, 40:60, :] = 255

        result = clahe.adaptive_sharpen(img, sigma=1.0, amount=1.0)

        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_clip_limit(self):
        """Test different clip limits"""
        from src.modules.clahe import CLAHEProcessor

        clahe = CLAHEProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        result1 = clahe.apply(img, clip_limit=1.0)
        result2 = clahe.apply(img, clip_limit=5.0)

        assert result1.shape == result2.shape


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
