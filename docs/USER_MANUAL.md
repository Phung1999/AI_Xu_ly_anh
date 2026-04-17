# Image Enhancement Studio - User Manual

## Getting Started

### Installation
1. Extract the application
2. Run `ImageEnhancementStudio.exe`

### System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- No GPU required (CPU-optimized)

## Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar: File | Edit | View                                │
├─────────────────────────────────────────────────────────────┤
│ Toolbar: Open | Save | Reset | Auto Enhance                 │
├─────────────┬───────────────────────────┬──────────────────┤
│             │                           │                  │
│  Left       │     Center                 │     Right        │
│  Panel      │     Image Viewer          │     Panel        │
│             │                           │                  │
│  - White    │                           │  - Presets       │
│    Balance  │                           │  - Batch Queue   │
│  - Levels   │                           │  - Quality       │
│  - Sharp    │                           │    Metrics       │
│  - CLAHE    │                           │                  │
│             │                           │                  │
├─────────────┴───────────────────────────┴──────────────────┤
│ Status Bar: Ready                          [Progress Bar]   │
└─────────────────────────────────────────────────────────────┘
```

## Adjustments

### White Balance
- **Temperature**: Adjust color temperature (-100 cool to +100 warm)
- **Tint**: Adjust green/magenta tint (-100 to +100)

### Levels
- **Shadows**: Darken or lighten shadows (adjusts black point)
- **Midtones (Gamma)**: Adjust midtone brightness (0.5 to 2.0)
- **Highlights**: Adjust highlight brightness

### Sharpening
- **Sharpness**: High-pass sharpening intensity (0 to 2.0)

### Local Contrast (CLAHE)
- **Clip Limit**: Contrast enhancement strength (1.0 to 5.0)

## Presets

### Built-in Presets
- **Auto Enhance**: AI-powered automatic enhancement
- **Professional**: Balanced professional photo editing
- **Denoise + Upscale**: Noise reduction with 2x upscaling

### Applying Presets
1. Select a preset from the Presets panel
2. Click "Apply"
3. View the result in the center viewer

## Batch Processing

### Adding Images to Queue
1. Click "Add Folder to Queue"
2. Select a folder containing images
3. Images will be added to the processing queue

### Processing Queue
1. Click "Process Queue"
2. Monitor progress in the status bar
3. Processed images saved to output folder

## Before/After Comparison

### Toggle Views
- **Show Original**: Display unprocessed image
- **Split View**: Side-by-side comparison (click toggle)

### Quality Metrics
Quality scores are calculated automatically when processing:
- **PSNR**: Peak Signal-to-Noise Ratio (higher is better)
- **SSIM**: Structural Similarity Index (0-1, higher is better)
- **CQE**: Color Quality Estimator (0-100)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open image |
| Ctrl+S | Save image |
| Ctrl+Shift+S | Save As |
| Ctrl+Z | Undo (future) |
| Ctrl+R | Reset all |
| Ctrl+E | Auto enhance |
| +/= | Zoom in |
| - | Zoom out |
| 0 | Fit to window |

## Troubleshooting

### Application won't start
- Ensure all dependencies are installed
- Run as administrator if needed

### Slow processing
- Close other applications
- Reduce batch size
- Check system resources

### Poor quality results
- Try different presets
- Adjust individual settings
- Use conservative mode for subtle enhancement

## Export Options

### Formats
- PNG (lossless)
- JPEG (compressed)

### Resolution
- Original resolution preserved
- Upscaling available via presets

## Support

For issues and feedback:
- GitHub Issues: [repository]/issues
- Email: support@example.com
