"""
Internationalization Module
Multi-language support: English, Vietnamese
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "app_title": "Image Enhancement Studio",
        
        # Menu - File
        "file": "&File",
        "open": "&Open... (Ctrl+O)",
        "save": "&Save (Ctrl+S)",
        "save_as": "Save &As...",
        "exit": "E&xit",
        
        # Menu - Edit
        "edit": "&Edit",
        "reset_all": "&Reset All",
        "auto_enhance": "&Auto Enhance",
        
        # Menu - View
        "view": "&View",
        "zoom_in": "&Zoom In",
        "zoom_out": "Zoom &Out",
        "fit_window": "&Fit to Window",
        
        # Menu - Language
        "language": "&Language",
        "english": "English",
        "vietnamese": "Vietnamese",
        
        # Panels
        "white_balance": "White Balance",
        "temperature": "Temperature",
        "tint": "Tint",
        
        "levels": "Levels",
        "shadows": "Shadows",
        "midtone_gamma": "Midtones (Gamma)",
        "highlights": "Highlights",
        
        "sharpening": "Sharpening",
        "sharpness": "Sharpness",
        
        "local_contrast": "Local Contrast",
        "clip_limit": "Clip Limit",
        
        "presets": "Presets",
        "apply": "Apply",
        
        "batch_processing": "Batch Processing",
        "add_folder": "Add Folder",
        "process_queue": "Process Queue",
        
        "quality_metrics": "Quality Metrics",
        "load_image_quality": "Load an image to see quality metrics",
        
        # Buttons
        "split_view": "Split View",
        "show_original": "Original",
        "current": "Current",
        
        # Status
        "ready": "Ready",
        "adjusting": "Adjusting...",
        "opened": "Opened: {}",
        "saved": "Saved: {}",
        "applied_preset": "Applied preset: {}",
        "reset_adjustments": "Reset all adjustments",
        "auto_enhance_applied": "Auto enhance applied",
        "added_folder": "Added folder: {}",
        "queue_complete": "Queue processing complete",
        
        # Dialogs
        "error": "Error",
        "warning": "Warning",
        "failed_open": "Failed to open image: {}",
        "failed_save": "Failed to save: {}",
        "auto_enhance_failed": "Auto enhance failed: {}",
        "no_image_selected": "No image selected",
        
        # Image viewer
        "drop_image": "Drop image here or click Open",
        
        # Toolbar
        "toolbar_title": "Main Toolbar",
        
        # View modes
        "view_current": "Current",
        "view_original": "Original",
        "view_split": "Split",
        
        # Color Reference Panel
        "color_reference": "Color Reference",
        "reference": "Reference",
        "select_reference": "Select Reference Image",
        "load_reference": "Load Reference",
        "apply_color": "Apply Color",
        "clear_reference": "Clear",
        "reference_loaded": "Reference loaded: {}",
        "reference_loaded_title": "Color Analysis Complete",
        "reference_cleared": "Reference cleared",
        "no_image_to_apply": "No image loaded to apply color",
        "palette_analysis": "Palette Analysis",
        "saturation": "Saturation",
        "brightness": "Brightness",
        "warm": "Warm",
        "cool": "Cool",
        "neutral": "Neutral",
        "dominant_colors": "Dominant Colors",
        "analysis_complete": "Color analysis complete!",
        "color_applied": "Color applied successfully!",

        # Chibi Panel
        "chibi_transform": "Chibi Transform",
        "anime_style": "Anime Style",
        "apply_chibi": "Apply Chibi",
        "chibi_applied": "Chibi transformation applied!",
    },
    
    "vi": {
        "app_title": "Phần Mềm Nâng Cấp Ảnh",
        
        # Menu - File
        "file": "&Tệp",
        "open": "&Mở... (Ctrl+O)",
        "save": "&Lưu (Ctrl+S)",
        "save_as": "Lưu &Như...",
        "exit": "T&hoát",
        
        # Menu - Edit
        "edit": "&Sửa",
        "reset_all": "&Đặt Lại Tất Cả",
        "auto_enhance": "Tự &Động Nâng Cấp",
        
        # Menu - View
        "view": "&Hiển Thị",
        "zoom_in": "Phóng &To",
        "zoom_out": "Thu &Nhỏ",
        "fit_window": "&Co Vừa Cửa Sổ",
        
        # Menu - Language
        "language": "&Ngôn Ngữ",
        "english": "Tiếng Anh",
        "vietnamese": "Tiếng Việt",
        
        # Panels
        "white_balance": "Cân Bằng Trắng",
        "temperature": "Nhiệt Độ",
        "tint": "Sắc Độ",
        
        "levels": "Mức",
        "shadows": "Bóng Tối",
        "midtone_gamma": "Tông Trung",
        "highlights": "Vùng Sáng",
        
        "sharpening": "Tăng Nét",
        "sharpness": "Độ Nét",
        
        "local_contrast": "Tương Phản Cục Bộ",
        "clip_limit": "Giới Hạn Cắt",
        
        "presets": "Cài Đặt Sẵn",
        "apply": "Áp Dụng",
        
        "batch_processing": "Xử Lý Hàng Loạt",
        "add_folder": "Thêm Thư Mục",
        "process_queue": "Xử Lý Hàng Đợi",
        
        "quality_metrics": "Chỉ Số Chất Lượng",
        "load_image_quality": "Mở ảnh để xem chỉ số",
        
        # Buttons
        "split_view": "Chia Màn",
        "show_original": "Ảnh Gốc",
        "current": "Hiện Tại",
        
        # Status
        "ready": "Sẵn Sàng",
        "adjusting": "Đang điều chỉnh...",
        "opened": "Đã mở: {}",
        "saved": "Đã lưu: {}",
        "applied_preset": "Đã áp dụng: {}",
        "reset_adjustments": "Đã đặt lại tất cả",
        "auto_enhance_applied": "Đã tự động nâng cấp",
        "added_folder": "Đã thêm thư mục: {}",
        "queue_complete": "Xử lý hàng đợi hoàn tất",
        
        # Dialogs
        "error": "Lỗi",
        "warning": "Cảnh Báo",
        "failed_open": "Không thể mở ảnh: {}",
        "failed_save": "Không thể lưu: {}",
        "auto_enhance_failed": "Tự động nâng cấp thất bại: {}",
        "no_image_selected": "Chưa chọn ảnh",
        
        # Image viewer
        "drop_image": "Kéo ảnh vào đây hoặc click Mở",
        
        # Toolbar
        "toolbar_title": "Thanh Công Cụ",
        
        # View modes
        "view_current": "Hiện Tại",
        "view_original": "Ảnh Gốc",
        "view_split": "Chia Màn",
        
        # Color Reference Panel
        "color_reference": "Màu Tham Chiếu",
        "reference": "Tham Chiếu",
        "select_reference": "Chọn Ảnh Tham Chiếu",
        "load_reference": "Tải Ảnh Tham Chiếu",
        "apply_color": "Áp Dụng Màu",
        "clear_reference": "Xóa",
        "reference_loaded": "Đã tải tham chiếu: {}",
        "reference_loaded_title": "Phân Tích Màu Hoàn Tất",
        "reference_cleared": "Đã xóa tham chiếu",
        "no_image_to_apply": "Chưa có ảnh để áp dụng màu",
        "palette_analysis": "Phân Tích Bảng Màu",
        "saturation": "Độ Bão Hòa",
        "brightness": "Độ Sáng",
        "warm": "Ấm",
        "cool": "Lạnh",
        "neutral": "Trung Tính",
        "dominant_colors": "Màu Chủ Đạo",
        "analysis_complete": "Phân tích màu hoàn tất!",
        "color_applied": "Áp dụng màu thành công!",

        # Chibi Panel
        "chibi_transform": "Biến Đổi Chibi",
        "anime_style": "Phong Cách Anime",
        "apply_chibi": "Áp Dụng Chibi",
        "chibi_applied": "Đã biến đổi Chibi!",
    }
}


class I18n:
    _current_language = "en"
    
    @classmethod
    def set_language(cls, lang: str):
        if lang in TRANSLATIONS:
            cls._current_language = lang
    
    @classmethod
    def get_language(cls) -> str:
        return cls._current_language
    
    @classmethod
    def t(cls, key: str, *args) -> str:
        text = TRANSLATIONS.get(cls._current_language, {}).get(
            key, 
            TRANSLATIONS["en"].get(key, key)
        )
        if args:
            return text.format(*args)
        return text


def t(key: str, *args) -> str:
    return I18n.t(key, *args)
