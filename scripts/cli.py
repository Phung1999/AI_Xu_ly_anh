"""
CLI Tool - Command Line Interface
Phase 5: Polish & Production

Process images from command line.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from loguru import logger

from src.modules.image_processor import ImageProcessor
from src.modules.pipeline import PipelineScheduler, PresetPipeline, PipelineStep, PipelineStepType
from src.ai.auto_enhance import AutoEnhancer


def process_single(input_path: str, output_path: str, preset: str = None):
    """Process a single image."""
    logger.info(f"Processing: {input_path}")

    processor = ImageProcessor()
    image = processor.load_image(input_path)

    if preset:
        pipeline = get_preset_pipeline(preset)
        result = pipeline.execute(image)
        output = result.image if result.success else image
    else:
        enhancer = AutoEnhancer()
        output = enhancer.auto_enhance(image, mode="moderate")

    processor.save_image(output, output_path)
    logger.info(f"Saved: {output_path}")


def process_batch(input_dir: str, output_dir: str, preset: str = None):
    """Process a directory of images."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(f"*{ext}"))
        image_files.extend(input_path.glob(f"*{ext.upper()}"))

    logger.info(f"Found {len(image_files)} images")

    processor = ImageProcessor()
    enhancer = AutoEnhancer()
    pipeline = get_preset_pipeline(preset) if preset else None

    for i, img_file in enumerate(image_files, 1):
        logger.info(f"[{i}/{len(image_files)}] Processing: {img_file.name}")

        image = processor.load_image(str(img_file))

        if pipeline:
            result = pipeline.execute(image)
            output = result.image if result.success else image
        else:
            output = enhancer.auto_enhance(image, mode="moderate")

        out_file = output_path / img_file.name
        processor.save_image(output, str(out_file))

    logger.info(f"Batch processing complete. {len(image_files)} images saved to {output_dir}")


def get_preset_pipeline(preset_name: str):
    """Get pipeline for preset."""
    if preset_name == "professional":
        return PresetPipeline.professional_pipeline()
    elif preset_name == "auto":
        return PresetPipeline.auto_enhance_pipeline()
    elif preset_name == "denoise":
        return PresetPipeline.denoise_upscale_pipeline()
    else:
        return PresetPipeline.auto_enhance_pipeline()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Image Enhancement Studio CLI")
    parser.add_argument("input", help="Input image or directory")
    parser.add_argument("-o", "--output", required=True, help="Output path or directory")
    parser.add_argument("-p", "--preset", choices=["auto", "professional", "denoise"],
                        help="Preset to apply")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    input_path = Path(args.input)

    if input_path.is_dir():
        process_batch(str(input_path), args.output, args.preset)
    elif input_path.is_file():
        process_single(str(input_path), args.output, args.preset)
    else:
        logger.error(f"Input not found: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
