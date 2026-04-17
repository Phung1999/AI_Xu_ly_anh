"""
Color Analyzer Module
Analyzes color palette from reference images
"""

import numpy as np
import cv2
from typing import Dict, List, Tuple
from dataclasses import dataclass
from loguru import logger


@dataclass
class ColorPalette:
    """Represents a color palette extracted from an image."""
    dominant_colors: List[Tuple[int, int, int]]  # RGB colors
    percentages: List[float]  # Percentage of each color
    temperature: str  # "warm", "cool", "neutral"
    saturation: float  # 0-1 average saturation
    brightness: float  # 0-255 average brightness


@dataclass
class ColorTransferSettings:
    """Settings for color transfer."""
    match_luminance: bool = True
    saturation_strength: float = 1.0
    temperature_match: bool = True
    palette_match: bool = True


class ColorAnalyzer:
    """Analyzes color characteristics of images."""
    
    def __init__(self):
        self.palette = None
    
    def analyze(self, image: np.ndarray) -> ColorPalette:
        """
        Analyze color palette of an image.
        
        Args:
            image: RGB image array
            
        Returns:
            ColorPalette with dominant colors and characteristics
        """
        # Convert to RGB if BGR
        if image.ndim == 3 and image.shape[2] == 3:
            # Check if it's BGR (OpenCV) or RGB
            # Assuming RGB from our processor
            
            # Calculate average color
            avg_color = np.mean(image, axis=(0, 1))
            avg_r, avg_g, avg_b = avg_color
            
            # Determine temperature
            if avg_r > avg_g > avg_b:
                temp = "warm"
            elif avg_b > avg_g > avg_r:
                temp = "cool"
            else:
                temp = "neutral"
            
            # Convert to HSV for saturation and brightness
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            avg_saturation = np.mean(hsv[:, :, 1]) / 255.0
            avg_value = np.mean(hsv[:, :, 2])
            
            # Get dominant colors using K-means
            dominant_colors = self._extract_dominant_colors(image, k=5)
            
            self.palette = ColorPalette(
                dominant_colors=dominant_colors,
                percentages=[20.0] * len(dominant_colors),
                temperature=temp,
                saturation=avg_saturation,
                brightness=avg_value
            )
            
            logger.debug(f"Color analysis: temp={temp}, sat={avg_saturation:.2f}, bright={avg_value:.1f}")
            
            return self.palette
        
        return None
    
    def _extract_dominant_colors(self, image: np.ndarray, k: int = 5) -> List[Tuple[int, int, int]]:
        """Extract k dominant colors using K-means."""
        # Reshape image for clustering
        pixels = image.reshape(-1, 3)
        
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(
            np.float32(pixels), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )
        
        # Sort by frequency
        unique, counts = np.unique(labels, return_counts=True)
        sorted_indices = np.argsort(-counts)
        
        colors = []
        for idx in sorted_indices:
            center = centers[idx].astype(int)
            colors.append((int(center[0]), int(center[1]), int(center[2])))
        
        return colors
    
    def get_lut_from_palette(self) -> np.ndarray:
        """Generate a LUT from the current palette for Photoshop-style adjustment."""
        if self.palette is None:
            return np.arange(256)
        
        lut = np.zeros(256, dtype=np.uint8)
        
        for i in range(256):
            # Find closest dominant color
            closest_idx = 0
            min_dist = float('inf')
            
            for idx, color in enumerate(self.palette.dominant_colors[:3]):
                # Map current intensity to color
                target_val = int(color[idx % 3] * (i / 128.0))
                dist = abs(target_val - i)
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = idx
            
            # Apply color tint based on dominant colors
            base_color = self.palette.dominant_colors[closest_idx]
            factor = i / 255.0
            
            if closest_idx == 0:  # Most dominant
                r = int(base_color[0] * factor + i * (1 - factor))
                g = int(base_color[1] * factor + i * (1 - factor))
                b = int(base_color[2] * factor + i * (1 - factor))
            else:
                r = int(base_color[0] * factor + i * (1 - factor * 0.5))
                g = int(base_color[1] * factor + i * (1 - factor * 0.5))
                b = int(base_color[2] * factor + i * (1 - factor * 0.5))
            
            lut[i] = np.clip(r, 0, 255)
        
        return lut


class ColorTransfer:
    """Transfer color characteristics from one image to another."""
    
    def __init__(self):
        self.analyzer = ColorAnalyzer()
        self.settings = ColorTransferSettings()
        self.source_palette: ColorPalette = None
    
    def learn_from_image(self, image: np.ndarray) -> ColorPalette:
        """
        Learn color characteristics from a source image.
        
        Args:
            image: Reference image (RGB)
            
        Returns:
            ColorPalette extracted from the image
        """
        self.source_palette = self.analyzer.analyze(image)
        return self.source_palette
    
    def apply_to(self, target_image: np.ndarray) -> np.ndarray:
        """
        Apply learned color characteristics to target image.
        
        Args:
            target_image: Image to apply colors to (RGB)
            
        Returns:
            Color-adjusted image
        """
        if self.source_palette is None:
            logger.warning("No source palette. Run learn_from_image first.")
            return target_image
        
        result = target_image.copy()
        
        # Match luminance
        if self.settings.match_luminance:
            result = self._match_luminance(result)
        
        # Apply temperature shift
        if self.settings.temperature_match:
            result = self._apply_temperature_shift(result)
        
        # Apply saturation adjustment
        if self.settings.saturation_strength != 1.0:
            result = self._adjust_saturation(result)
        
        # Apply palette-based color transfer
        if self.settings.palette_match:
            result = self._apply_palette_colors(result)
        
        return result
    
    def _match_luminance(self, image: np.ndarray) -> np.ndarray:
        """Match luminance with source."""
        if self.source_palette is None:
            return image
        
        # Calculate luminance from dominant color
        weights = np.array([0.299, 0.587, 0.114])
        dominant = np.array(self.source_palette.dominant_colors[0])
        source_lum = np.dot(weights, dominant)
        source_lum = float(min(200, max(55, source_lum)))
        
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        target_lum = float(np.mean(hsv[:, :, 2]))
        
        # Adjust value
        if target_lum > 0:
            ratio = source_lum / target_lum
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * ratio, 0, 255)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    def _apply_temperature_shift(self, image: np.ndarray) -> np.ndarray:
        """Apply temperature (warm/cool) shift."""
        if self.source_palette is None:
            return image
        
        temp = self.source_palette.temperature
        
        if temp == "warm":
            # Add yellow/orange tint
            image = image.astype(np.float32)
            image[:, :, 0] = np.clip(image[:, :, 0] * 1.05, 0, 255)  # R
            image[:, :, 1] = np.clip(image[:, :, 1] * 1.02, 0, 255)  # G
            image[:, :, 2] = np.clip(image[:, :, 2] * 0.95, 0, 255)  # B
            return image.astype(np.uint8)
        
        elif temp == "cool":
            # Add blue tint
            image = image.astype(np.float32)
            image[:, :, 0] = np.clip(image[:, :, 0] * 0.95, 0, 255)  # R
            image[:, :, 1] = np.clip(image[:, :, 1] * 0.98, 0, 255)  # G
            image[:, :, 2] = np.clip(image[:, :, 2] * 1.05, 0, 255)  # B
            return image.astype(np.uint8)
        
        return image
    
    def _adjust_saturation(self, image: np.ndarray) -> np.ndarray:
        """Adjust saturation."""
        if self.source_palette is None:
            return image
        
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        target_sat = np.mean(hsv[:, :, 1])
        source_sat = self.source_palette.saturation * 255
        
        if target_sat > 0:
            ratio = source_sat / target_sat
            ratio = 1 + (ratio - 1) * self.settings.saturation_strength
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * ratio, 0, 255)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    
    def _apply_palette_colors(self, image: np.ndarray) -> np.ndarray:
        """Apply dominant colors from palette."""
        if self.source_palette is None:
            return image
        
        # Use dominant color to tint
        dominant = self.source_palette.dominant_colors[0]
        
        # Calculate blend factor based on average brightness
        avg_brightness = np.mean(image)
        blend = (avg_brightness / 255.0) * 0.15
        
        image = image.astype(np.float32)
        
        # Blend each channel with dominant color
        image[:, :, 0] = image[:, :, 0] * (1 - blend) + dominant[0] * blend
        image[:, :, 1] = image[:, :, 1] * (1 - blend) + dominant[1] * blend
        image[:, :, 2] = image[:, :, 2] * (1 - blend) + dominant[2] * blend
        
        return np.clip(image, 0, 255).astype(np.uint8)
    
    def get_palette_info(self) -> str:
        """Get formatted palette information."""
        if self.source_palette is None:
            return "No palette loaded"
        
        info = []
        info.append(f"Temperature: {self.source_palette.temperature}")
        info.append(f"Saturation: {self.source_palette.saturation:.1%}")
        info.append(f"Brightness: {self.source_palette.brightness:.1f}")
        info.append("Dominant Colors:")
        for i, color in enumerate(self.source_palette.dominant_colors[:3]):
            info.append(f"  {i+1}. RGB({color[0]}, {color[1]}, {color[2]})")
        
        return "\n".join(info)
