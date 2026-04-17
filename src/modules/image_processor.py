"""
Core Image Processor Module
Foundation Phase - Task 1.2

Provides basic image loading, saving, and manipulation capabilities.
Uses OpenCV (cv2) as the primary image processing library.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Union, Dict, Optional, Tuple
from loguru import logger


class ImageLoader:
    """
    Handles image loading from various formats.

    Supported formats: PNG, JPG, JPEG, BMP, TIFF, WEBP
    """

    SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}

    def __init__(self):
        logger.debug("ImageLoader initialized")

    def load(self, path: Union[str, Path]) -> np.ndarray:
        """
        Load an image from file path.

        Args:
            path: Path to image file (str or Path object)

        Returns:
            numpy.ndarray: Loaded image in RGB format

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If format is not supported
        """
        import os
        
        path = Path(path)
        path_str = os.fspath(path)

        if not Path(path_str).exists():
            logger.error(f"File not found: {path_str}")
            raise FileNotFoundError(f"Image file not found: {path_str}")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            logger.error(f"Unsupported format: {path.suffix}")
            raise ValueError(f"Unsupported image format: {path.suffix}")

        logger.info(f"Loading image: {path_str}")

        # Use numpy to read file bytes (handles Unicode paths on Windows)
        file_bytes = np.fromfile(path_str, dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            logger.error(f"Failed to load image: {path_str}")
            raise ValueError(f"Could not load image: {path_str}")

        # Convert BGR to RGB for consistent processing
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        logger.debug(f"Image loaded: shape={img_rgb.shape}")

        return img_rgb

    def get_info(self, path: Union[str, Path]) -> Dict[str, any]:
        """
        Get image metadata without loading full image.

        Args:
            path: Path to image file

        Returns:
            Dict containing width, height, channels, dtype
        """
        import os
        path = Path(path)
        path_str = os.fspath(path)
        
        file_bytes = np.fromfile(path_str, dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError(f"Could not read image info: {path_str}")

        return {
            "width": img.shape[1],
            "height": img.shape[0],
            "channels": img.shape[2] if len(img.shape) > 2 else 1,
            "dtype": str(img.dtype),
            "format": path.suffix.lower(),
            "size_bytes": Path(path).stat().st_size,
        }

    def save(self, image: np.ndarray, path: Union[str, Path], quality: int = 95) -> None:
        """
        Save an image to file.

        Args:
            image: Image array (RGB format)
            path: Output path
            quality: JPEG quality (1-100)
        """
        import os
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        path_str = os.fspath(path)

        # Convert RGB to BGR for OpenCV
        img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        logger.info(f"Saving image: {path}")

        if path.suffix.lower() in {".jpg", ".jpeg"}:
            result, encoded = cv2.imencode('.jpg', img_bgr, [cv2.IMWRITE_JPEG_QUALITY, quality])
            if result:
                encoded.tofile(path_str)
        elif path.suffix.lower() == ".png":
            result, encoded = cv2.imencode('.png', img_bgr, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            if result:
                encoded.tofile(path_str)
        else:
            result, encoded = cv2.imencode(path.suffix, img_bgr)
            if result:
                encoded.tofile(path_str)

        logger.debug(f"Image saved: {path}")


class ImageProcessor:
    """
    Core image processor with basic manipulation capabilities.

    All internal processing uses RGB format.
    """

    def __init__(self):
        self.loader = ImageLoader()
        logger.debug("ImageProcessor initialized")

    def load_image(self, path: Union[str, Path]) -> np.ndarray:
        """
        Load image and convert to RGB.

        Args:
            path: Path to image file

        Returns:
            numpy.ndarray: Image in RGB format
        """
        return self.loader.load(path)

    def save_image(
        self, image: np.ndarray, path: Union[str, Path], quality: int = 95
    ) -> None:
        """
        Save processed image.

        Args:
            image: Image array (RGB format)
            path: Output path
            quality: JPEG quality
        """
        self.loader.save(image, path, quality)

    def _validate_image(self, image: np.ndarray) -> bool:
        """
        Validate image array format.

        Args:
            image: Image array to validate

        Returns:
            bool: True if valid
        """
        if not isinstance(image, np.ndarray):
            logger.error("Image must be numpy array")
            return False

        if image.size == 0:
            logger.error("Image array is empty")
            return False

        if len(image.shape) == 2:
            logger.warning("Grayscale image detected, will convert to RGB")
            return True

        if len(image.shape) != 3 or image.shape[2] not in [3, 4]:
            logger.error(f"Invalid image shape: {image.shape}")
            return False

        if image.dtype != np.uint8:
            logger.warning(f"Image dtype {image.dtype} converted to uint8")
            return True

        return True

    def _ensure_rgb(self, image: np.ndarray) -> np.ndarray:
        """
        Ensure image is in RGB format.

        Args:
            image: Input image (RGB or RGBA)

        Returns:
            numpy.ndarray: RGB image
        """
        if len(image.shape) == 2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        if image.shape[2] == 4:
            return cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        return image

    def _ensure_bgr(self, image: np.ndarray) -> np.ndarray:
        """
        Ensure image is in BGR format for OpenCV operations.

        Args:
            image: Input image (RGB)

        Returns:
            numpy.ndarray: BGR image
        """
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    def resize(
        self, image: np.ndarray, width: Optional[int] = None, height: Optional[int] = None, scale: Optional[float] = None
    ) -> np.ndarray:
        """
        Resize image by dimensions or scale factor.

        Args:
            image: Input image
            width: Target width (None to calculate from height)
            height: Target height (None to calculate from width)
            scale: Scale factor (overrides width/height if set)

        Returns:
            numpy.ndarray: Resized image
        """
        h, w = image.shape[:2]

        if scale is not None:
            new_w, new_h = int(w * scale), int(h * scale)
        elif width is not None and height is not None:
            new_w, new_h = width, height
        elif width is not None:
            new_w, new_h = width, int(h * width / w)
        elif height is not None:
            new_w, new_h = int(w * height / h), height
        else:
            logger.warning("No resize parameters provided, returning original")
            return image

        img_bgr = self._ensure_bgr(image)
        resized = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        return cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    def crop(
        self, image: np.ndarray, x: int, y: int, width: int, height: int
    ) -> np.ndarray:
        """
        Crop a region from the image.

        Args:
            image: Input image
            x: Left coordinate
            y: Top coordinate
            width: Crop width
            height: Crop height

        Returns:
            numpy.ndarray: Cropped image
        """
        h, w = image.shape[:2]

        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))
        width = min(width, w - x)
        height = min(height, h - y)

        return image[y : y + height, x : x + width]

    def rotate(
        self, image: np.ndarray, angle: float, keep_size: bool = False
    ) -> np.ndarray:
        """
        Rotate image by angle.

        Args:
            image: Input image
            angle: Rotation angle in degrees (positive = counter-clockwise)
            keep_size: If True, crop to original size after rotation

        Returns:
            numpy.ndarray: Rotated image
        """
        h, w = image.shape[:2]
        center = (w // 2, h // 2)

        img_bgr = self._ensure_bgr(image)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        if keep_size:
            rotated = cv2.warpAffine(img_bgr, matrix, (w, h))
        else:
            # Calculate new bounding box
            cos = np.abs(matrix[0, 0])
            sin = np.abs(matrix[0, 1])
            new_w = int(h * sin + w * cos)
            new_h = int(h * cos + w * sin)
            matrix[0, 2] += new_w / 2 - center[0]
            matrix[1, 2] += new_h / 2 - center[1]
            rotated = cv2.warpAffine(img_bgr, matrix, (new_w, new_h))

        return cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)

    def flip(self, image: np.ndarray, mode: str = "horizontal") -> np.ndarray:
        """
        Flip image.

        Args:
            image: Input image
            mode: 'horizontal', 'vertical', or 'both'

        Returns:
            numpy.ndarray: Flipped image
        """
        flip_codes = {
            "horizontal": 1,
            "vertical": 0,
            "both": -1,
        }

        if mode not in flip_codes:
            raise ValueError(f"Invalid flip mode: {mode}")

        img_bgr = self._ensure_bgr(image)
        flipped = cv2.flip(img_bgr, flip_codes[mode])
        return cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)

    def to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image to grayscale.

        Args:
            image: Input RGB image

        Returns:
            numpy.ndarray: Grayscale image
        """
        img_bgr = self._ensure_bgr(image)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        return gray

    def adjust_brightness(self, image: np.ndarray, factor: float) -> np.ndarray:
        """
        Adjust image brightness.

        Args:
            image: Input image
            factor: Brightness factor (1.0 = no change, >1 = brighter, <1 = darker)

        Returns:
            numpy.ndarray: Brightness-adjusted image
        """
        img_bgr = self._ensure_bgr(image)
        adjusted = np.clip(img_bgr.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)

    def adjust_contrast(self, image: np.ndarray, factor: float) -> np.ndarray:
        """
        Adjust image contrast.

        Args:
            image: Input image
            factor: Contrast factor (1.0 = no change, >1 = more contrast, <1 = less)

        Returns:
            numpy.ndarray: Contrast-adjusted image
        """
        img_bgr = self._ensure_bgr(image)
        mean = img_bgr.mean()
        adjusted = np.clip(
            (img_bgr.astype(np.float32) - mean) * factor + mean, 0, 255
        ).astype(np.uint8)
        return cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)

    def blend(
        self, image1: np.ndarray, image2: np.ndarray, alpha: float = 0.5
    ) -> np.ndarray:
        """
        Blend two images.

        Args:
            image1: First image
            image2: Second image
            alpha: Blend factor (0 = all image1, 1 = all image2)

        Returns:
            numpy.ndarray: Blended image
        """
        if image1.shape != image2.shape:
            # Resize image2 to match image1
            image2 = self.resize(image2, width=image1.shape[1], height=image1.shape[0])

        img1_bgr = self._ensure_bgr(image1)
        img2_bgr = self._ensure_bgr(image2)

        blended = cv2.addWeighted(img1_bgr, alpha, img2_bgr, 1 - alpha, 0)
        return cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)
