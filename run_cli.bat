@echo off
title Image Enhancement Studio - CLI
cd /d "%~dp0"

if "%~1"=="" (
    echo Usage: run_cli.bat input_path -o output_path [-p preset]
    echo.
    echo Examples:
    echo   run_cli.bat photo.jpg -o enhanced.jpg --preset auto
    echo   run_cli.bat photos/ -o output/ --preset professional
    echo.
    echo Presets: auto, professional, denoise
    pause
    exit /b 1
)

.\venv\Scripts\python scripts/cli.py %*
pause
