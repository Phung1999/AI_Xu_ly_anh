"""
Test suite for White Balance Module - Task 1.4
Phase 1: Foundation

Run: pytest tests/test_white_balance.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestWhiteBalance:
    """Test suite for WhiteBalance class"""

    def test_initialization(self):
        """Test WhiteBalance can be initialized"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        assert wb is not None

    def test_adjust_warm(self):
        """Test warm temperature adjustment"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 100
        img[:, :, 1] = 100
        img[:, :, 2] = 100

        adjusted = wb.adjust(img, temperature=50, tint=0)

        assert adjusted.shape == img.shape
        assert adjusted.dtype == np.uint8

    def test_adjust_cool(self):
        """Test cool temperature adjustment"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        adjusted = wb.adjust(img, temperature=-50, tint=0)

        assert adjusted.shape == img.shape

    def test_adjust_tint_green(self):
        """Test green tint adjustment"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        adjusted = wb.adjust(img, temperature=0, tint=-50)

        assert adjusted.shape == img.shape

    def test_adjust_tint_magenta(self):
        """Test magenta tint adjustment"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        adjusted = wb.adjust(img, temperature=0, tint=50)

        assert adjusted.shape == img.shape

    def test_auto_white_balance(self):
        """Test automatic white balance calculation"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 100
        img[:, :, 1] = 100
        img[:, :, 2] = 150

        temp, tint = wb.auto_white_balance(img)

        assert -100 <= temp <= 100
        assert -100 <= tint <= 100

    def test_gray_world(self):
        """Test gray world white balance"""
        from src.modules.white_balance import WhiteBalance

        wb = WhiteBalance()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 80
        img[:, :, 1] = 120
        img[:, :, 2] = 180

        corrected = wb.gray_world(img)

        assert corrected.shape == img.shape
        assert corrected.dtype == np.uint8
        assert np.all(corrected >= 0)
        assert np.all(corrected <= 255)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
