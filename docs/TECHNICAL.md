# Image Enhancement Studio - Technical Documentation

## Overview
Professional image enhancement application with AI-powered automation, batch processing, and non-destructive editing.

## Architecture

```
src/
├── modules/              # Core processing modules
│   ├── image_processor.py    # Image I/O and basic operations
│   ├── levels.py             # Photoshop-style levels adjustment
│   ├── white_balance.py      # Temperature & tint adjustment
│   ├── sharpening.py         # High-pass sharpening
│   ├── clahe.py              # Contrast enhancement
│   ├── iqa.py                # Image quality assessment
│   ├── pipeline.py           # Workflow scheduler
│   ├── queue.py              # Batch processing queue
│   ├── preset.py             # Preset management
│   ├── nondestructive.py     # Layer-based editing
│   └── performance.py        # Performance monitoring
│
├── ai/                   # AI modules
│   ├── enhancement.py        # Super-resolution & enhancement
│   └── auto_enhance.py       # Intelligent auto enhancement
│
└── ui/                   # PyQt6 interface
    ├── main_window.py        # Main application window
    ├── trackbar_widget.py    # Adjustment sliders
    ├── comparison_widget.py  # Before/after comparison
    └── preset_gallery.py     # Preset gallery
```

## Core Classes

### ImageProcessor
```python
from src.modules.image_processor import ImageProcessor

processor = ImageProcessor()
image = processor.load_image("photo.jpg")
resized = processor.resize(image, width=800)
processor.save_image(resized, "output.jpg")
```

### LevelsAdjustment
```python
from src.modules.levels import LevelsAdjustment

levels = LevelsAdjustment()
adjusted = levels.adjust(image, shadows=10, midtones=1.1, highlights=245)
```

### ImageQualityAssessment
```python
from src.modules.iqa import ImageQualityAssessment

iqa = ImageQualityAssessment()
scores = iqa.evaluate(original, enhanced)
print(iqa.get_summary(scores))
```

### AutoEnhancer
```python
from src.ai.auto_enhance import AutoEnhancer

enhancer = AutoEnhancer()
analysis = enhancer.analyze(image)
enhanced = enhancer.auto_enhance(image, mode="moderate")
```

### ProcessingQueue
```python
from src.modules.queue import ProcessingQueue
from src.modules.pipeline import PresetPipeline

queue = ProcessingQueue()
queue.add_from_directory("input/", "output/")
queue.process_all()
```

## Workflow Pipeline

```python
from src.modules.pipeline import PipelineScheduler, PipelineStep, PipelineStepType

pipeline = PipelineScheduler()
pipeline.add_step(PipelineStep("wb", PipelineStepType.PROCESS,
    {"type": "white_balance", "temperature": 10}))
pipeline.add_step(PipelineStep("levels", PipelineStepType.PROCESS,
    {"shadows": 10, "midtones": 1.05}))
pipeline.add_step(PipelineStep("sharpen", PipelineStepType.PROCESS,
    {"type": "sharpening", "amount": 0.3}))

result = pipeline.execute(image)
```

## Presets

```python
from src.modules.preset import PresetManager

manager = PresetManager()
presets = manager.list_presets()
preset = manager.load_preset("professional")
```

## Performance Monitoring

```python
from src.modules.performance import PerformanceMonitor

monitor = PerformanceMonitor()
monitor.record("resize", 0.05)
print(monitor.get_stats("resize"))
```

## Command Line Usage

```bash
# Run UI
python -m src.ui.main_window

# Run batch processing
python scripts/batch_process.py --input input/ --output output/

# Run single image enhancement
python scripts/enhance.py photo.jpg -o enhanced.jpg --preset professional
```

## Dependencies

- Python 3.9+
- OpenCV 4.8+
- NumPy
- PyQt6
- scikit-image
- ONNX Runtime (optional)
