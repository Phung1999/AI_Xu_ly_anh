"""
Image Enhancement Studio - Main Entry Point

Run: python main.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Main entry point."""
    from src.ui.main_window import run_app
    run_app()


if __name__ == "__main__":
    main()
