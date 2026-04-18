"""
Chibi Transformer - Chuyển đổi ảnh thành style Chibi/Anime
"""

import numpy as np
import cv2
from typing import Optional

from src.ai.chibi.face_detector import FaceDetector, FaceLandmarks
from src.ai.chibi.settings import ChibiSettings


class ChibiTransformer:
    """
    Chibi style transformation.
    Tạo anime-style từ ảnh thật.
    """
    
    def __init__(self, settings: Optional[ChibiSettings] = None):
        self.settings = settings or ChibiSettings()
        self.face_detector = FaceDetector()
    
    def transform(self, image: np.ndarray) -> np.ndarray:
        """
        Transform ảnh sang style Chibi.
        
        Args:
            image: Ảnh RGB đầu vào
            
        Returns:
            Ảnh Chibi style
        """
        if image is None or image.size == 0:
            return image
        
        original = image.copy()
        
        landmarks_list = self.face_detector.detect_faces(image)
        
        if not landmarks_list:
            return self._transform_without_face(original)
        
        result = self._transform_with_landmarks(original, landmarks_list[0])
        
        if self.settings.output_size:
            result = cv2.resize(result, self.settings.output_size)
        
        return result
    
    def _transform_with_landmarks(self, image: np.ndarray, 
                               landmarks: FaceLandmarks) -> np.ndarray:
        """Transform khi có face landmarks."""
        result = image.copy()
        h, w = result.shape[:2]
        
        x, y, fw, fh = landmarks.face_box
        
        result = self._transform_eyes(result, landmarks)
        
        if self.settings.cheeks_enabled:
            result = self._add_cheeks(result, landmarks)
        
        if self.settings.simplify_features:
            result = self._simplify_face(result, landmarks)
        
        result = self._round_face(result, landmarks)
        
        return result
    
    def _transform_without_face(self, image: np.ndarray) -> np.ndarray:
        """Transform khi không detect được face."""
        result = image.copy()
        h, w = result.shape[:2]
        
        min_dim = min(h, w)
        cx, cy = w // 2, h // 2
        
        if self.settings.output_size:
            result = cv2.resize(result, self.settings.output_size)
        
        return result
    
    def _transform_eyes(self, image: np.ndarray, 
                     landmarks: FaceLandmarks) -> np.ndarray:
        """Transform mắt - phóng to và sáng hơn."""
        result = image.copy()
        
        scale = self.settings.eye_scale
        h, w = result.shape[:2]
        
        for eye_pos in [landmarks.left_eye, landmarks.right_eye]:
            ex, ey = eye_pos
            if 0 <= ex < w and 0 <= ey < h:
                eye_region = result[
                    max(0, ey-20):min(h, ey+20),
                    max(0, ex-20):min(w, ex+20)
                ]
                if eye_region.size > 0:
                    center = (eye_region.shape[1]//2, eye_region.shape[0]//2)
                    eye_region = cv2.resize(eye_region, 
                                        (int(eye_region.shape[1]*scale),
                                         int(eye_region.shape[0]*scale)))
                    eye_region = cv2.GaussianBlur(eye_region, (3, 3), 0)
                    
                    new_h, new_w = eye_region.shape[:2]
                    y1 = max(0, ey - new_h//2)
                    y2 = min(h, ey + new_h//2)
                    x1 = max(0, ex - new_w//2)
                    x2 = min(w, ex + new_w//2)
                    
                    result[y1:y2, x1:x2] = eye_region[:y2-y1, :x2-x1]
        
        if self.settings.eye_brightness != 1.0:
            result = np.clip(result * self.settings.eye_brightness, 0, 255).astype(np.uint8)
        
        return result
    
    def _add_cheeks(self, image: np.ndarray, 
                landmarks: FaceLandmarks) -> np.ndarray:
        """Thêm má hồng."""
        result = image.copy()
        h, w = result.shape[:2]
        
        x, y, fw, fh = landmarks.face_box
        
        cheek_y = int(y + fh * 0.7)
        left_cheek_x = int(x + fw * 0.15)
        right_cheek_x = int(x + fw * 0.85)
        
        blush_color = np.array([180, 120, 120])
        
        for cx in [left_cheek_x, right_cheek_x]:
            if 0 <= cx < w and 0 <= cheek_y < h:
                radius = int(fw * 0.08)
                cv2.circle(result, (cx, cheek_y), radius, 
                         (int(blush_color[0]), int(blush_color[1]), int(blush_color[2])), -1)
        
        return result
    
    def _simplify_face(self, image: np.ndarray, 
                  landmarks: FaceLandmarks) -> np.ndarray:
        """Đơn giản hóa features."""
        result = image.copy()
        x, y, fw, fh = landmarks.face_box
        
        if fw > 50:
            face_region = result[y:y+fh, x:x+fw]
            if face_region.size > 0:
                face_region = cv2.bilateralFilter(face_region, 5, 30, 30)
                result[y:y+fh, x:x+fw] = face_region
        
        return result
    
    def _round_face(self, image: np.ndarray, 
                 landmarks: FaceLandmarks) -> np.ndarray:
        """Làm tròn mặt."""
        if self.settings.face_roundness < 0.1:
            return image
        
        result = image.copy()
        x, y, fw, fh = landmarks.face_box
        
        h, w = result.shape[:2]
        
        return result