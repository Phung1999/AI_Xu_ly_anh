"""
Chibi Transformer - Chuyển đổi ảnh thành style Chibi/Anime
Sử dụng AnimeGANv3 ONNX models
"""

import numpy as np
import cv2
from typing import Optional

from src.ai.chibi.settings import ChibiSettings
from src.ai.anime.anime_gan import AnimeGAN


class ChibiTransformer:
    """
    Chibi style transformation using AnimeGANv3.
    Tạo anime-style từ ảnh thật với model ONNX.
    """
    
    def __init__(self, settings: Optional[ChibiSettings] = None):
        self.settings = settings or ChibiSettings()
        self._anime_gan = None
        self._current_style = "Hayao"
    
    @property
    def anime_gan(self) -> AnimeGAN:
        if self._anime_gan is None or self._anime_gan.style != self._current_style:
            self._anime_gan = AnimeGAN(style=self._current_style)
        return self._anime_gan
    
    def set_style(self, style: str):
        """Set anime style (Hayao, Shinkai, Paprika)."""
        if style not in AnimeGAN.get_available_styles():
            raise ValueError(f"Invalid style: {style}. Available: {AnimeGAN.get_available_styles()}")
        self._current_style = style
        self._anime_gan = None
    
    def transform(self, image: np.ndarray) -> np.ndarray:
        """
        Transform ảnh sang style Chibi/Anime.
        
        Args:
            image: Ảnh RGB đầu vào
            
        Returns:
            Ảnh Chibi/Anime style
        """
        if image is None or image.size == 0:
            return image
        
        result = self.anime_gan.transform(image)
        
        if self.settings.output_size:
            result = cv2.resize(result, self.settings.output_size)
        
        return result
    
    def transform_with_style(self, image: np.ndarray, style: str) -> np.ndarray:
        """
        Transform with specific style.
        
        Args:
            image: Ảnh RGB đầu vào
            style: Anime style (Hayao, Shinkai, Paprika)
            
        Returns:
            Ảnh Anime style
        """
        self.set_style(style)
        return self.transform(image)
    
    @staticmethod
    def get_available_styles() -> list:
        return AnimeGAN.get_available_styles()