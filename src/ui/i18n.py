"""
Internationalization Module
Multi-language support: English, Vietnamese with bilingual labels
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
        
        # Panels - with EN/VI
        "white_balance": "White Balance / Cân Bằng Trắng",
        "temperature": "Temperature / Nhiệt Độ",
        "tint": "Tint / Sắc Độ",
        
        "levels": "Levels / Mức",
        "shadows": "Shadows / Bóng Tối",
        "midtone_gamma": "Midtones (Gamma) / Tông Trung",
        "highlights": "Highlights / Vùng Sáng",
        
        "sharpening": "Sharpening / Tăng Nét",
        "sharpness": "Sharpness / Độ Nét",
        
        "local_contrast": "Local Contrast / Tương Phản Cục Bộ",
        "clip_limit": "Clip Limit / Giới Hạn Cắt",
        
        "presets": "Presets / Cài Đặt Sẵn",
        "apply": "Apply / Áp Dụng",
        
        "batch_processing": "Batch Processing / Xử Lý Hàng Loạt",
        "add_folder": "Add Folder / Thêm Thư Mục",
        "process_queue": "Process Queue / Xử Lý Hàng Đợi",
        
        "quality_metrics": "Quality Metrics / Chỉ Số Chất Lượng",
        "load_image_quality": "Load an image to see quality metrics / Mở ảnh để xem chỉ số",
        
        # Buttons
        "split_view": "Split View / Chia Màn",
        "show_original": "Original / Ảnh Gốc",
        "current": "Current / Hiện Tại",
        
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
        "drop_image": "Drop image here or click Open\nKéo ảnh vào đây hoặc click Mở",
        
        # Toolbar
        "toolbar_title": "Main Toolbar",
        
        # View modes
        "view_current": "Current",
        "view_original": "Original",
        "view_split": "Split",
        
        # Color Reference Panel
        "color_reference": "Color Reference / Màu Tham Chiếu",
        "select_reference": "Select Reference / Chọn Ảnh Tham Chiếu",
        "load_reference": "Load Reference / Tải Ảnh Tham Chiếu",
        "apply_color": "Apply Color / Áp Dụng Màu",
        "clear_reference": "Clear / Xóa",
        "reference_loaded": "Reference loaded: {}",
        "reference_loaded_title": "Color Analysis Complete",
        "reference_cleared": "Reference cleared",
        "no_image_to_apply": "No image loaded to apply color",
        "palette_analysis": "Palette Analysis / Phân Tích Bảng Màu",
        "temperature": "Temperature / Nhiệt Độ",
        "saturation": "Saturation / Độ Bão Hòa",
        "brightness": "Brightness / Độ Sáng",
        "warm": "Warm / Ấm",
        "cool": "Cool / Lạnh",
        "neutral": "Neutral / Trung Tính",
        "dominant_colors": "Dominant Colors / Màu Chủ Đạo",
        "analysis_complete": "Color analysis complete!",
        "color_applied": "Color applied successfully!",
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
        
        # Panels - with EN/VI
        "white_balance": "White Balance / Cân Bằng Trắng",
        "temperature": "Temperature / Nhiệt Độ",
        "tint": "Tint / Sắc Độ",
        
        "levels": "Levels / Mức",
        "shadows": "Shadows / Bóng Tối",
        "midtone_gamma": "Midtones (Gamma) / Tông Trung",
        "highlights": "Highlights / Vùng Sáng",
        
        "sharpening": "Sharpening / Tăng Nét",
        "sharpness": "Sharpness / Độ Nét",
        
        "local_contrast": "Local Contrast / Tương Phản Cục Bộ",
        "clip_limit": "Clip Limit / Giới Hạn Cắt",
        
        "presets": "Presets / Cài Đặt Sẵn",
        "apply": "Apply / Áp Dụng",
        
        "batch_processing": "Batch Processing / Xử Lý Hàng Loạt",
        "add_folder": "Add Folder / Thêm Thư Mục",
        "process_queue": "Process Queue / Xử Lý Hàng Đợi",
        
        "quality_metrics": "Quality Metrics / Chỉ Số Chất Lượng",
        "load_image_quality": "Load an image to see quality metrics / Mở ảnh để xem chỉ số",
        
        # Buttons
        "split_view": "Split View / Chia Màn",
        "show_original": "Original / Ảnh Gốc",
        "current": "Current / Hiện Tại",
        
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
        "drop_image": "Drop image here or click Open\nKéo ảnh vào đây hoặc click Mở",
        
        # Toolbar
        "toolbar_title": "Thanh Công Cụ",
        
        # View modes
        "view_current": "Hiện Tại",
        "view_original": "Ảnh Gốc",
        "view_split": "Chia Màn",
        
        # Color Reference Panel
        "color_reference": "Color Reference / Màu Tham Chiếu",
        "select_reference": "Select Reference / Chọn Ảnh Tham Chiếu",
        "load_reference": "Load Reference / Tải Ảnh Tham Chiếu",
        "apply_color": "Apply Color / Áp Dụng Màu",
        "clear_reference": "Clear / Xóa",
        "reference_loaded": "Reference loaded: {}",
        "reference_loaded_title": "Phân Tích Màu Hoàn Tất",
        "reference_cleared": "Đã xóa tham chiếu",
        "no_image_to_apply": "Chưa có ảnh để áp dụng màu",
        "palette_analysis": "Palette Analysis / Phân Tích Bảng Màu",
        "temperature": "Temperature / Nhiệt Độ",
        "saturation": "Saturation / Độ Bão Hòa",
        "brightness": "Brightness / Độ Sáng",
        "warm": "Warm / Ấm",
        "cool": "Cool / Lạnh",
        "neutral": "Neutral / Trung Tính",
        "dominant_colors": "Dominant Colors / Màu Chủ Đạo",
        "analysis_complete": "Phân tích màu hoàn tất!",
        "color_applied": "Áp dụng màu thành công!",
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
