from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Jarvis AI API", version="1.0.0")

@app.get("/")
def read_root():
    html_content = """
    <html>
        <head>
            <title>Jarvis Dashboard</title>
            <style>
                body { background-color: #0b0c10; color: #66fcf1; font-family: 'Courier New', Courier, monospace; padding: 40px; }
                h1 { border-bottom: 2px solid #45a29e; padding-bottom: 15px; }
                .panel { background-color: #1f2833; border: 1px solid #45a29e; padding: 20px; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
                .panel h3 { color: #c5c6c7; margin-top: 0; }
            </style>
        </head>
        <body>
            <h1>Jarvis Holographic Dashboard</h1>
            <p>System Status: <b style="color: #66fcf1;">ONLINE</b></p>
            
            <div class="panel" style="border-color: #ffcc00;">
                <h3>🧠 AI Thoughts (Ollama + Llama3.1)</h3>
                <p>Waiting for context or command...</p>
            </div>
            
            <div class="panel">
                <h3>👁️ Live Screen Vision</h3>
                <p>Vision Loop: Active (Waiting for frame capture)</p>
            </div>
            
            <div class="panel">
                <h3>📜 Task History & Execution</h3>
                <p>No active tasks currently executed by Open Interpreter.</p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Jarvis API Layer is active."}
