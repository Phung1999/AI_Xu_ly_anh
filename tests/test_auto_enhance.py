"""
Test suite for Auto Enhancement Logic - Task 2.4
Phase 2: AI Foundation

Run: pytest tests/test_auto_enhance.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestAutoEnhancer:
    """Test suite for AutoEnhancer"""

    def test_initialization(self):
        """Test AutoEnhancer initialization"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        assert enhancer is not None

    def test_analyze_image(self):
        """Test image analysis"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        analysis = enhancer.analyze(img)

        assert "brightness" in analysis
        assert "sharpness" in analysis
        assert "contrast" in analysis
        assert "levels" in analysis
        assert "white_balance" in analysis

    def test_analyze_gray_image(self):
        """Test analyzing grayscale-like image"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.ones((100, 100, 3), dtype=np.uint8) * 128

        analysis = enhancer.analyze(img)

        assert analysis["brightness"] > 40

    def test_analyze_color_image(self):
        """Test analyzing color image"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 255
        img[:, :, 1] = 128
        img[:, :, 2] = 64

        analysis = enhancer.analyze(img)

        assert "white_balance" in analysis

    def test_auto_enhance_conservative(self):
        """Test conservative auto enhancement"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.auto_enhance(img, mode="conservative")

        assert enhanced.shape == img.shape

    def test_auto_enhance_moderate(self):
        """Test moderate auto enhancement"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.auto_enhance(img, mode="moderate")

        assert enhanced.shape == img.shape

    def test_auto_enhance_aggressive(self):
        """Test aggressive auto enhancement"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.auto_enhance(img, mode="aggressive")

        assert enhanced.shape == img.shape

    def test_auto_enhance_with_target(self):
        """Test auto enhancement with target score"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        enhanced = enhancer.auto_enhance(img, target_score=80.0)

        assert enhanced.shape == img.shape

    def test_enhance_with_preset(self):
        """Test enhancement with preset"""
        from src.ai.auto_enhance import AutoEnhancer, EnhancementSettings

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        preset = EnhancementSettings(
            temperature=10,
            tint=5,
            sharpness=0.5,
            clahe_clip=2.0,
        )

        enhanced = enhancer.enhance_with_preset(img, preset)

        assert enhanced.shape == img.shape

    def test_create_preset_from_analysis(self):
        """Test creating preset from analysis"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        preset = enhancer.create_preset_from_analysis(img)

        assert preset is not None
        assert isinstance(preset.temperature, int)
        assert isinstance(preset.sharpness, float)

    def test_batch_analyze(self):
        """Test batch analysis"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        images = [np.zeros((50, 50, 3), dtype=np.uint8) for _ in range(3)]

        results = enhancer.batch_analyze(images)

        assert len(results) == 3
        for result in results:
            assert "brightness" in result

    def test_smart_compare(self):
        """Test smart comparison"""
        from src.ai.auto_enhance import AutoEnhancer

        enhancer = AutoEnhancer()
        original = np.zeros((100, 100, 3), dtype=np.uint8)
        enhanced = np.ones((100, 100, 3), dtype=np.uint8) * 128

        comparison = enhancer.smart_compare(original, enhanced)

        assert "quality_scores" in comparison
        assert "original_metrics" in comparison
        assert "enhanced_metrics" in comparison
        assert "improvements" in comparison


class TestEnhancementSettings:
    """Test EnhancementSettings dataclass"""

    def test_default_settings(self):
        """Test default settings"""
        from src.ai.auto_enhance import EnhancementSettings

        settings = EnhancementSettings()

        assert settings.temperature == 0
        assert settings.tint == 0
        assert settings.shadows == 0
        assert settings.highlights == 255
        assert settings.midtones == 1.0
        assert settings.sharpness == 0.0
        assert settings.denoise is False
        assert settings.upscale is False

    def test_custom_settings(self):
        """Test custom settings"""
        from src.ai.auto_enhance import EnhancementSettings

        settings = EnhancementSettings(
            temperature=20,
            tint=10,
            sharpness=0.5,
            denoise=True,
            upscale=True,
            scale=4,
        )

        assert settings.temperature == 20
        assert settings.tint == 10
        assert settings.sharpness == 0.5
        assert settings.denoise is True
        assert settings.upscale is True
        assert settings.scale == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
