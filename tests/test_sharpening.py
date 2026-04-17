"""
Test suite for High Pass Sharpening Module - Task 1.5
Phase 1: Foundation

Run: pytest tests/test_sharpening.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestHighPassSharpening:
    """Test suite for HighPassSharpening class"""

    def test_initialization(self):
        """Test HighPassSharpening can be initialized"""
        from src.modules.sharpening import HighPassSharpening

        sharp = HighPassSharpening()
        assert sharp is not None

    def test_apply_soft_light(self):
        """Test high pass with soft light blend"""
        from src.modules.sharpening import HighPassSharpening

        sharp = HighPassSharpening()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[40:60, 40:60, :] = 200

        result = sharp.apply(img, radius=2.0, amount=1.0, blend_mode="soft_light")

        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_apply_overlay(self):
        """Test high pass with overlay blend"""
        from src.modules.sharpening import HighPassSharpening

        sharp = HighPassSharpening()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        result = sharp.apply(img, radius=1.0, amount=0.5, blend_mode="overlay")

        assert result.shape == img.shape

    def test_apply_normal(self):
        """Test high pass with normal blend"""
        from src.modules.sharpening import HighPassSharpening

        sharp = HighPassSharpening()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        result = sharp.apply(img, blend_mode="normal")

        assert result.shape == img.shape

    def test_unsharp_mask(self):
        """Test unsharp mask sharpening"""
        from src.modules.sharpening import HighPassSharpening

        sharp = HighPassSharpening()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[40:60, 40:60, :] = 255

        result = sharp.unsharp_mask(img, amount=1.5, radius=1.0, threshold=0)

        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_unsharp_mask_with_threshold(self):
        """Test unsharp mask with threshold"""
        from src.modules.sharpening import HighPassSharpening

        sharp = HighPassSharpening()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[40:60, 40:60, :] = 100

        result = sharp.unsharp_mask(img, amount=1.0, radius=1.0, threshold=50)

        assert result.shape == img.shape


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
