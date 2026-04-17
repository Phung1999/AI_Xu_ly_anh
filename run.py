"""
Image Enhancement Studio - Main Entry Point

Run: python run.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from src.ui.main_window import run_app


def main():
    """Run the application."""
    logger.info("Starting Image Enhancement Studio...")

    try:
        run_app()
    except KeyboardInterrupt:
        logger.info("Application closed by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise


if __name__ == "__main__":
    main()
