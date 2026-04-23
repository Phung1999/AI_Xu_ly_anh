"""
Main Window - Image Enhancement Studio UI
Professional image editing with Before/After comparison
Multi-language support (EN/VI)
"""

import sys
import os
import numpy as np
from pathlib import Path
from typing import Optional
from loguru import logger

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox,
    QStatusBar, QMenuBar, QMenu, QToolBar,
    QGroupBox, QScrollArea, QListWidget,
    QProgressBar, QSlider, QComboBox,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QImage, QPixmap, QKeySequence

from src.modules.image_processor import ImageProcessor
from src.modules.levels import LevelsAdjustment
from src.modules.white_balance import WhiteBalance
from src.modules.sharpening import HighPassSharpening
from src.modules.clahe import CLAHEProcessor
from src.ai.auto_enhance import AutoEnhancer
from src.ai.enhancement import ImageEnhancer
from src.ai.chibi import ChibiTransformer
from src.modules.iqa import ImageQualityAssessment
from src.modules.preset import PresetManager
from src.modules.queue import ProcessingQueue
from src.modules.color_analyzer import ColorTransfer, ColorAnalyzer
from src.ui.i18n import I18n, t


class CompactSlider(QWidget):
    """Compact labeled slider for image adjustments."""

    valueChanged = pyqtSignal(float)

    def __init__(self, label: str, min_val: float, max_val: float, default: float, parent=None):
        super().__init__(parent)
        self.min_val = min_val
        self.max_val = max_val
        self._label_text = label
        self.setFixedHeight(45)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(8)

        self.label = QLabel(label)
        self.label.setFixedWidth(90)
        self.label.setStyleSheet("font-size: 11px;")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(int(min_val * 10))
        self.slider.setMaximum(int(max_val * 10))
        self.slider.setValue(int(default * 10))
        self.slider.setFixedHeight(16)
        self.slider.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self.slider)

        self.value_label = QLabel(f"{default:.1f}")
        self.value_label.setFixedWidth(40)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.value_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        layout.addWidget(self.value_label)

    def _on_value_changed(self, value: int):
        real_value = value / 10.0
        self.value_label.setText(f"{real_value:.1f}")
        self.valueChanged.emit(real_value)

    def set_value(self, value: float):
        self.slider.setValue(int(value * 10))
        self.value_label.setText(f"{value:.1f}")

    def get_value(self) -> float:
        return self.slider.value() / 10.0

    def update_label(self, text: str):
        self._label_text = text
        self.label.setText(text)


class ImageViewer(QLabel):
    """Custom image viewer widget with drag & drop support."""

    fileDropped = pyqtSignal(str)

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.title = title
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 200)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px dashed #666; background: #2a2a2a; color: #888;")
        self.setText(t("drop_image"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and self._is_image_file(urls[0].toLocalFile()):
                event.acceptProposedAction()
                self.setStyleSheet("border: 2px dashed #0f0; background: #2a3a2a; color: #0f0;")
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        if not self.pixmap():
            self.setStyleSheet("border: 2px dashed #666; background: #2a2a2a; color: #888;")
        else:
            self.setStyleSheet("border: 1px solid #999; background: #2a2a2a;")

    def dropEvent(self, event):
        if not self.pixmap():
            self.setStyleSheet("border: 2px dashed #666; background: #2a2a2a; color: #888;")
        else:
            self.setStyleSheet("border: 1px solid #999; background: #2a2a2a;")
            
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if self._is_image_file(file_path):
                    self.fileDropped.emit(file_path)
                    event.acceptProposedAction()

    def _is_image_file(self, path: str) -> bool:
        ext = Path(path).suffix.lower()
        return ext in {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}

    def set_image(self, image: np.ndarray):
        if image is None:
            return
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled = pixmap.scaled(
            self.size(), Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled)
        self.setStyleSheet("border: 1px solid #999; background: #2a2a2a;")

    def clear(self):
        QLabel.clear(self)
        self.setText(t("drop_image"))
        self.setStyleSheet("border: 2px dashed #666; background: #2a2a2a; color: #888;")


class MainWindow(QMainWindow):
    """Main application window."""

    languageChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(1400, 900)

        self.original_image: Optional[np.ndarray] = None
        self.current_image: Optional[np.ndarray] = None

        self.processor = ImageProcessor()
        self.levels = LevelsAdjustment()
        self.wb = WhiteBalance()
        self.sharp = HighPassSharpening()
        self.clahe = CLAHEProcessor()
        self.auto_enhancer = AutoEnhancer()
        self.enhancer = ImageEnhancer()
        self.iqa = ImageQualityAssessment()
        self.preset_manager = PresetManager()
        self.queue = ProcessingQueue()
        self.color_transfer = ColorTransfer()
        self.color_analyzer = ColorAnalyzer()

        self._adjustments = {
            "temperature": 0, "tint": 0,
            "shadows": 0, "midtones": 1.0, "highlights": 255,
            "sharpness": 0, "clahe_clip": 2.0,
        }

        self._sliders = {}
        self._labels = {}
        self._view_mode = "current"
        self._menu_items = {}
        self._color_reference_path = None
        self._color_reference_image = None

        self._setup_ui()
        self._create_menu()
        self._create_toolbar()
        self._on_view_mode_changed("Current")

        self.languageChanged.connect(self._update_ui_text)

        logger.info("MainWindow initialized")

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)

        main_layout.addWidget(self._create_left_panel())
        main_layout.addWidget(self._create_center_panel())
        main_layout.addWidget(self._create_right_panel())

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(t("ready"))

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _create_left_panel(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(220)
        scroll.setMaximumWidth(250)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(3)
        layout.setContentsMargins(5, 5, 5, 5)

        wb_group = QGroupBox(t("white_balance"))
        wb_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 5px; }")
        self._labels["wb_group"] = wb_group
        wb_layout = QVBoxLayout()
        wb_layout.setSpacing(2)
        wb_layout.setContentsMargins(3, 8, 3, 3)

        self.temp_slider = CompactSlider(t("temperature"), -100, 100, 0)
        self.temp_slider.valueChanged.connect(self._on_adjustment_changed)
        wb_layout.addWidget(self.temp_slider)

        self.tint_slider = CompactSlider(t("tint"), -100, 100, 0)
        self.tint_slider.valueChanged.connect(self._on_adjustment_changed)
        wb_layout.addWidget(self.tint_slider)

        wb_group.setLayout(wb_layout)
        layout.addWidget(wb_group)

        levels_group = QGroupBox(t("levels"))
        levels_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 5px; }")
        self._labels["levels_group"] = levels_group
        levels_layout = QVBoxLayout()
        levels_layout.setSpacing(2)
        levels_layout.setContentsMargins(3, 8, 3, 3)

        self.shadows_slider = CompactSlider(t("shadows"), -50, 50, 0)
        self.shadows_slider.valueChanged.connect(self._on_adjustment_changed)
        levels_layout.addWidget(self.shadows_slider)

        self.midtone_slider = CompactSlider(t("midtone_gamma"), 0.5, 2.0, 1.0)
        self.midtone_slider.valueChanged.connect(self._on_adjustment_changed)
        levels_layout.addWidget(self.midtone_slider)

        self.highlights_slider = CompactSlider(t("highlights"), -50, 50, 0)
        self.highlights_slider.valueChanged.connect(self._on_adjustment_changed)
        levels_layout.addWidget(self.highlights_slider)

        levels_group.setLayout(levels_layout)
        layout.addWidget(levels_group)

        sharpen_group = QGroupBox(t("sharpening"))
        sharpen_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 5px; }")
        self._labels["sharpen_group"] = sharpen_group
        sharpen_layout = QVBoxLayout()
        sharpen_layout.setSpacing(2)
        sharpen_layout.setContentsMargins(3, 8, 3, 3)

        self.sharpness_slider = CompactSlider(t("sharpness"), 0, 2.0, 0)
        self.sharpness_slider.valueChanged.connect(self._on_adjustment_changed)
        sharpen_layout.addWidget(self.sharpness_slider)

        sharpen_group.setLayout(sharpen_layout)
        layout.addWidget(sharpen_group)

        clahe_group = QGroupBox(t("local_contrast"))
        clahe_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 5px; }")
        self._labels["clahe_group"] = clahe_group
        clahe_layout = QVBoxLayout()
        clahe_layout.setSpacing(2)
        clahe_layout.setContentsMargins(3, 8, 3, 3)

        self.clahe_slider = CompactSlider(t("clip_limit"), 1.0, 5.0, 2.0)
        self.clahe_slider.valueChanged.connect(self._on_adjustment_changed)
        clahe_layout.addWidget(self.clahe_slider)

        clahe_group.setLayout(clahe_layout)
        layout.addWidget(clahe_group)

        layout.addStretch()
        scroll.setWidget(widget)
        return scroll

    def _create_center_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        header_layout = QHBoxLayout()
        header_layout.addStretch()

        self.view_combo = QComboBox()
        self.view_combo.addItems(["Current", "Original", "Split"])
        self.view_combo.setFixedWidth(100)
        self.view_combo.currentTextChanged.connect(self._on_view_mode_changed)
        header_layout.addWidget(self.view_combo)

        self.original_btn = QPushButton(t("show_original"))
        self.original_btn.setFixedWidth(100)
        self.original_btn.clicked.connect(self._show_original)
        header_layout.addWidget(self.original_btn)

        layout.addLayout(header_layout)

        self.compare_container = QWidget()
        self.compare_layout = QHBoxLayout(self.compare_container)
        self.compare_layout.setContentsMargins(0, 0, 0, 0)
        self.compare_layout.setSpacing(5)

        self.original_viewer = ImageViewer(t("show_original"))
        self.current_viewer = ImageViewer(t("current"))

        self.original_viewer.fileDropped.connect(self._on_file_dropped)
        self.current_viewer.fileDropped.connect(self._on_file_dropped)

        self.compare_layout.addWidget(self.original_viewer)
        self.compare_layout.addWidget(self.current_viewer)
        self.compare_layout.setStretch(0, 1)
        self.compare_layout.setStretch(1, 1)

        self.single_viewer = ImageViewer()
        self.single_viewer.fileDropped.connect(self._on_file_dropped)

        layout.addWidget(self.compare_container)
        layout.addWidget(self.single_viewer)
        self.single_viewer.setVisible(False)

        return widget

    def _create_right_panel(self) -> QWidget:
        widget = QWidget()
        widget.setMinimumWidth(250)
        widget.setMaximumWidth(300)
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        presets_group = QGroupBox(t("presets"))
        presets_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self._labels["presets_group"] = presets_group
        presets_layout = QVBoxLayout()

        self.preset_list = QListWidget()
        self.preset_list.setMaximumHeight(120)
        for name in self.preset_manager.list_presets():
            info = self.preset_manager.get_preset_info(name)
            if info:
                en_name = info['name'].split(' / ')[0] if ' / ' in info['name'] else info['name']
                self.preset_list.addItem(en_name)
        self.preset_list.itemDoubleClicked.connect(self._apply_selected_preset)
        presets_layout.addWidget(self.preset_list)

        presets_btns = QHBoxLayout()
        self.apply_preset_btn = QPushButton(t("apply"))
        self.apply_preset_btn.clicked.connect(self._apply_selected_preset)
        presets_btns.addWidget(self.apply_preset_btn)

        presets_group.setLayout(presets_layout)
        layout.addWidget(presets_group)

        batch_group = QGroupBox(t("batch_processing"))
        batch_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self._labels["batch_group"] = batch_group
        batch_layout = QVBoxLayout()

        self.batch_btn = QPushButton(t("add_folder"))
        self.batch_btn.clicked.connect(self._add_folder_to_queue)
        batch_layout.addWidget(self.batch_btn)

        self.process_queue_btn = QPushButton(t("process_queue"))
        self.process_queue_btn.clicked.connect(self._process_queue)
        batch_layout.addWidget(self.process_queue_btn)

        batch_group.setLayout(batch_layout)
        layout.addWidget(batch_group)

        quality_group = QGroupBox(t("quality_metrics"))
        quality_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self._labels["quality_group"] = quality_group
        quality_layout = QVBoxLayout()
        self.quality_label = QLabel(t("load_image_quality"))
        self.quality_label.setWordWrap(True)
        self.quality_label.setStyleSheet("font-size: 10px;")
        quality_layout.addWidget(self.quality_label)
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)

        # Color Reference Panel
        color_group = QGroupBox(t("color_reference"))
        color_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self._labels["color_group"] = color_group
        color_layout = QVBoxLayout()
        color_layout.setSpacing(5)

        self.reference_viewer = ImageViewer(t("reference"))
        self.reference_viewer.setMinimumHeight(120)
        self.reference_viewer.fileDropped.connect(self._on_reference_dropped)
        color_layout.addWidget(self.reference_viewer)

        self.ref_progress = QProgressBar()
        self.ref_progress.setMaximumHeight(10)
        self.ref_progress.setTextVisible(False)
        self.ref_progress.setVisible(False)
        color_layout.addWidget(self.ref_progress)

        self.color_info_label = QLabel(t("select_reference"))
        self.color_info_label.setWordWrap(True)
        self.color_info_label.setStyleSheet("font-size: 9px; color: #888;")
        color_layout.addWidget(self.color_info_label)

        color_btn_layout = QHBoxLayout()
        self.load_ref_btn = QPushButton(t("load_reference"))
        self.load_ref_btn.clicked.connect(self._load_color_reference)
        self.load_ref_btn.setMaximumHeight(28)
        color_btn_layout.addWidget(self.load_ref_btn)

        self.apply_color_btn = QPushButton(t("apply_color"))
        self.apply_color_btn.clicked.connect(self._apply_color_transfer)
        self.apply_color_btn.setMaximumHeight(28)
        self.apply_color_btn.setEnabled(False)
        color_btn_layout.addWidget(self.apply_color_btn)

        self.clear_ref_btn = QPushButton(t("clear_reference"))
        self.clear_ref_btn.clicked.connect(self._clear_color_reference)
        self.clear_ref_btn.setMaximumHeight(28)
        color_btn_layout.addWidget(self.clear_ref_btn)

        color_layout.addLayout(color_btn_layout)
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)

        chibi_group = QGroupBox(t("chibi_transform"))
        chibi_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        chibi_layout = QVBoxLayout()
        chibi_layout.setSpacing(5)

        self.chibi_transformer = ChibiTransformer()

        style_label = QLabel(t("anime_style"))
        chibi_layout.addWidget(style_label)

        self.anime_style_combo = QComboBox()
        self.anime_style_combo.addItems(self.chibi_transformer.get_available_styles())
        self.anime_style_combo.setCurrentText("Hayao")
        chibi_layout.addWidget(self.anime_style_combo)

        self.apply_chibi_btn = QPushButton(t("apply_chibi"))
        self.apply_chibi_btn.clicked.connect(self._apply_chibi_transform)
        self.apply_chibi_btn.setMinimumHeight(35)
        chibi_layout.addWidget(self.apply_chibi_btn)

        chibi_group.setLayout(chibi_layout)
        layout.addWidget(chibi_group)

        layout.addStretch()
        return widget

    def _on_view_mode_changed(self, mode: str):
        old_mode = self._view_mode
        self._view_mode = mode.lower()

        if self._view_mode == "current":
            self.compare_container.setVisible(False)
            self.single_viewer.setVisible(True)
        else:
            self.compare_container.setVisible(True)
            self.single_viewer.setVisible(False)

            if self._view_mode == "split":
                self.original_viewer.setVisible(True)
                self.current_viewer.setVisible(True)
            elif self._view_mode == "original":
                self.original_viewer.setVisible(True)
                self.current_viewer.setVisible(False)

        self._update_views()

    def _create_menu(self):
        menubar = self.menuBar()
        self._menu_items["menubar"] = menubar

        file_menu = menubar.addMenu(t("file"))
        self._menu_items["file_menu"] = file_menu
        
        open_action = QAction(t("open"), self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)
        self._menu_items["open"] = open_action

        save_action = QAction(t("save"), self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)
        self._menu_items["save"] = save_action

        save_as_action = QAction(t("save_as"), self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_image_as)
        file_menu.addAction(save_as_action)
        self._menu_items["save_as"] = save_as_action

        file_menu.addSeparator()
        exit_action = QAction(t("exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        self._menu_items["exit"] = exit_action

        edit_menu = menubar.addMenu(t("edit"))
        self._menu_items["edit_menu"] = edit_menu
        
        reset_action = QAction(t("reset_all"), self)
        reset_action.triggered.connect(self.reset_adjustments)
        edit_menu.addAction(reset_action)
        self._menu_items["reset_all"] = reset_action

        auto_action = QAction(t("auto_enhance"), self)
        auto_action.triggered.connect(self.auto_enhance_image)
        edit_menu.addAction(auto_action)
        self._menu_items["auto_enhance"] = auto_action

        view_menu = menubar.addMenu(t("view"))
        self._menu_items["view_menu"] = view_menu
        
        zoom_in_action = QAction(t("zoom_in"), self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        self._menu_items["zoom_in"] = zoom_in_action

        zoom_out_action = QAction(t("zoom_out"), self)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        self._menu_items["zoom_out"] = zoom_out_action

        fit_action = QAction(t("fit_window"), self)
        fit_action.triggered.connect(self.fit_to_window)
        view_menu.addAction(fit_action)
        self._menu_items["fit_window"] = fit_action

        language_menu = menubar.addMenu(t("language"))
        self._menu_items["language_menu"] = language_menu
        
        en_action = QAction(t("english"), self)
        en_action.triggered.connect(lambda: self._change_language("en"))
        language_menu.addAction(en_action)
        self._menu_items["english"] = en_action

        vi_action = QAction(t("vietnamese"), self)
        vi_action.triggered.connect(lambda: self._change_language("vi"))
        language_menu.addAction(vi_action)
        self._menu_items["vietnamese"] = vi_action
        language_menu.addAction(vi_action)

    def _create_toolbar(self):
        toolbar = QToolBar(t("toolbar_title"))
        self.addToolBar(toolbar)

        open_action = QAction(t("open"), self)
        open_action.triggered.connect(self.open_image)
        toolbar.addAction(open_action)

        save_action = QAction(t("save"), self)
        save_action.triggered.connect(self.save_image)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        reset_action = QAction(t("reset_all"), self)
        reset_action.triggered.connect(self.reset_adjustments)
        toolbar.addAction(reset_action)

        auto_action = QAction(t("auto_enhance"), self)
        auto_action.triggered.connect(self.auto_enhance_image)
        toolbar.addAction(auto_action)

    def _change_language(self, lang: str):
        I18n.set_language(lang)
        self.languageChanged.emit()

    def _update_ui_text(self):
        self.setWindowTitle(t("app_title"))

        # Update Menu
        self._menu_items["file_menu"].setTitle(t("file"))
        self._menu_items["open"].setText(t("open"))
        self._menu_items["save"].setText(t("save"))
        self._menu_items["save_as"].setText(t("save_as"))
        self._menu_items["exit"].setText(t("exit"))
        
        self._menu_items["edit_menu"].setTitle(t("edit"))
        self._menu_items["reset_all"].setText(t("reset_all"))
        self._menu_items["auto_enhance"].setText(t("auto_enhance"))
        
        self._menu_items["view_menu"].setTitle(t("view"))
        self._menu_items["zoom_in"].setText(t("zoom_in"))
        self._menu_items["zoom_out"].setText(t("zoom_out"))
        self._menu_items["fit_window"].setText(t("fit_window"))
        
        self._menu_items["language_menu"].setTitle(t("language"))
        self._menu_items["english"].setText(t("english"))
        self._menu_items["vietnamese"].setText(t("vietnamese"))

        # Update Panel Labels
        self._labels["wb_group"].setTitle(t("white_balance"))
        self.temp_slider.update_label(t("temperature"))
        self.tint_slider.update_label(t("tint"))

        self._labels["levels_group"].setTitle(t("levels"))
        self.shadows_slider.update_label(t("shadows"))
        self.midtone_slider.update_label(t("midtone_gamma"))
        self.highlights_slider.update_label(t("highlights"))

        self._labels["sharpen_group"].setTitle(t("sharpening"))
        self.sharpness_slider.update_label(t("sharpness"))

        self._labels["clahe_group"].setTitle(t("local_contrast"))
        self.clahe_slider.update_label(t("clip_limit"))

        self._labels["presets_group"].setTitle(t("presets"))
        self.apply_preset_btn.setText(t("apply"))

        current_lang = I18n.get_language()
        self.preset_list.clear()
        for name in self.preset_manager.list_presets():
            info = self.preset_manager.get_preset_info(name)
            if info:
                if current_lang == "vi" and ' / ' in info['name']:
                    display_name = info['name'].split(' / ')[1]
                else:
                    display_name = info['name'].split(' / ')[0]
                self.preset_list.addItem(display_name)

        self._labels["batch_group"].setTitle(t("batch_processing"))
        self.batch_btn.setText(t("add_folder"))
        self.process_queue_btn.setText(t("process_queue"))

        self._labels["quality_group"].setTitle(t("quality_metrics"))
        self.original_btn.setText(t("show_original"))

        if self.original_image is None:
            self.quality_label.setText(t("load_image_quality"))

        # Update Color Reference Panel
        self._labels["color_group"].setTitle(t("color_reference"))
        self.load_ref_btn.setText(t("load_reference"))
        self.apply_color_btn.setText(t("apply_color"))
        self.clear_ref_btn.setText(t("clear_reference"))
        if self._color_reference_path is None:
            self.color_info_label.setText(t("select_reference"))

        # Update View Combo
        self.view_combo.blockSignals(True)
        self.view_combo.setItemText(0, t("view_current"))
        self.view_combo.setItemText(1, t("view_original"))
        self.view_combo.setItemText(2, t("view_split"))
        self.view_combo.blockSignals(False)

    def _on_adjustment_changed(self, value: float):
        if self.original_image is None:
            return

        sender = self.sender()
        if sender == self.temp_slider:
            self._adjustments["temperature"] = value
        elif sender == self.tint_slider:
            self._adjustments["tint"] = value
        elif sender == self.shadows_slider:
            self._adjustments["shadows"] = value
        elif sender == self.midtone_slider:
            self._adjustments["midtones"] = value
        elif sender == self.highlights_slider:
            self._adjustments["highlights"] = value
        elif sender == self.sharpness_slider:
            self._adjustments["sharpness"] = value
        elif sender == self.clahe_slider:
            self._adjustments["clahe_clip"] = value

        self._apply_adjustments()
        self.status_bar.showMessage(t("adjusting"), 300)

    def _apply_adjustments(self):
        if self.original_image is None:
            return

        adj = self._adjustments
        result = self.original_image.copy()

        if adj["temperature"] != 0 or adj["tint"] != 0:
            result = self.wb.adjust(result, int(adj["temperature"]), int(adj["tint"]))

        shadow = max(0, 0 + int(adj["shadows"]))
        highlight = min(255, 255 + int(adj["highlights"]))
        result = self.levels.adjust(result, shadows=shadow, midtones=adj["midtones"], highlights=highlight)

        if adj["clahe_clip"] > 1.0:
            result = self.clahe.apply(result, clip_limit=adj["clahe_clip"])

        if adj["sharpness"] > 0:
            result = self.sharp.apply(result, radius=1.0, amount=adj["sharpness"] / 2.0)

        self.current_image = result
        self._update_views()

    def _update_views(self):
        if self._view_mode == "current":
            self.single_viewer.set_image(self.current_image)
        elif self._view_mode == "original":
            self.original_viewer.set_image(self.original_image)
        elif self._view_mode == "split":
            orig = self.original_image if self.original_image is not None else self.current_image
            self.original_viewer.set_image(orig)
            if self.current_image is not None:
                self.current_viewer.set_image(self.current_image)
            else:
                self.current_viewer.set_image(orig)

    def _show_original(self):
        if self.original_image is not None:
            self.view_combo.setCurrentText("Original")
            self._on_view_mode_changed("Original")

    def _on_file_dropped(self, file_path: str):
        try:
            file_path = os.path.abspath(file_path)
            self.original_image = self.processor.load_image(file_path)
            self.current_image = self.original_image.copy()
            
            current_mode = self._view_mode
            if current_mode == "current":
                self.single_viewer.set_image(self.current_image)
            else:
                self.original_viewer.set_image(self.original_image)
                if current_mode == "split":
                    self.current_viewer.set_image(self.current_image)
            
            self._update_quality_metrics()
            self.status_bar.showMessage(t("opened", file_path))
        except Exception as e:
            QMessageBox.critical(self, t("error"), t("failed_open", str(e)))

    def _on_reference_dropped(self, file_path: str):
        try:
            file_path = os.path.abspath(file_path)
            ref_image = self.processor.load_image(file_path)
            
            self._color_reference_image = ref_image
            self.reference_viewer.set_image(ref_image)
            
            self.color_transfer.learn_from_image(ref_image)
            self._color_reference_path = file_path
            
            self.ref_progress.setVisible(True)
            self.ref_progress.setValue(100)
            QApplication.processEvents()
            
            palette = self.color_transfer.source_palette
            info_parts = [
                f"{t('temperature')}: {t(palette.temperature)}",
                f"{t('saturation')}: {palette.saturation:.0%}",
                f"{t('brightness')}: {palette.brightness:.0f}",
                "",
                f"{t('dominant_colors')}:"
            ]
            for i, color in enumerate(palette.dominant_colors[:3]):
                info_parts.append(f"  {i+1}. RGB({color[0]}, {color[1]}, {color[2]})")
            
            self.color_info_label.setText("\n".join(info_parts))
            self.apply_color_btn.setEnabled(True)
            
            QMessageBox.information(self, t("reference_loaded_title"), f"{t('analysis_complete')}\n\n{t('temperature')}: {t(palette.temperature)}\n{t('saturation')}: {palette.saturation:.0%}\n{t('brightness')}: {palette.brightness:.0f}")
            
            self.status_bar.showMessage(t("reference_loaded", file_path))
            self.ref_progress.setVisible(False)
        except Exception as e:
            self.ref_progress.setVisible(False)
            QMessageBox.critical(self, t("error"), t("failed_open", str(e)))

    def _apply_selected_preset(self):
        current_row = self.preset_list.currentRow()
        if current_row < 0:
            return

        preset_names = self.preset_manager.list_presets()
        if current_row < len(preset_names):
            preset = self.preset_manager.load_preset(preset_names[current_row])
            if preset and self.original_image is not None:
                result = self.auto_enhancer.enhance_with_preset(self.original_image, preset.settings)
                self.current_image = result
                self._update_views()
                self._update_quality_metrics()
                self.status_bar.showMessage(t("applied_preset", preset.metadata.name))

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, t("open"), "", "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if file_path:
            try:
                file_path = os.path.abspath(file_path)
                self.original_image = self.processor.load_image(file_path)
                self.current_image = self.original_image.copy()
                self._update_views()
                self._update_quality_metrics()
                self.view_combo.setCurrentText("Current")
                self._on_view_mode_changed("Current")
                self.status_bar.showMessage(t("opened", file_path))
            except Exception as e:
                QMessageBox.critical(self, t("error"), t("failed_open", str(e)))

    def save_image(self):
        if self.current_image is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, t("save_as"), "", "PNG (*.png);;JPEG (*.jpg)"
        )

        if file_path:
            try:
                file_path = os.path.abspath(file_path)
                self.processor.save_image(self.current_image, file_path)
                self.status_bar.showMessage(t("saved", file_path))
            except Exception as e:
                QMessageBox.critical(self, t("error"), t("failed_save", str(e)))

    def save_image_as(self):
        self.save_image()

    def reset_adjustments(self):
        self._adjustments = {
            "temperature": 0, "tint": 0,
            "shadows": 0, "midtones": 1.0, "highlights": 255,
            "sharpness": 0, "clahe_clip": 2.0,
        }

        self.temp_slider.set_value(0)
        self.tint_slider.set_value(0)
        self.shadows_slider.set_value(0)
        self.midtone_slider.set_value(1.0)
        self.highlights_slider.set_value(0)
        self.sharpness_slider.set_value(0)
        self.clahe_slider.set_value(2.0)

        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self._update_views()

        self.status_bar.showMessage(t("reset_adjustments"))

    def auto_enhance_image(self):
        if self.original_image is None:
            return

        try:
            enhanced = self.auto_enhancer.auto_enhance(self.original_image, mode="moderate")
            self.current_image = enhanced
            self._update_views()
            self._update_quality_metrics()
            self.status_bar.showMessage(t("auto_enhance_applied"))
        except Exception as e:
            QMessageBox.warning(self, t("warning"), t("auto_enhance_failed", str(e)))

    def _add_folder_to_queue(self):
        folder = QFileDialog.getExistingDirectory(self, t("add_folder"))
        if folder:
            self.status_bar.showMessage(t("added_folder", folder))

    def _process_queue(self):
        self.status_bar.showMessage(t("process_queue") + "...")
        QTimer.singleShot(100, self._process_queue_step)

    def _process_queue_step(self):
        self.status_bar.showMessage(t("queue_complete"))
        self.progress_bar.setValue(100)

    def _update_quality_metrics(self):
        if self.original_image is None or self.current_image is None:
            return

        scores = self.iqa.evaluate(self.original_image, self.current_image)
        summary = self.iqa.get_summary(scores)
        self.quality_label.setText(summary)

    def _load_color_reference(self):
        """Load a reference image for color analysis."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, t("select_reference"), "", "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if file_path:
            try:
                self.ref_progress.setVisible(True)
                self.ref_progress.setValue(30)
                QApplication.processEvents()
                
                file_path = os.path.abspath(file_path)
                ref_image = self.processor.load_image(file_path)
                
                self.ref_progress.setValue(60)
                QApplication.processEvents()
                
                self._color_reference_image = ref_image
                self.reference_viewer.set_image(ref_image)
                
                self.color_transfer.learn_from_image(ref_image)
                self._color_reference_path = file_path
                
                self.ref_progress.setValue(100)
                QApplication.processEvents()
                
                palette = self.color_transfer.source_palette
                info_parts = [
                    f"{t('temperature')}: {t(palette.temperature)}",
                    f"{t('saturation')}: {palette.saturation:.0%}",
                    f"{t('brightness')}: {palette.brightness:.0f}",
                    "",
                    f"{t('dominant_colors')}:"
                ]
                for i, color in enumerate(palette.dominant_colors[:3]):
                    info_parts.append(f"  {i+1}. RGB({color[0]}, {color[1]}, {color[2]})")
                
                self.color_info_label.setText("\n".join(info_parts))
                self.apply_color_btn.setEnabled(True)
                
                info_text = f"{t('analysis_complete')}\n\n"
                info_text += f"{t('temperature')}: {t(palette.temperature)}\n"
                info_text += f"{t('saturation')}: {palette.saturation:.0%}\n"
                info_text += f"{t('brightness')}: {palette.brightness:.0f}"
                QMessageBox.information(self, t("reference_loaded_title"), info_text)
                
                self.status_bar.showMessage(t("reference_loaded", file_path))
                self.ref_progress.setVisible(False)
            except Exception as e:
                self.ref_progress.setVisible(False)
                QMessageBox.critical(self, t("error"), t("failed_open", str(e)))

    def _apply_color_transfer(self):
        """Apply color from reference to current image."""
        if self.original_image is None:
            QMessageBox.warning(self, t("warning"), t("no_image_to_apply"))
            return
        
        if self.color_transfer.source_palette is None:
            return
        
        try:
            # Apply color transfer
            result = self.color_transfer.apply_to(self.original_image)
            self.current_image = result
            self._update_views()
            self._update_quality_metrics()
            QMessageBox.information(self, t("color_reference"), t("color_applied"))
            self.status_bar.showMessage(t("color_applied"))
        except Exception as e:
            QMessageBox.warning(self, t("warning"), str(e))

    def _clear_color_reference(self):
        """Clear the color reference."""
        self.color_transfer = ColorTransfer()
        self.color_analyzer = ColorAnalyzer()
        self._color_reference_path = None
        self._color_reference_image = None
        self.reference_viewer.clear()
        self.color_info_label.setText(t("select_reference"))
        self.apply_color_btn.setEnabled(False)
        self.status_bar.showMessage(t("reference_cleared"))

    def _apply_chibi_transform(self):
        """Apply Chibi transformation to current image."""
        if self.original_image is None:
            QMessageBox.warning(self, t("warning"), t("no_image_selected"))
            return
        try:
            style = self.anime_style_combo.currentText()
            result = self.chibi_transformer.transform_with_style(self.original_image, style)
            self.current_image = result
            self._update_views()
            self._update_quality_metrics()
            QMessageBox.information(self, t("chibi_transform"), t("chibi_applied"))
            self.status_bar.showMessage(t("chibi_applied"))
        except Exception as e:
            QMessageBox.warning(self, t("warning"), str(e))

    def zoom_in(self):
        self.status_bar.showMessage(t("zoom_in"))

    def zoom_out(self):
        self.status_bar.showMessage(t("zoom_out"))

    def fit_to_window(self):
        self._update_views()


def run_app():
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
