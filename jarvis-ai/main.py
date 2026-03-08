import uvicorn
import threading
from server.api_server import app
from phone.telegram_bot import start_telegram_bot_sync

def start_telegram_thread():
    print("-> Connecting Fietao to Mobile via Telegram...")
    telegram_thread = threading.Thread(target=start_telegram_bot_sync, daemon=True)
    telegram_thread.start()

if __name__ == "__main__":
    print("========================================")
    print("   Fietao AI System Core Initializing   ")
    print("========================================")
    print("-> Loading Plugins: Antigravity... OK")
    start_telegram_thread()
    print("-> Dashboard will be available at: http://localhost:3000")
    print("========================================")
    uvicorn.run(app, host="127.0.0.1", port=3000)
