"""
Test suite for Phase 3 - Batch Processing Engine
Phase 3: Tasks 3.1-3.4

Run: pytest tests/test_batch_processing.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np


class TestPipelineScheduler:
    """Test suite for PipelineScheduler"""

    def test_initialization(self):
        """Test PipelineScheduler initialization"""
        from src.modules.pipeline import PipelineScheduler

        pipeline = PipelineScheduler()
        assert pipeline is not None
        assert len(pipeline.steps) == 0

    def test_add_step(self):
        """Test adding steps to pipeline"""
        from src.modules.pipeline import PipelineScheduler, PipelineStep, PipelineStepType

        pipeline = PipelineScheduler()
        step = PipelineStep(
            name="test_step",
            step_type=PipelineStepType.PROCESS,
            params={"type": "levels"},
        )

        pipeline.add_step(step)
        assert len(pipeline.steps) == 1

    def test_remove_step(self):
        """Test removing a step"""
        from src.modules.pipeline import PipelineScheduler, PipelineStep, PipelineStepType

        pipeline = PipelineScheduler()
        step = PipelineStep(name="test", step_type=PipelineStepType.PROCESS)
        pipeline.add_step(step)

        result = pipeline.remove_step("test")
        assert result is True
        assert len(pipeline.steps) == 0

    def test_clear_steps(self):
        """Test clearing all steps"""
        from src.modules.pipeline import PipelineScheduler, PipelineStep, PipelineStepType

        pipeline = PipelineScheduler()
        for i in range(3):
            pipeline.add_step(PipelineStep(name=f"step{i}", step_type=PipelineStepType.PROCESS))

        pipeline.clear_steps()
        assert len(pipeline.steps) == 0

    def test_execute_with_levels(self):
        """Test executing pipeline with levels step"""
        from src.modules.pipeline import PipelineScheduler, PipelineStep, PipelineStepType

        pipeline = PipelineScheduler()
        pipeline.add_step(
            PipelineStep(
                name="levels",
                step_type=PipelineStepType.PROCESS,
                params={"type": "levels", "shadows": 10, "midtones": 1.1},
            )
        )

        img = np.zeros((100, 100, 3), dtype=np.uint8)
        result = pipeline.execute(img)

        assert result.success is True
        assert result.image is not None

    def test_to_json(self):
        """Test pipeline JSON export"""
        from src.modules.pipeline import PipelineScheduler, PipelineStep, PipelineStepType

        pipeline = PipelineScheduler()
        pipeline.add_step(
            PipelineStep(name="test", step_type=PipelineStepType.PROCESS)
        )

        json_str = pipeline.to_json()
        assert "test" in json_str
        assert "step_type" in json_str

    def test_from_json(self):
        """Test pipeline JSON import"""
        from src.modules.pipeline import PipelineScheduler

        pipeline = PipelineScheduler()
        json_str = '{"steps": [{"name": "loaded", "step_type": "process", "params": {}, "enabled": true}]}'

        pipeline.from_json(json_str)
        assert len(pipeline.steps) == 1
        assert pipeline.steps[0].name == "loaded"


class TestPresetPipeline:
    """Test suite for PresetPipeline"""

    def test_auto_enhance_pipeline(self):
        """Test auto enhance preset"""
        from src.modules.pipeline import PresetPipeline

        pipeline = PresetPipeline.auto_enhance_pipeline()
        assert len(pipeline.steps) >= 1

    def test_professional_pipeline(self):
        """Test professional pipeline"""
        from src.modules.pipeline import PresetPipeline

        pipeline = PresetPipeline.professional_pipeline()
        assert len(pipeline.steps) == 4

    def test_denoise_upscale_pipeline(self):
        """Test denoise and upscale pipeline"""
        from src.modules.pipeline import PresetPipeline

        pipeline = PresetPipeline.denoise_upscale_pipeline(scale=2)
        assert len(pipeline.steps) == 2


class TestProcessingQueue:
    """Test suite for ProcessingQueue"""

    def test_initialization(self):
        """Test ProcessingQueue initialization"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        assert queue is not None
        assert len(queue.items) == 0

    def test_add_item(self):
        """Test adding item to queue"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        item = queue.add_item("input.jpg", "output.jpg")

        assert item is not None
        assert item.input_path == "input.jpg"
        assert queue.stats.total == 1

    def test_add_items(self):
        """Test adding multiple items"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        items = [("in1.jpg", "out1.jpg"), ("in2.jpg", "out2.jpg")]
        queue_items = queue.add_items(items)

        assert len(queue_items) == 2
        assert queue.stats.total == 2

    def test_get_item(self):
        """Test getting item by ID"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        item = queue.add_item("input.jpg", "output.jpg")

        retrieved = queue.get_item(item.id)
        assert retrieved is not None
        assert retrieved.id == item.id

    def test_remove_item(self):
        """Test removing item"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        item = queue.add_item("input.jpg", "output.jpg")

        result = queue.remove_item(item.id)
        assert result is True
        assert queue.stats.total == 0

    def test_clear_queue(self):
        """Test clearing queue"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        queue.add_item("in1.jpg", "out1.jpg")
        queue.add_item("in2.jpg", "out2.jpg")

        queue.clear_queue()
        assert len(queue.items) == 0

    def test_stats(self):
        """Test queue statistics"""
        from src.modules.queue import ProcessingQueue

        queue = ProcessingQueue()
        queue.add_item("in1.jpg", "out1.jpg")
        queue.add_item("in2.jpg", "out2.jpg")

        stats = queue.get_stats()
        assert stats.total == 2
        assert stats.pending == 2


class TestPresetManager:
    """Test suite for PresetManager"""

    def test_initialization(self):
        """Test PresetManager initialization"""
        from src.modules.preset import PresetManager

        manager = PresetManager()
        assert manager is not None
        assert len(manager.presets) > 0

    def test_list_presets(self):
        """Test listing presets"""
        from src.modules.preset import PresetManager

        manager = PresetManager()
        presets = manager.list_presets()

        assert len(presets) > 0
        assert "auto_enhance" in presets

    def test_load_preset(self):
        """Test loading a preset"""
        from src.modules.preset import PresetManager

        manager = PresetManager()
        preset = manager.load_preset("auto_enhance")

        assert preset is not None
        assert preset.metadata.name == "Auto Enhance"

    def test_get_preset_info(self):
        """Test getting preset info"""
        from src.modules.preset import PresetManager

        manager = PresetManager()
        info = manager.get_preset_info("auto_enhance")

        assert info is not None
        assert "name" in info
        assert "description" in info


class TestNonDestructiveEditor:
    """Test suite for NonDestructiveEditor"""

    def test_initialization(self):
        """Test NonDestructiveEditor initialization"""
        from src.modules.nondestructive import NonDestructiveEditor

        editor = NonDestructiveEditor()
        assert editor is not None

    def test_create_project(self):
        """Test creating a project"""
        from src.modules.nondestructive import NonDestructiveEditor

        editor = NonDestructiveEditor()
        project = editor.create_project("Test Project", 1920, 1080)

        assert project is not None
        assert project.name == "Test Project"
        assert project.width == 1920
        assert project.height == 1080

    def test_add_layer(self):
        """Test adding a layer"""
        from src.modules.nondestructive import NonDestructiveEditor, LayerType
        from src.ai.auto_enhance import EnhancementSettings

        editor = NonDestructiveEditor()
        editor.create_project("Test", 100, 100)

        layer = editor.add_layer(
            name="Test Layer",
            layer_type=LayerType.ADJUSTMENT,
            settings=EnhancementSettings(temperature=10),
        )

        assert layer is not None
        assert len(editor.project.layers) == 1

    def test_remove_layer(self):
        """Test removing a layer"""
        from src.modules.nondestructive import NonDestructiveEditor, LayerType

        editor = NonDestructiveEditor()
        editor.create_project("Test", 100, 100)
        layer = editor.add_layer(name="Test", layer_type=LayerType.ADJUSTMENT)

        result = editor.remove_layer(layer.id)
        assert result is True
        assert len(editor.project.layers) == 0

    def test_update_layer(self):
        """Test updating a layer"""
        from src.modules.nondestructive import NonDestructiveEditor, LayerType

        editor = NonDestructiveEditor()
        editor.create_project("Test", 100, 100)
        layer = editor.add_layer(name="Test", layer_type=LayerType.ADJUSTMENT)

        editor.update_layer(layer.id, {"name": "Updated", "opacity": 0.5})
        updated = editor.get_layer(layer.id)

        assert updated.name == "Updated"
        assert updated.opacity == 0.5

    def test_duplicate_layer(self):
        """Test duplicating a layer"""
        from src.modules.nondestructive import NonDestructiveEditor, LayerType

        editor = NonDestructiveEditor()
        editor.create_project("Test", 100, 100)
        layer = editor.add_layer(name="Original", layer_type=LayerType.ADJUSTMENT)

        duplicated = editor.duplicate_layer(layer.id)

        assert duplicated is not None
        assert len(editor.project.layers) == 2
        assert duplicated.name == "Original (copy)"

    def test_get_layer_stack_info(self):
        """Test getting layer stack info"""
        from src.modules.nondestructive import NonDestructiveEditor, LayerType

        editor = NonDestructiveEditor()
        editor.create_project("Test", 100, 100)
        editor.add_layer(name="Layer 1", layer_type=LayerType.ADJUSTMENT)
        editor.add_layer(name="Layer 2", layer_type=LayerType.ADJUSTMENT)

        info = editor.get_layer_stack_info()

        assert info["total_layers"] == 2
        assert info["enabled_layers"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
