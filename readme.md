# Image Enhancement Studio

Professional AI-powered image enhancement application with batch processing support.

## Features

- **AI Auto Enhancement**: Intelligent image analysis and enhancement
- **Professional Tools**: White Balance, Levels, Sharpening, CLAHE
- **Image Quality Assessment**: PSNR, SSIM, CQE metrics
- **Batch Processing**: Process thousands of images automatically
- **Non-destructive Editing**: Keep original images intact
- **Preset System**: Save and apply custom enhancement presets
- **CPU Optimized**: Works on systems without GPU

## Quick Start

### GUI
```bash
python run.py
```

### Command Line
```bash
# Single image
python scripts/cli.py photo.jpg -o enhanced.jpg --preset auto

# Batch process
python scripts/cli.py input_folder/ -o output_folder/ --preset professional
```

## Presets

| Preset | Description |
|--------|-------------|
| `auto` | AI-powered automatic enhancement |
| `professional` | Balanced professional photo editing |
| `denoise` | Noise reduction with 2x upscaling |

## Requirements

- Windows 10/11 (64-bit)
- Python 3.9+ (for development)
- 4GB RAM minimum

## Installation

```bash
pip install -r requirements.txt
```

## Testing

```bash
pytest tests/ -v
```

## Building

```bash
python scripts/build.py
```

## Project Structure

```
src/
├── modules/       # Core image processing
├── ai/           # AI enhancement
└── ui/           # PyQt6 interface
```

## License

MIT License
