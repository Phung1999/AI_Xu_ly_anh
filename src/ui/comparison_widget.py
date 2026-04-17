"""
Comparison Widget - Phase 4.3
Before/After image comparison.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PyQt6.QtCore import Qt


class ComparisonWidget(QWidget):
    """Widget for comparing original and enhanced images."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)

        self.setLayout(layout)

    def set_images(self, original, enhanced):
        """Set images to compare."""
        pass

    def set_split_position(self, position: float):
        """Set split position (0.0 - 1.0)."""
        pass

    def toggle_mode(self, mode: str):
        """Toggle between modes: split, overlay, side_by_side."""
        pass
