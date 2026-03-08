@echo off
title Fietao AI - Core Server
echo =======================================
echo     Starting Fietao AI System...
echo =======================================
echo.

:: Ensure we run the exact python executable from the virtual environment
cd /d "%~dp0\jarvis-ai"

:: Check if the virtual environment exists before activating
if exist ".venv\Scripts\activate.bat" (
    echo [Boot Sequence] Virtual environment detected. Activating .venv...
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Could not find the .venv folder. Did you run setup.bat yet?
    pause
    exit
)

echo [Boot Sequence] Initializing Python Core Server...
python main.py

pause