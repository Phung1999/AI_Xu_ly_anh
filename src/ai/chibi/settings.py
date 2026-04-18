"""
Chibi Settings - Cấu hình cho transformation
Giữ nguyên dataclass pattern như EnhancementSettings
"""

from dataclasses import dataclass


@dataclass
class ChibiSettings:
    """Cấu hình Chibi transformation - dễ extend."""
    
    # Eye transformation
    eye_scale: float = 1.8  # 1.0 = original, 1.8 = +80%
    eye_brightness: float = 1.3  # Làm sáng mắt
    
    # Face transformation  
    face_roundness: float = 0.3  # 0-1 độ tròn
    chin_reduction: float = 0.3  # 0-1 thu nhỏ cằm
    
    # Features
    cheeks_enabled: bool = True  # Thêm má hồng
    simplify_features: bool = True  # Đơn giản hóa
    
    # Output
    output_size: tuple = (512, 512)
    preserve_color: bool = True
    
    def validate(self) -> bool:
        return 0.5 <= self.eye_scale <= 3.0 and 0.0 <= self.face_roundness <= 1.0