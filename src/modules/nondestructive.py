"""
Non-destructive Layer System - Task 3.4
Phase 3: Batch Processing Engine

Non-destructive editing with layer management.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
from datetime import datetime
import numpy as np

from src.ai.auto_enhance import EnhancementSettings


class LayerBlendMode(Enum):
    """Layer blend modes."""
    NORMAL = "normal"
    SOFT_LIGHT = "soft_light"
    OVERLAY = "overlay"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    ADD = "add"
    DIFFERENCE = "difference"


class LayerType(Enum):
    """Types of layers."""
    ADJUSTMENT = "adjustment"
    IMAGE = "image"
    MASK = "mask"
    TEXT = "text"
    SHAPE = "shape"


@dataclass
class Layer:
    """A single layer in the non-destructive editing stack."""
    id: str
    name: str
    layer_type: LayerType
    enabled: bool = True
    opacity: float = 1.0
    blend_mode: LayerBlendMode = LayerBlendMode.NORMAL
    settings: Optional[EnhancementSettings] = None
    params: Dict[str, Any] = field(default_factory=dict)
    visible: bool = True
    locked: bool = False
    created_at: str = ""
    modified_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.modified_at = self.created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "layer_type": self.layer_type.value,
            "enabled": self.enabled,
            "opacity": self.opacity,
            "blend_mode": self.blend_mode.value,
            "settings": asdict(self.settings) if self.settings else None,
            "params": self.params,
            "visible": self.visible,
            "locked": self.locked,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }


from dataclasses import asdict


@dataclass
class ProjectFile:
    """Non-destructive project file."""
    version: str = "1.0"
    name: str = "Untitled"
    width: int = 0
    height: int = 0
    layers: List[Layer] = field(default_factory=list)
    original_path: Optional[str] = None
    created_at: str = ""
    modified_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.modified_at:
            self.modified_at = self.created_at


class NonDestructiveEditor:
    """
    Non-destructive editing system.

    Keeps original image intact and applies adjustments as layers.
    """

    def __init__(self, project: Optional[ProjectFile] = None):
        self.project = project or ProjectFile()
        self._processors = {}

    def create_project(
        self,
        name: str,
        width: int,
        height: int,
        original_path: Optional[str] = None,
    ) -> ProjectFile:
        """Create a new project."""
        self.project = ProjectFile(
            name=name,
            width=width,
            height=height,
            original_path=original_path,
        )
        logger.info(f"Created project: {name}")
        return self.project

    def load_project(self, project_path: str) -> ProjectFile:
        """Load a project from file."""
        with open(project_path, "r") as f:
            data = json.load(f)

        layers = []
        for layer_data in data.get("layers", []):
            layer = Layer(
                id=layer_data["id"],
                name=layer_data["name"],
                layer_type=LayerType(layer_data["layer_type"]),
                enabled=layer_data.get("enabled", True),
                opacity=layer_data.get("opacity", 1.0),
                blend_mode=LayerBlendMode(layer_data.get("blend_mode", "normal")),
                settings=EnhancementSettings(**layer_data["settings"]) if layer_data.get("settings") else None,
                params=layer_data.get("params", {}),
                visible=layer_data.get("visible", True),
                locked=layer_data.get("locked", False),
                created_at=layer_data.get("created_at", ""),
                modified_at=layer_data.get("modified_at", ""),
            )
            layers.append(layer)

        self.project = ProjectFile(
            version=data.get("version", "1.0"),
            name=data.get("name", "Untitled"),
            width=data.get("width", 0),
            height=data.get("height", 0),
            layers=layers,
            original_path=data.get("original_path"),
            created_at=data.get("created_at", ""),
            modified_at=data.get("modified_at", ""),
            metadata=data.get("metadata", {}),
        )

        logger.info(f"Loaded project: {self.project.name}")
        return self.project

    def save_project(self, project_path: str):
        """Save project to file."""
        self.project.modified_at = datetime.now().isoformat()

        data = {
            "version": self.project.version,
            "name": self.project.name,
            "width": self.project.width,
            "height": self.project.height,
            "original_path": self.project.original_path,
            "created_at": self.project.created_at,
            "modified_at": self.project.modified_at,
            "metadata": self.project.metadata,
            "layers": [layer.to_dict() for layer in self.project.layers],
        }

        Path(project_path).parent.mkdir(parents=True, exist_ok=True)
        with open(project_path, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved project to {project_path}")

    def add_layer(
        self,
        name: str,
        layer_type: LayerType,
        settings: Optional[EnhancementSettings] = None,
        params: Optional[Dict] = None,
    ) -> Layer:
        """Add a new layer."""
        layer_id = f"layer_{len(self.project.layers) + 1}"

        layer = Layer(
            id=layer_id,
            name=name,
            layer_type=layer_type,
            settings=settings,
            params=params or {},
        )

        self.project.layers.append(layer)
        self.project.modified_at = datetime.now().isoformat()

        logger.info(f"Added layer: {name}")
        return layer

    def remove_layer(self, layer_id: str) -> bool:
        """Remove a layer by ID."""
        for i, layer in enumerate(self.project.layers):
            if layer.id == layer_id:
                self.project.layers.pop(i)
                self.project.modified_at = datetime.now().isoformat()
                logger.info(f"Removed layer: {layer_id}")
                return True
        return False

    def get_layer(self, layer_id: str) -> Optional[Layer]:
        """Get a layer by ID."""
        for layer in self.project.layers:
            if layer.id == layer_id:
                return layer
        return None

    def update_layer(self, layer_id: str, updates: Dict):
        """Update layer properties."""
        layer = self.get_layer(layer_id)
        if layer:
            if "name" in updates:
                layer.name = updates["name"]
            if "enabled" in updates:
                layer.enabled = updates["enabled"]
            if "opacity" in updates:
                layer.opacity = updates["opacity"]
            if "blend_mode" in updates:
                layer.blend_mode = LayerBlendMode(updates["blend_mode"])
            if "visible" in updates:
                layer.visible = updates["visible"]
            if "locked" in updates:
                layer.locked = updates["locked"]
            if "params" in updates:
                layer.params.update(updates["params"])

            layer.modified_at = datetime.now().isoformat()
            self.project.modified_at = datetime.now().isoformat()

            return layer
        return None

    def reorder_layers(self, layer_ids: List[str]):
        """Reorder layers by IDs."""
        id_to_layer = {layer.id: layer for layer in self.project.layers}
        new_layers = [id_to_layer[lid] for lid in layer_ids if lid in id_to_layer]

        if len(new_layers) == len(self.project.layers):
            self.project.layers = new_layers
            self.project.modified_at = datetime.now().isoformat()
            logger.info("Layers reordered")

    def duplicate_layer(self, layer_id: str) -> Optional[Layer]:
        """Duplicate a layer."""
        layer = self.get_layer(layer_id)
        if layer:
            new_layer = Layer(
                id=f"layer_{len(self.project.layers) + 1}",
                name=f"{layer.name} (copy)",
                layer_type=layer.layer_type,
                enabled=layer.enabled,
                opacity=layer.opacity,
                blend_mode=layer.blend_mode,
                settings=layer.settings,
                params=layer.params.copy(),
                visible=layer.visible,
                locked=False,
            )
            self.project.layers.append(new_layer)
            self.project.modified_at = datetime.now().isoformat()
            return new_layer
        return None

    def merge_layers(self) -> np.ndarray:
        """Merge all visible layers into final image."""
        from src.ai.auto_enhance import AutoEnhancer

        if not self.project.original_path:
            raise ValueError("No original image path in project")

        enhancer = AutoEnhancer()

        from src.modules.image_processor import ImageProcessor
        processor = ImageProcessor()
        image = processor.load_image(self.project.original_path)

        for layer in self.project.layers:
            if not layer.enabled or not layer.visible:
                continue

            if layer.layer_type == LayerType.ADJUSTMENT and layer.settings:
                image = enhancer.enhance_with_preset(image, layer.settings)

        return image

    def get_layer_stack_info(self) -> Dict:
        """Get information about the layer stack."""
        return {
            "total_layers": len(self.project.layers),
            "enabled_layers": sum(1 for l in self.project.layers if l.enabled),
            "visible_layers": sum(1 for l in self.project.layers if l.visible),
            "adjustment_layers": sum(1 for l in self.project.layers if l.layer_type == LayerType.ADJUSTMENT),
            "layers": [
                {
                    "id": l.id,
                    "name": l.name,
                    "type": l.layer_type.value,
                    "enabled": l.enabled,
                    "visible": l.visible,
                    "opacity": l.opacity,
                }
                for l in self.project.layers
            ],
        }

    def export_render(self, output_path: str):
        """Export final rendered image."""
        merged = self.merge_layers()

        from src.modules.image_processor import ImageProcessor
        processor = ImageProcessor()
        processor.save_image(merged, output_path)

        logger.info(f"Exported render to {output_path}")
