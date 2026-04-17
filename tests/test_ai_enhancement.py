"""
Test suite for AI Enhancement Module - Task 2.2 & 2.3
Phase 2: AI Foundation

Run: pytest tests/test_ai_enhancement.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestSuperResolutionModel:
    """Test suite for SuperResolutionModel"""

    def test_initialization(self):
        """Test model initialization"""
        from src.ai.enhancement import SuperResolutionModel

        model = SuperResolutionModel("bicubic")
        assert model is not None
        assert model.model_type == "bicubic"

    def test_load_bicubic(self):
        """Test loading bicubic model"""
        from src.ai.enhancement import SuperResolutionModel

        model = SuperResolutionModel("bicubic")
        loaded = model.load()
        assert loaded is True
        assert model.model_loaded is True

    def test_upscale_bicubic_2x(self):
        """Test bicubic upscale 2x"""
        from src.ai.enhancement import SuperResolutionModel

        model = SuperResolutionModel("bicubic")
        model.load()

        img = np.zeros((100, 100, 3), dtype=np.uint8)
        upscaled = model.upscale(img, scale=2)

        assert upscaled.shape == (200, 200, 3)

    def test_upscale_bicubic_4x(self):
        """Test bicubic upscale 4x"""
        from src.ai.enhancement import SuperResolutionModel

        model = SuperResolutionModel("bicubic")
        model.load()

        img = np.zeros((50, 50, 3), dtype=np.uint8)
        upscaled = model.upscale(img, scale=4)

        assert upscaled.shape == (200, 200, 3)

    def test_upscale_preserves_content(self):
        """Test upscaling preserves main content"""
        from src.ai.enhancement import SuperResolutionModel

        model = SuperResolutionModel("bicubic")
        model.load()

        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[40:60, 40:60, :] = 255

        upscaled = model.upscale(img, scale=2)

        center_region = upscaled[80:120, 80:120, :]
        assert center_region.max() > 200


class TestImageEnhancer:
    """Test suite for ImageEnhancer"""

    def test_initialization(self):
        """Test enhancer initialization"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        assert enhancer is not None

    def test_enhance_all_steps(self):
        """Test full enhancement pipeline"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.enhance(img, denoise=True, sharpen=True, upscale=True, scale=2)

        assert enhanced.shape[0] > img.shape[0]
        assert enhanced.shape[1] > img.shape[1]

    def test_enhance_denoise_only(self):
        """Test denoising only"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.enhance(img, denoise=True, sharpen=False, upscale=False)

        assert enhanced.shape == img.shape

    def test_enhance_sharpen_only(self):
        """Test sharpening only"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.enhance(img, denoise=False, sharpen=True, upscale=False)

        assert enhanced.shape == img.shape

    def test_enhance_upscale_only(self):
        """Test upscaling only"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.enhance(img, denoise=False, sharpen=False, upscale=True, scale=2)

        assert enhanced.shape == (200, 200, 3)

    def test_analyze_image(self):
        """Test image analysis"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, :] = 128

        analysis = enhancer.analyze_image(img)

        assert "brightness" in analysis
        assert "sharpness" in analysis
        assert "contrast" in analysis
        assert "suggestions" in analysis
        assert isinstance(analysis["suggestions"], list)

    def test_analyze_dark_image(self):
        """Test analyzing dark image"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        analysis = enhancer.analyze_image(img)

        assert "brightness" in analysis
        assert len(analysis["suggestions"]) >= 1

    def test_analyze_blurry_image(self):
        """Test analyzing blurry image"""
        from src.ai.enhancement import ImageEnhancer

        enhancer = ImageEnhancer()
        img = np.ones((100, 100, 3), dtype=np.uint8) * 128

        analysis = enhancer.analyze_image(img)

        assert analysis["sharpness"] < 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
