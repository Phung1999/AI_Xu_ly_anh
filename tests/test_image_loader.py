"""
Test suite for ImageLoader - Core Image Engine
TDD: Tests written BEFORE implementation

Run: pytest tests/test_image_loader.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestImageLoader:
    """Test suite for ImageLoader class"""

    def test_loader_initialization(self):
        """Test ImageLoader can be initialized"""
        from src.modules.image_processor import ImageLoader

        loader = ImageLoader()
        assert loader is not None

    def test_load_image_from_path_string(self):
        """Test loading image from string path"""
        from src.modules.image_processor import ImageLoader
        import cv2

        loader = ImageLoader()
        dummy_path = "tests/fixtures/test_image.png"
        Path(dummy_path).parent.mkdir(parents=True, exist_ok=True)
        dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(dummy_path, cv2.cvtColor(dummy_img, cv2.COLOR_RGB2BGR))

        img = loader.load(dummy_path)
        assert img is not None
        assert isinstance(img, np.ndarray)
        assert img.shape[0] > 0
        assert img.shape[1] > 0

    def test_load_image_from_pathlib(self):
        """Test loading image from pathlib.Path"""
        from src.modules.image_processor import ImageLoader

        loader = ImageLoader()
        img = loader.load(Path("tests/fixtures/test_image.png"))
        assert img is not None

    def test_load_nonexistent_file_raises_error(self):
        """Test loading nonexistent file raises FileNotFoundError"""
        from src.modules.image_processor import ImageLoader

        loader = ImageLoader()
        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent/path/to/image.png")

    def test_get_image_info(self):
        """Test getting image metadata"""
        from src.modules.image_processor import ImageLoader

        loader = ImageLoader()
        info = loader.get_info("tests/fixtures/test_image.png")

        assert "width" in info
        assert "height" in info
        assert "channels" in info
        assert "dtype" in info

    def test_save_image(self):
        """Test saving processed image"""
        from src.modules.image_processor import ImageLoader
        import cv2

        loader = ImageLoader()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        output_path = "tests/fixtures/output_test.png"
        loader.save(img, output_path)

        assert Path(output_path).exists()


class TestImageProcessor:
    """Test suite for ImageProcessor class"""

    def test_processor_initialization(self):
        """Test ImageProcessor can be initialized"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        assert processor is not None

    def test_load_and_convert_to_rgb(self):
        """Test loading image and converting to RGB"""
        from src.modules.image_processor import ImageProcessor
        import cv2

        processor = ImageProcessor()
        img = processor.load_image("tests/fixtures/test_image.png")

        assert img.shape[2] == 3  # RGB channels


class TestImageValidation:
    """Test suite for image validation"""

    def test_validate_image_array(self):
        """Test image array validation"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()

        valid_img = np.zeros((100, 100, 3), dtype=np.uint8)
        assert processor._validate_image(valid_img) is True

        invalid_img = np.zeros((100, 100, 3), dtype=np.float32)
        assert processor._validate_image(invalid_img) is True

    def test_validate_image_shape(self):
        """Test image shape validation"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()

        valid_img = np.zeros((100, 100, 3), dtype=np.uint8)
        assert processor._validate_image(valid_img) is True

        gray_img = np.zeros((100, 100), dtype=np.uint8)
        result = processor._validate_image(gray_img)
        assert result is True


class TestImageOperations:
    """Test suite for basic image operations"""

    def test_resize_by_width(self):
        """Test resizing by width"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        resized = processor.resize(img, width=50)
        assert resized.shape[1] == 50
        assert resized.shape[0] == 50

    def test_resize_by_scale(self):
        """Test resizing by scale factor"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)

        resized = processor.resize(img, scale=2.0)
        assert resized.shape[0] == 200
        assert resized.shape[1] == 200

    def test_crop(self):
        """Test cropping image"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255

        cropped = processor.crop(img, x=10, y=10, width=50, height=50)
        assert cropped.shape[0] == 50
        assert cropped.shape[1] == 50

    def test_flip_horizontal(self):
        """Test horizontal flip"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :50, :] = 255

        flipped = processor.flip(img, "horizontal")
        assert np.all(flipped[:, :50, :] == 0)
        assert np.all(flipped[:, 50:, :] == 255)

    def test_adjust_brightness(self):
        """Test brightness adjustment"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.ones((10, 10, 3), dtype=np.uint8) * 100

        bright = processor.adjust_brightness(img, 2.0)
        assert np.all(bright >= 200)

    def test_adjust_contrast(self):
        """Test contrast adjustment"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.ones((10, 10, 3), dtype=np.uint8) * 128

        contrasted = processor.adjust_contrast(img, 1.5)
        assert contrasted.dtype == np.uint8

    def test_to_grayscale(self):
        """Test RGB to grayscale conversion"""
        from src.modules.image_processor import ImageProcessor

        processor = ImageProcessor()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 255

        gray = processor.to_grayscale(img)
        assert len(gray.shape) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
