@echo off
echo =========================================
echo    Jarvis AI System - Setup Script
echo =========================================
echo.
echo Installing Python dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Installing Playwright browsers for Browser Engine...
playwright install

echo.
echo -----------------------------------------
echo IMPORTANT: Next Steps
echo -----------------------------------------
echo 1. Ensure you have Ollama installed from https://ollama.com
echo 2. Download the recommended models manually if needed:
echo    - ollama run llama3.1:8b
echo    - ollama run qwen2.5-coder:7b
echo.
echo Setup Complete! 
echo Run the system by double-clicking main.py or running `python main.py`
pause
