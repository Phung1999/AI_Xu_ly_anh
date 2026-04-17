"""
Test suite for IQA Module - Task 2.1
Phase 2: AI Foundation

Run: pytest tests/test_iqa.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
import cv2


class TestImageQualityAssessment:
    """Test suite for ImageQualityAssessment class"""

    def test_initialization(self):
        """Test IQA can be initialized"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        assert iqa is not None

    def test_calculate_psnr_identical(self):
        """Test PSNR for identical images"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        psnr = iqa.calculate_psnr(img, img)
        assert psnr == float("inf")

    def test_calculate_psnr_different(self):
        """Test PSNR for different images"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        img2 = np.ones((100, 100, 3), dtype=np.uint8) * 255

        psnr = iqa.calculate_psnr(img1, img2)
        assert psnr >= 0  # Black vs white = 0 dB
        assert psnr < 100

    def test_calculate_psnr_different_shapes(self):
        """Test PSNR handles different shapes"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        img2 = np.ones((50, 50, 3), dtype=np.uint8) * 255

        psnr = iqa.calculate_psnr(img1, img2)
        assert psnr >= 0

    def test_calculate_ssim_identical(self):
        """Test SSIM for identical images"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        ssim = iqa.calculate_ssim(img, img)
        assert abs(ssim - 1.0) < 0.01

    def test_calculate_ssim_different(self):
        """Test SSIM for different images"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        img2 = np.ones((100, 100, 3), dtype=np.uint8) * 255

        ssim = iqa.calculate_ssim(img1, img2)
        assert -1 <= ssim <= 1

    def test_calculate_cqe(self):
        """Test CQE calculation"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 255
        img[:, :, 1] = 128
        img[:, :, 2] = 64

        cqe = iqa.calculate_cqe(img)
        assert 0 <= cqe <= 100

    def test_calculate_eme(self):
        """Test EME calculation"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        eme = iqa.calculate_eme(img)
        assert eme >= 0

    def test_calculate_eme_with_pattern(self):
        """Test EME with varied image"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[0:50, :, :] = 255

        eme = iqa.calculate_eme(img)
        assert eme > 0

    def test_evaluate_full(self):
        """Test full evaluation"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        original = np.zeros((100, 100, 3), dtype=np.uint8)
        enhanced = np.ones((100, 100, 3), dtype=np.uint8) * 128

        results = iqa.evaluate(original, enhanced)

        assert "psnr" in results
        assert "ssim" in results
        assert "cqe" in results
        assert "eme" in results
        assert all(isinstance(v, float) for v in results.values())

    def test_evaluate_with_reference(self):
        """Test evaluation with reference"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        original = np.zeros((100, 100, 3), dtype=np.uint8)
        enhanced = np.ones((100, 100, 3), dtype=np.uint8) * 128
        reference = np.ones((100, 100, 3), dtype=np.uint8) * 140

        results = iqa.evaluate(original, enhanced, reference)

        assert "psnr_ref" in results
        assert "ssim_ref" in results

    def test_get_summary(self):
        """Test summary generation"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()
        scores = {
            "psnr": 35.0,
            "ssim": 0.95,
            "cqe": 75.0,
            "eme": 10.0,
        }

        summary = iqa.get_summary(scores)
        assert "PSNR" in summary
        assert "SSIM" in summary
        assert "CQE" in summary
        assert "EME" in summary


class TestIQAMetrics:
    """Test individual metric calculations"""

    def test_colorfulness_measurement(self):
        """Test colorfulness measurement"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()

        gray_img = np.ones((100, 100, 3), dtype=np.float32) * 0.5
        color_img = np.zeros((100, 100, 3), dtype=np.float32)
        color_img[:, :, 0] = 1.0
        color_img[:, :, 1] = 0.0
        color_img[:, :, 2] = 0.0

        gray_c = iqa._measure_colorfulness(gray_img)
        color_c = iqa._measure_colorfulness(color_img)

        assert 0 <= gray_c <= 1
        assert 0 <= color_c <= 1

    def test_sharpness_measurement(self):
        """Test sharpness measurement"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()

        blur_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
        sharp_img = np.zeros((100, 100, 3), dtype=np.uint8)
        sharp_img[40:60, 40:60, :] = 255

        blur_s = iqa._measure_sharpness(blur_img)
        sharp_s = iqa._measure_sharpness(sharp_img)

        assert 0 <= blur_s <= 1
        assert 0 <= sharp_s <= 1

    def test_contrast_measurement(self):
        """Test contrast measurement"""
        from src.modules.iqa import ImageQualityAssessment

        iqa = ImageQualityAssessment()

        low_contrast = np.ones((100, 100, 3), dtype=np.float32) * 0.5
        high_contrast = np.zeros((100, 100, 3), dtype=np.float32)
        high_contrast[50:, :, :] = 1.0

        low_c = iqa._measure_contrast(low_contrast)
        high_c = iqa._measure_contrast(high_contrast)

        assert 0 <= low_c <= 1
        assert 0 <= high_c <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
