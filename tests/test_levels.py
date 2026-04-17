"""
Test suite for Levels Module - Task 1.3
Phase 1: Foundation

Run: pytest tests/test_levels.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestLevelsAdjustment:
    """Test suite for LevelsAdjustment class"""

    def test_initialization(self):
        """Test LevelsAdjustment can be initialized"""
        from src.modules.levels import LevelsAdjustment

        levels = LevelsAdjustment()
        assert levels is not None

    def test_identity_lut(self):
        """Test identity LUT is created correctly"""
        from src.modules.levels import LevelsAdjustment

        levels = LevelsAdjustment()
        lut = levels._create_identity_lut()

        assert len(lut) == 256
        assert lut[0] == 0
        assert lut[128] == 128
        assert lut[255] == 255

    def test_calculate_lut(self):
        """Test LUT calculation"""
        from src.modules.levels import LevelsAdjustment

        levels = LevelsAdjustment()
        lut = levels._calculate_lut(
            shadows=0, gamma=1.0, highlights=255,
            shadow_out=0, highlight_out=255
        )

        assert len(lut) == 256
        assert lut[0] == 0
        assert lut[255] == 255

    def test_gamma_correction(self):
        """Test gamma correction in LUT"""
        from src.modules.levels import LevelsAdjustment

        levels = LevelsAdjustment()
        lut = levels._calculate_lut(
            shadows=0, gamma=2.0, highlights=255,
            shadow_out=0, highlight_out=255
        )

        midtone = lut[128]
        assert midtone < 128

    def test_adjust_image(self):
        """Test adjusting an image"""
        from src.modules.levels import LevelsAdjustment

        levels = LevelsAdjustment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, :] = 128

        adjusted = levels.adjust(img, shadows=0, midtones=1.0, highlights=255)

        assert adjusted.shape == img.shape
        assert adjusted.dtype == np.uint8

    def test_auto_levels(self):
        """Test automatic levels calculation"""
        from src.modules.levels import LevelsAdjustment

        levels = LevelsAdjustment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[50:, :, :] = 200

        shadow, highlight = levels.auto_levels(img)

        assert 0 <= shadow <= 128
        assert 128 <= highlight <= 255


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
