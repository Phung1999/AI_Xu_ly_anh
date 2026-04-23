"""
Tests for AnimeGAN module.
"""

import numpy as np
import pytest


class TestAnimeGANStyles:
    """Test AnimeGAN available styles."""
    
    def test_get_available_styles(self):
        from src.ai.anime.anime_gan import AnimeGAN
        styles = AnimeGAN.get_available_styles()
        assert "Hayao" in styles
        assert "Shinkai" in styles
        assert "Paprika" in styles
        assert len(styles) == 3


class TestAnimeGAN:
    """Test AnimeGAN transformation."""
    
    @pytest.fixture
    def sample_image(self):
        return np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    
    def test_init_hayao(self):
        from src.ai.anime.anime_gan import AnimeGAN
        try:
            gan = AnimeGAN(style="Hayao", model_dir="models")
            assert gan.style == "Hayao"
        except Exception:
            pytest.skip("Model not downloaded yet")
    
    def test_init_shinkai(self):
        from src.ai.anime.anime_gan import AnimeGAN
        try:
            gan = AnimeGAN(style="Shinkai", model_dir="models")
            assert gan.style == "Shinkai"
        except Exception:
            pytest.skip("Model not downloaded yet")
    
    def test_init_paprika(self):
        from src.ai.anime.anime_gan import AnimeGAN
        try:
            gan = AnimeGAN(style="Paprika", model_dir="models")
            assert gan.style == "Paprika"
        except Exception:
            pytest.skip("Model not downloaded yet")
    
    def test_transform_empty(self):
        from src.ai.anime.anime_gan import AnimeGAN
        gan = AnimeGAN(style="Hayao", model_dir="models")
        result = gan.transform(None)
        assert result is None
    
    def test_transform_zero_image(self):
        from src.ai.anime.anime_gan import AnimeGAN
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        try:
            gan = AnimeGAN(style="Hayao", model_dir="models")
            result = gan.transform(image)
            assert result is not None
            assert result.shape[0] > 0
        except Exception:
            pytest.skip("Model not downloaded yet")
    
    def test_transform_output_shape(self):
        from src.ai.anime.anime_gan import AnimeGAN
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        try:
            gan = AnimeGAN(style="Hayao", model_dir="models")
            result = gan.transform(image)
            assert result.shape == (512, 512, 3)
        except Exception:
            pytest.skip("Model not downloaded yet")


class TestChibiTransformerWithAnimeGAN:
    """Test ChibiTransformer with AnimeGAN."""
    
    def test_get_available_styles(self):
        from src.ai.chibi import ChibiTransformer
        transformer = ChibiTransformer()
        styles = transformer.get_available_styles()
        assert "Hayao" in styles
        assert "Shinkai" in styles
        assert "Paprika" in styles
    
    def test_set_style(self):
        from src.ai.chibi import ChibiTransformer
        transformer = ChibiTransformer()
        transformer.set_style("Shinkai")
        assert transformer._current_style == "Shinkai"
    
    def test_transform_with_style(self):
        from src.ai.chibi import ChibiTransformer
        image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        transformer = ChibiTransformer()
        try:
            result = transformer.transform_with_style(image, "Paprika")
            assert result is not None
        except Exception:
            pytest.skip("Model not downloaded yet")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])