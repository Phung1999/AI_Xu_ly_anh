"""
Face Detector - Phát hiện khuôn mặt
Dùng OpenCV Haar Cascade (nhẹ, nhanh)
"""

import numpy as np
import cv2
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class FaceLandmarks:
    """Facial landmarks data."""
    left_eye: Tuple[int, int]
    right_eye: Tuple[int, int]
    nose: Tuple[int, int]
    left_mouth: Tuple[int, int]
    right_mouth: Tuple[int, int]
    chin: Tuple[int, int]
    face_box: Tuple[int, int, int, int]  # x, y, w, h


class FaceDetector:
    """
    Face detection sử dụng Haar Cascade.
    Nhẹ, nhanh, không cần ML model nặng.
    """
    
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
        self._load_cascades()
    
    def _load_cascades(self):
        """Load Haar cascade files."""
        # OpenCV chứa sẵn cascade files
        cv_path = cv2.data.haarcascades
        
        self.face_cascade = cv2.CascadeClassifier(
            cv_path + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv_path + 'haarcascade_eye.xml'
        )
        
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade")
    
    def detect_faces(self, image: np.ndarray) -> List[FaceLandmarks]:
        """
        Phát hiện tất cả khuôn mặt trong ảnh.
        
        Args:
            image: Ảnh RGB numpy array
            
        Returns:
            List of FaceLandmarks
        """
        if image is None or image.size == 0:
            return []
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        landmarks_list = []
        for (x, y, w, h) in faces:
            landmarks = self._extract_landmarks(image, gray, (x, y, w, h))
            if landmarks:
                landmarks_list.append(landmarks)
        
        return landmarks_list
    
    def _extract_landmarks(self, image: np.ndarray, gray: np.ndarray, 
                          face_box: Tuple[int, int, int, int]) -> Optional[FaceLandmarks]:
        """Trích xuất landmarks từ face region."""
        x, y, w, h = face_box
        
        # Face region
        face_roi = gray[y:y+h, x:x+w]
        
        # Detect eyes
        eyes = self.eye_cascade.detectMultiScale(
            face_roi, 
            scaleFactor=1.1, 
            minNeighbors=3,
            minSize=(10, 10)
        )
        
        if len(eyes) < 2:
            # Fallback: estimate from face proportions
            return self._estimate_landmarks(x, y, w, h)
        
        # Sort eyes by x position
        eyes = sorted(eyes, key=lambda e: e[0])
        
        left_eye = (int(x + eyes[0][0] + eyes[0][2]//2), 
                    int(y + eyes[0][1] + eyes[0][3]//2))
        right_eye = (int(x + eyes[1][0] + eyes[1][2]//2), 
                     int(y + eyes[1][1] + eyes[1][3]//2))
        
        # Estimate other landmarks from face proportions
        nose = (int(x + w//2), int(y + h*0.6))
        chin = (int(x + w//2), int(y + h*0.9))
        
        mouth_y = int(y + h*0.75)
        left_mouth = (int(x + w*0.3), mouth_y)
        right_mouth = (int(x + w*0.7), mouth_y)
        
        return FaceLandmarks(
            left_eye=left_eye,
            right_eye=right_eye,
            nose=nose,
            left_mouth=left_mouth,
            right_mouth=right_mouth,
            chin=chin,
            face_box=face_box
        )
    
    def _estimate_landmarks(self, x: int, y: int, w: int, h: int) -> FaceLandmarks:
        """Estimate landmarks khi không detect được eyes."""
        # Standard face proportions (anime/chibi style)
        eye_y = int(y + h * 0.35)
        left_eye = (int(x + w * 0.3), eye_y)
        right_eye = (int(x + w * 0.7), eye_y)
        
        nose = (int(x + w * 0.5), int(y + h * 0.55))
        chin = (int(x + w * 0.5), int(y + h * 0.9))
        
        mouth_y = int(y + h * 0.7)
        left_mouth = (int(x + w * 0.35), mouth_y)
        right_mouth = (int(x + w * 0.65), mouth_y)
        
        return FaceLandmarks(
            left_eye=left_eye,
            right_eye=right_eye,
            nose=nose,
            left_mouth=left_mouth,
            right_mouth=right_mouth,
            chin=chin,
            face_box=(x, y, w, h)
        )
    
    def get_face_center(self, landmarks: FaceLandmarks) -> Tuple[int, int]:
        """Lấy tọa độ tâm mặt."""
        x, y, w, h = landmarks.face_box
        return (int(x + w//2), int(y + h//2))
    
    def get_eyes_distance(self, landmarks: FaceLandmarks) -> int:
        """Khoảng cách giữa hai mắt."""
        dx = landmarks.right_eye[0] - landmarks.left_eye[0]
        dy = landmarks.right_eye[1] - landmarks.left_eye[1]
        return int(np.sqrt(dx*dx + dy*dy))