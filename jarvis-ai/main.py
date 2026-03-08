import uvicorn
from server.api_server import app

if __name__ == "__main__":
    print("========================================")
    print("   Jarvis AI System Core Initializing   ")
    print("========================================")
    print("-> Loading Plugins: Antigravity... OK")
    print("-> Dashboard will be available at: http://localhost:3000")
    print("========================================")
    uvicorn.run(app, host="0.0.0.0", port=3000)
