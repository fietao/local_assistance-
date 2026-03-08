# Fietao AI 2.0 Roadmap & Development Phases

## Phase 1: Core Foundation (✅ COMPLETED)

- [x] Establish project folder architecture (`fietao-ai/`)
- [x] Install Python virtual environment (`.venv`) and core dependencies
- [x] Initialize Local AI Models via Ollama (`qwen2.5-coder:7b`, `llama3.1:8b`)
- [x] Create foundational FastAPI server (`main.py` -> `api_server.py`)
- [x] Build Holographic Dashboard UI at `http://127.0.0.1:3000`

## Phase 2: Core Brain & Senses (⏳ IN PROGRESS)

- [x] **Brain / Memory**: Upgrade local memory so Fietao maintains conversation history.
- [x] **Vision (Screen Reading)**: Implement OCR using `pytesseract` to allow Fietao to read the user's screen.
- [x] Wire the Vision Module directly into the Dashboard UI.
- [x] **Voice (Speech to Text)**: Implement `SpeechRecognition` so the user can speak to the computer microphone instead of typing.
- [x] **Voice (Text to Speech)**: Add audio playback so Fietao can talk back out loud.

## Phase 3: The Phone (Telegram Integration) 📱 (✅ COMPLETED)

Since Fietao runs on your *local* PC, you need a way to talk to him when you leave the house. We will use Telegram for this.

- [x] Register a new bot on Telegram using "BotFather" to get an API Token.
- [x] Build `phone/telegram_bot.py` using `python-telegram-bot`.
- [x] Wrap the Telegram hook into the FastAPI server so the bot listens 24/7.
- [x] Connect the Mobile Telegram Bot directly to the Local Ollama Brain.

*Result: You will be able to text your computer from your phone while you are at work or outside, and your local AI will respond!*

## Phase 4: Autonomous Operations (Open Interpreter)

- [x] Build the `automation` module using Open Interpreter.
- [x] Give Fietao permission to read local files, create folders, and run scripts on your computer.
- [x] Give Fietao permissions to move the user's physical mouse via `pyautogui` or Playwright.

## Phase 5: Deep Memory (Vector Search)

- [x] Integrate `chromadb` into `memory/vector_db.py`.
- [x] Teach Fietao to digest PDF documents and long-term notes so he remembers you across reboots.

## Phase 6: Browser & Playwright (✅ COMPLETED)

- [x] Build out the `browser` module.
- [x] Teach Fietao to open Chrome autonomously, log into websites, and scrape data for you.
