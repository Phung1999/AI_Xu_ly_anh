"""
Tests for Chibi transformation module.
"""

import numpy as np
import pytest
from src.ai.chibi import ChibiTransformer, ChibiSettings, FaceDetector


class TestChibiSettings:
    """Test ChibiSettings."""
    
    def test_default_settings(self):
        settings = ChibiSettings()
        assert settings.eye_scale == 1.8
        assert settings.eye_brightness == 1.3
        assert settings.face_roundness == 0.3
        assert settings.cheeks_enabled is True
        assert settings.simplify_features is True
        assert settings.output_size == (512, 512)
    
    def test_custom_settings(self):
        settings = ChibiSettings(eye_scale=2.0, cheeks_enabled=False)
        assert settings.eye_scale == 2.0
        assert settings.cheeks_enabled is False
    
    def test_validate_valid(self):
        settings = ChibiSettings(eye_scale=1.5, face_roundness=0.5)
        assert settings.validate() is True
    
    def test_validate_invalid_scale(self):
        settings = ChibiSettings(eye_scale=0.1)
        assert settings.validate() is False
    
    def test_validate_invalid_roundness(self):
        settings = ChibiSettings(face_roundness=1.5)
        assert settings.validate() is False


class TestFaceDetector:
    """Test FaceDetector."""
    
    def test_init(self):
        detector = FaceDetector()
        assert detector.face_cascade is not None
        assert detector.eye_cascade is not None
    
    def test_detect_faces_empty(self):
        detector = FaceDetector()
        empty_image = np.zeros((100, 100, 3), dtype=np.uint8)
        results = detector.detect_faces(empty_image)
        assert isinstance(results, list)
    
    def test_detect_faces_none(self):
        detector = FaceDetector()
        results = detector.detect_faces(None)
        assert results == []
    
    def test_get_face_center(self):
        detector = FaceDetector()
        from src.ai.chibi import FaceLandmarks
        landmarks = FaceLandmarks(
            left_eye=(30, 30),
            right_eye=(70, 30),
            nose=(50, 60),
            left_mouth=(35, 80),
            right_mouth=(65, 80),
            chin=(50, 90),
            face_box=(20, 20, 60, 80)
        )
        center = detector.get_face_center(landmarks)
        assert center == (50, 60)
    
    def test_get_eyes_distance(self):
        detector = FaceDetector()
        from src.ai.chibi import FaceLandmarks
        landmarks = FaceLandmarks(
            left_eye=(30, 30),
            right_eye=(70, 30),
            nose=(50, 60),
            left_mouth=(35, 80),
            right_mouth=(65, 80),
            chin=(50, 90),
            face_box=(20, 20, 60, 80)
        )
        distance = detector.get_eyes_distance(landmarks)
        assert distance == 40


class TestChibiTransformer:
    """Test ChibiTransformer."""
    
    def test_init_default(self):
        transformer = ChibiTransformer()
        assert transformer.settings is not None
        assert transformer.face_detector is not None
    
    def test_init_custom_settings(self):
        settings = ChibiSettings(eye_scale=2.0)
        transformer = ChibiTransformer(settings)
        assert transformer.settings.eye_scale == 2.0
    
    def test_transform_empty(self):
        transformer = ChibiTransformer()
        result = transformer.transform(None)
        assert result is None
    
    def test_transform_zero_image(self):
        transformer = ChibiTransformer()
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        result = transformer.transform(image)
        assert result is not None
        assert result.shape[0] > 0
    
    def test_transform_with_settings(self):
        settings = ChibiSettings(output_size=(256, 256))
        transformer = ChibiTransformer(settings)
        image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        result = transformer.transform(image)
        assert result.shape[:2] == (256, 256)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])