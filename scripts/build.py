"""
Build Script - Task 5.3
Phase 5: Polish & Production

Build and package the application.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ["build", "dist", "__pycache__"]

    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"Cleaned: {dir_name}")


def build_executable():
    """Build executable using PyInstaller."""
    print("Building executable with PyInstaller...")

    try:
        subprocess.run(
            ["pyinstaller", "build/spec/main.spec", "--clean"],
            check=True
        )
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Install with: pip install pyinstaller")
        return False


def create_distribution_folder():
    """Create distribution folder with necessary files."""
    dist_path = Path("dist/ImageEnhancementStudio")
    dist_path.mkdir(parents=True, exist_ok=True)

    docs_path = dist_path / "docs"
    docs_path.mkdir(exist_ok=True)

    for doc in ["USER_MANUAL.md", "TECHNICAL.md"]:
        src = Path("docs") / doc
        if src.exists():
            shutil.copy(src, docs_path / doc)

    readme = dist_path / "README.txt"
    readme.write_text("""
Image Enhancement Studio
========================

For help, see docs/USER_MANUAL.md

Quick Start:
1. Run ImageEnhancementStudio.exe
2. Open an image (File > Open)
3. Adjust settings in left panel
4. Save when satisfied (File > Save)

For batch processing, use the Batch Queue panel.
""")

    print(f"Distribution folder created: {dist_path}")
    return dist_path


def run_tests():
    """Run final test suite."""
    print("\nRunning final tests...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode == 0:
            print("All tests passed!")
            return True
        else:
            print("Some tests failed!")
            return False
    except Exception as e:
        print(f"Test run failed: {e}")
        return False


def main():
    """Main build function."""
    print("=" * 60)
    print("IMAGE ENHANCEMENT STUDIO - BUILD SCRIPT")
    print("=" * 60)

    print("\n1. Running tests...")
    if not run_tests():
        print("Tests failed. Aborting build.")
        return False

    print("\n2. Cleaning previous builds...")
    clean_build_dirs()

    print("\n3. Building executable...")
    if not build_executable():
        return False

    print("\n4. Creating distribution...")
    dist_path = create_distribution_folder()

    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print(f"Executable: {dist_path}/ImageEnhancementStudio.exe")
    print("=" * 60)


if __name__ == "__main__":
    main()
