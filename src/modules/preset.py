"""
Preset System - Task 3.3
Phase 3: Batch Processing Engine

Preset management for saving and loading processing configurations.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from loguru import logger
from datetime import datetime

from src.ai.auto_enhance import EnhancementSettings


@dataclass
class PresetMetadata:
    """Metadata for a preset."""
    name: str
    description: str = ""
    author: str = ""
    created_at: str = ""
    updated_at: str = ""
    tags: List[str] = field(default_factory=list)
    version: str = "1.0"
    category: str = "custom"


@dataclass
class ProcessingPreset:
    """A complete processing preset."""
    metadata: PresetMetadata
    settings: EnhancementSettings
    pipeline_steps: List[Dict[str, Any]] = field(default_factory=list)
    options: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "metadata": asdict(self.metadata),
            "settings": asdict(self.settings),
            "pipeline_steps": self.pipeline_steps,
            "options": self.options,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProcessingPreset":
        metadata = PresetMetadata(**data["metadata"])
        settings = EnhancementSettings(**data["settings"])
        return cls(
            metadata=metadata,
            settings=settings,
            pipeline_steps=data.get("pipeline_steps", []),
            options=data.get("options", {}),
        )


class PresetManager:
    """
    Manager for processing presets.

    Handles saving, loading, and organizing presets.
    """

    def __init__(self, preset_dir: Optional[str] = None):
        if preset_dir:
            self.preset_dir = Path(preset_dir)
        else:
            self.preset_dir = Path(__file__).parent.parent.parent / "assets" / "presets"

        self.preset_dir.mkdir(parents=True, exist_ok=True)
        self.presets: Dict[str, ProcessingPreset] = {}
        self._load_builtin_presets()

    def _load_builtin_presets(self):
        """Load built-in presets."""
        builtin_presets = {
            "auto_enhance": self._create_auto_enhance_preset(),
            "portrait": self._create_portrait_preset(),
            "landscape": self._create_landscape_preset(),
            "vivid": self._create_vivid_preset(),
            "vintage": self._create_vintage_preset(),
            "bw_classic": self._create_bw_preset(),
            "cinematic": self._create_cinematic_preset(),
            "moody": self._create_moody_preset(),
            "golden_hour": self._create_golden_hour_preset(),
            "teal_orange": self._create_teal_orange_preset(),
            "fade_matte": self._create_fade_matte_preset(),
            "cyberpunk": self._create_cyberpunk_preset(),
            "autumn_warmth": self._create_autumn_warmth_preset(),
            "nordic_cool": self._create_nordic_cool_preset(),
            "sunset_glow": self._create_sunset_glow_preset(),
            "film_noir": self._create_film_noir_preset(),
        }

        for name, preset in builtin_presets.items():
            self.presets[name] = preset
            self._save_preset_to_file(preset)

    def _create_auto_enhance_preset(self) -> ProcessingPreset:
        """Create auto enhance preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Auto Enhance",
                description="Automatically enhance image quality",
                category="enhancement",
                tags=["auto", "enhancement", "recommended"],
            ),
            settings=EnhancementSettings(
                midtones=1.1,
                clahe_clip=2.0,
            ),
            pipeline_steps=[
                {"type": "auto_enhance", "params": {"mode": "moderate"}},
            ],
            options={"auto_apply": True},
        )

    def _create_portrait_preset(self) -> ProcessingPreset:
        """Create portrait preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Portrait",
                description="Optimized for portrait photography",
                category="photography",
                tags=["portrait", "skin", "beauty"],
            ),
            settings=EnhancementSettings(
                temperature=5,
                tint=5,
                shadows=10,
                midtones=1.05,
                sharpness=0.2,
                clahe_clip=1.5,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 5, "tint": 5}},
                {"type": "levels", "params": {"shadows": 10, "midtones": 1.05}},
                {"type": "clahe", "params": {"clip_limit": 1.5}},
            ],
        )

    def _create_landscape_preset(self) -> ProcessingPreset:
        """Create landscape preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Landscape",
                description="Enhanced colors and contrast for nature scenes",
                category="photography",
                tags=["landscape", "nature", "colors"],
            ),
            settings=EnhancementSettings(
                temperature=10,
                tint=0,
                shadows=5,
                midtones=1.1,
                highlights=250,
                sharpness=0.4,
                clahe_clip=2.5,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 10}},
                {"type": "levels", "params": {"shadows": 5, "midtones": 1.1, "highlights": 250}},
                {"type": "clahe", "params": {"clip_limit": 2.5}},
                {"type": "sharpening", "params": {"amount": 0.4}},
            ],
        )

    def _create_vivid_preset(self) -> ProcessingPreset:
        """Create vivid preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Vivid",
                description="High saturation and contrast",
                category="artistic",
                tags=["vivid", "saturated", "colors"],
            ),
            settings=EnhancementSettings(
                midtones=1.2,
                contrast=0.2,
                sharpness=0.5,
                clahe_clip=3.0,
            ),
            pipeline_steps=[
                {"type": "levels", "params": {"midtones": 1.2}},
                {"type": "clahe", "params": {"clip_limit": 3.0}},
                {"type": "sharpening", "params": {"amount": 0.5}},
            ],
        )

    def _create_vintage_preset(self) -> ProcessingPreset:
        """Create vintage preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Vintage",
                description="Warm, faded vintage look",
                category="artistic",
                tags=["vintage", "warm", "faded"],
            ),
            settings=EnhancementSettings(
                temperature=25,
                tint=10,
                shadows=15,
                midtones=0.9,
                highlights=240,
                clahe_clip=1.0,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 25, "tint": 10}},
                {"type": "levels", "params": {"shadows": 15, "midtones": 0.9, "highlights": 240}},
                {"type": "clahe", "params": {"clip_limit": 1.0}},
            ],
        )

    def _create_bw_preset(self) -> ProcessingPreset:
        """Create classic black and white preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Classic B&W",
                description="Timeless black and white conversion",
                category="artistic",
                tags=["bw", "monochrome", "classic"],
            ),
            settings=EnhancementSettings(
                shadows=5,
                midtones=1.15,
                contrast=0.3,
                sharpness=0.4,
            ),
            pipeline_steps=[
                {"type": "levels", "params": {"shadows": 5, "midtones": 1.15}},
                {"type": "grayscale"},
            ],
            options={"color_to_grayscale": True},
        )

    def _create_cinematic_preset(self) -> ProcessingPreset:
        """Create cinematic film look preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Cinematic / Điện Ảnh",
                description="Phong cách phim Hollywood với độ tương phản phong phú / Hollywood film look with rich contrast",
                category="theme",
                tags=["cinematic", "film", "moody", "professional"],
            ),
            settings=EnhancementSettings(
                temperature=-5,
                tint=5,
                shadows=-10,
                midtones=1.15,
                highlights=235,
                contrast=0.25,
                clahe_clip=2.0,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": -5, "tint": 5}},
                {"type": "levels", "params": {"shadows": -10, "midtones": 1.15, "highlights": 235}},
                {"type": "clahe", "params": {"clip_limit": 2.0}},
            ],
        )

    def _create_moody_preset(self) -> ProcessingPreset:
        """Create moody dark atmospheric preset."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Moody Dark / U Ám",
                description="Tâm trạng u ám với bóng tối sâu / Dark atmospheric mood with deep shadows",
                category="theme",
                tags=["moody", "dark", "atmospheric", "mystery"],
            ),
            settings=EnhancementSettings(
                temperature=-10,
                tint=0,
                shadows=-15,
                midtones=1.2,
                highlights=225,
                contrast=0.35,
                clahe_clip=1.5,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": -10}},
                {"type": "levels", "params": {"shadows": -15, "midtones": 1.2, "highlights": 225}},
                {"type": "clahe", "params": {"clip_limit": 1.5}},
            ],
        )

    def _create_golden_hour_preset(self) -> ProcessingPreset:
        """Create warm golden hour look."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Golden Hour / Giờ Vàng",
                description="Hiệu ứng ánh sáng hoàng hôn ấm áp / Warm sunset lighting effect",
                category="theme",
                tags=["golden", "warm", "sunset", "sunlight"],
            ),
            settings=EnhancementSettings(
                temperature=30,
                tint=8,
                shadows=5,
                midtones=1.1,
                highlights=250,
                contrast=0.15,
                clahe_clip=2.0,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 30, "tint": 8}},
                {"type": "levels", "params": {"shadows": 5, "midtones": 1.1, "highlights": 250}},
                {"type": "clahe", "params": {"clip_limit": 2.0}},
            ],
        )

    def _create_teal_orange_preset(self) -> ProcessingPreset:
        """Create teal and orange complementary color grading."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Teal & Orange / Xanh Đỏ Cam",
                description="Màu bổ túc kinh điển của điện ảnh / Cinematic complementary color split",
                category="theme",
                tags=["teal", "orange", "complementary", "cinema"],
            ),
            settings=EnhancementSettings(
                temperature=-8,
                tint=8,
                shadows=-5,
                midtones=1.18,
                highlights=250,
                contrast=0.3,
                clahe_clip=2.5,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": -8, "tint": 8}},
                {"type": "levels", "params": {"shadows": -5, "midtones": 1.18, "highlights": 250}},
                {"type": "clahe", "params": {"clip_limit": 2.5}},
            ],
        )

    def _create_fade_matte_preset(self) -> ProcessingPreset:
        """Create faded matte look."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Fade Matte / Mờ Nhẹ",
                description="Phong cách mờ nhẹ với blacks nâng cao / Soft faded look with lifted blacks",
                category="theme",
                tags=["fade", "matte", "soft", "pastel"],
            ),
            settings=EnhancementSettings(
                temperature=5,
                tint=0,
                shadows=20,
                midtones=0.95,
                highlights=245,
                contrast=0.1,
                clahe_clip=1.5,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 5}},
                {"type": "levels", "params": {"shadows": 20, "midtones": 0.95, "highlights": 245}},
                {"type": "clahe", "params": {"clip_limit": 1.5}},
            ],
        )

    def _create_cyberpunk_preset(self) -> ProcessingPreset:
        """Create cyberpunk neon aesthetic."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Cyberpunk / Tương Lai",
                description="Neon tương lai với màu sắc contrast cao / Neon cyberpunk with high contrast colors",
                category="theme",
                tags=["cyberpunk", "neon", "futuristic", "glow"],
            ),
            settings=EnhancementSettings(
                temperature=-15,
                tint=15,
                shadows=-10,
                midtones=1.25,
                highlights=235,
                contrast=0.4,
                clahe_clip=3.0,
                sharpness=0.5,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": -15, "tint": 15}},
                {"type": "levels", "params": {"shadows": -10, "midtones": 1.25, "highlights": 235}},
                {"type": "clahe", "params": {"clip_limit": 3.0}},
                {"type": "sharpening", "params": {"amount": 0.5}},
            ],
        )

    def _create_autumn_warmth_preset(self) -> ProcessingPreset:
        """Create warm autumn tones."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Autumn Warmth / Thu Ấm",
                description="Tông ấm cam đỏ giàu có của mùa thu / Rich warm orange and red autumn tones",
                category="theme",
                tags=["autumn", "warm", "orange", "nature"],
            ),
            settings=EnhancementSettings(
                temperature=25,
                tint=12,
                shadows=5,
                midtones=1.12,
                highlights=250,
                contrast=0.2,
                clahe_clip=2.0,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 25, "tint": 12}},
                {"type": "levels", "params": {"shadows": 5, "midtones": 1.12, "highlights": 250}},
                {"type": "clahe", "params": {"clip_limit": 2.0}},
            ],
        )

    def _create_nordic_cool_preset(self) -> ProcessingPreset:
        """Create cool Nordic light aesthetic."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Nordic Cool / Bắc Âu Lạnh",
                description="Tông lạnh sạch sẽ với contrast nhẹ / Clean cool tones with soft contrast",
                category="theme",
                tags=["nordic", "cool", "clean", "minimal"],
            ),
            settings=EnhancementSettings(
                temperature=-15,
                tint=-5,
                shadows=5,
                midtones=1.08,
                highlights=250,
                contrast=0.15,
                clahe_clip=1.8,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": -15, "tint": -5}},
                {"type": "levels", "params": {"shadows": 5, "midtones": 1.08, "highlights": 250}},
                {"type": "clahe", "params": {"clip_limit": 1.8}},
            ],
        )

    def _create_sunset_glow_preset(self) -> ProcessingPreset:
        """Create warm sunset glow effect."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Sunset Glow / Hoàng Hôn Rực Rỡ",
                description="Hoàng hôn ma mị với tím và cam / Magical sunset with purple and orange",
                category="theme",
                tags=["sunset", "glow", "purple", "orange"],
            ),
            settings=EnhancementSettings(
                temperature=20,
                tint=5,
                shadows=-5,
                midtones=1.15,
                highlights=252,
                contrast=0.25,
                clahe_clip=2.2,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": 20, "tint": 5}},
                {"type": "levels", "params": {"shadows": -5, "midtones": 1.15, "highlights": 252}},
                {"type": "clahe", "params": {"clip_limit": 2.2}},
            ],
        )

    def _create_film_noir_preset(self) -> ProcessingPreset:
        """Create dramatic film noir look."""
        return ProcessingPreset(
            metadata=PresetMetadata(
                name="Film Noir / Phim Cổ Điển",
                description="Trắng đen drama với độ tương phản cao / High contrast black and white drama",
                category="theme",
                tags=["noir", "drama", "high-contrast", "classic"],
            ),
            settings=EnhancementSettings(
                temperature=-5,
                tint=0,
                shadows=-20,
                midtones=1.3,
                highlights=230,
                contrast=0.5,
                clahe_clip=2.0,
                sharpness=0.4,
            ),
            pipeline_steps=[
                {"type": "white_balance", "params": {"temperature": -5}},
                {"type": "levels", "params": {"shadows": -20, "midtones": 1.3, "highlights": 230}},
                {"type": "clahe", "params": {"clip_limit": 2.0}},
                {"type": "grayscale"},
                {"type": "sharpening", "params": {"amount": 0.4}},
            ],
            options={"color_to_grayscale": True},
        )

    def save_preset(self, name: str, preset: ProcessingPreset):
        """Save a preset."""
        preset.metadata.updated_at = datetime.now().isoformat()
        self.presets[name] = preset
        self._save_preset_to_file(preset)
        logger.info(f"Saved preset: {name}")

    def load_preset(self, name: str) -> Optional[ProcessingPreset]:
        """Load a preset by name."""
        if name in self.presets:
            return self.presets[name]

        preset_path = self.preset_dir / f"{name}.json"
        if preset_path.exists():
            try:
                with open(preset_path, "r") as f:
                    data = json.load(f)
                preset = ProcessingPreset.from_dict(data)
                self.presets[name] = preset
                return preset
            except Exception as e:
                logger.error(f"Failed to load preset {name}: {e}")

        return None

    def delete_preset(self, name: str) -> bool:
        """Delete a preset."""
        if name in self.presets:
            del self.presets[name]

        preset_path = self.preset_dir / f"{name}.json"
        if preset_path.exists():
            preset_path.unlink()
            logger.info(f"Deleted preset: {name}")
            return True

        return False

    def list_presets(self, category: Optional[str] = None) -> List[str]:
        """List all presets, optionally filtered by category."""
        if category:
            return [
                name for name, preset in self.presets.items()
                if preset.metadata.category == category
            ]
        return list(self.presets.keys())

    def get_preset_info(self, name: str) -> Optional[Dict]:
        """Get preset information."""
        preset = self.load_preset(name)
        if preset:
            return {
                "name": preset.metadata.name,
                "description": preset.metadata.description,
                "category": preset.metadata.category,
                "tags": preset.metadata.tags,
                "created": preset.metadata.created_at,
                "updated": preset.metadata.updated_at,
            }
        return None

    def _save_preset_to_file(self, preset: ProcessingPreset):
        """Save preset to JSON file."""
        import unicodedata
        slug = preset.metadata.name.lower()
        slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('ascii')
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '_', slug)
        preset_path = self.preset_dir / f"{slug}.json"
        with open(preset_path, "w") as f:
            json.dump(preset.to_dict(), f, indent=2)

    def export_preset(self, name: str, export_path: str):
        """Export preset to a specific location."""
        preset = self.load_preset(name)
        if preset:
            with open(export_path, "w") as f:
                json.dump(preset.to_dict(), f, indent=2)
            logger.info(f"Exported preset to {export_path}")

    def import_preset(self, import_path: str, new_name: Optional[str] = None):
        """Import preset from a file."""
        try:
            with open(import_path, "r") as f:
                data = json.load(f)
            preset = ProcessingPreset.from_dict(data)

            if new_name:
                preset.metadata.name = new_name

            if not preset.metadata.created_at:
                preset.metadata.created_at = datetime.now().isoformat()
            preset.metadata.updated_at = datetime.now().isoformat()

            name = preset.metadata.name.lower().replace(" ", "_")
            self.save_preset(name, preset)
            logger.info(f"Imported preset: {name}")
            return name

        except Exception as e:
            logger.error(f"Failed to import preset: {e}")
            return None
