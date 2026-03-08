@echo off
echo =========================================
echo    Fietao AI 2.0 - Universal Setup Script
echo =========================================
echo.

echo 1. Creating Python Virtual Environment...
if not exist ".venv" (
    python -m venv .venv
    echo [OK] Virtual Environment Created.
) else (
    echo [SKIPPED] Virtual environment already exists.
)

echo.
echo 2. Activating .venv and installing Python dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 3. Installing Playwright headless browser component...
playwright install chromium

echo.
echo 4. Creating .env configuration template...
if not exist ".env" (
    echo TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_TOKEN_HERE" > .env
    echo [OK] Created generic .env file. Please put your token in there!
) else (
    echo [SKIPPED] .env file already exists.
)

echo.
echo ==========================================================
echo    [ACTION REQUIRED] MANUAL STEPS FOR THE NEW LAPTOP
echo ==========================================================
echo 1. Install Ollama natively on Windows from: https://ollama.com
echo 2. Open a new command prompt and pull the brains:
echo    - ollama run qwen2.5-coder:7b
echo    - ollama run llama3.1:8b
echo 3. Install Tesseract OCR for Windows (Required for Vision):
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo    (Keep default install path: C:\Program Files\Tesseract-OCR)
echo 4. Edit the hidden ".env" file in this folder and paste your Telegram Token.
echo ==========================================================
echo.
echo Setup Complete! 
echo To launch Fietao on this new machine, either:
echo   A) Run StartAI_bot.bat
echo   B) Run: call .venv\Scripts\activate ^&^& python main.py
echo.
pause
