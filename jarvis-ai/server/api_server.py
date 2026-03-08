from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from brain.ollama_client import brain
from vision.screen_capture import vision
from voice.microphone_listener import voice
from automation.interpreter_agent import agent

app = FastAPI(title="Fietao AI API", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    requires_coding: bool = False
    speak_response: bool = False

@app.get("/")
def read_root():
    html_content = """
    <html>
        <head>
            <title>Fietao Dashboard</title>
            <style>
                body { background-color: #0b0c10; color: #66fcf1; font-family: 'Courier New', Courier, monospace; padding: 40px; }
                h1 { border-bottom: 2px solid #45a29e; padding-bottom: 15px; }
                .panel { background-color: #1f2833; border: 1px solid #45a29e; padding: 20px; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
                .panel h3 { color: #c5c6c7; margin-top: 0; }
                .chat-box { height: 200px; overflow-y: auto; background: #0b0c10; padding: 10px; margin-bottom: 10px; border: 1px solid #45a29e; border-radius: 4px;}
                input { width: 75%; padding: 10px; background: #0b0c10; color: #c5c6c7; border: 1px solid #45a29e; border-radius: 4px; }
                button { padding: 10px 20px; background: #45a29e; color: #0b0c10; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-left: 5px; }
                button:hover { background: #66fcf1; }
                .action-btns { margin-top: 10px; }
                .action-btns button { margin-right: 10px; margin-left: 0; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <h1>Fietao Holographic Dashboard</h1>
            <p>System Status: <b style="color: #66fcf1;">ONLINE</b></p>
            
            <div class="panel" style="border-color: #ffcc00;">
                <h3>🧠 AI Thoughts & Senses</h3>
                <div class="chat-box" id="chat-box">
                    <p style="margin: 0; color: #66fcf1;">Fietao is online and listening...</p>
                </div>
                <input type="text" id="chat-input" placeholder="Give Fietao a command or ask a question..." onkeypress="if(event.key === 'Enter') sendMessage()">
                <button onclick="sendMessage(null, false, false)">Send to Brain</button>
                
                <div class="action-btns">
                    <button style="background-color: #c5c6c7;" onclick="triggerVision()">👁️ Instruct AI to Read Screen</button>
                    <button style="background-color: #ffcc00; color: #000;" onclick="triggerVoice()">🎤 Voice: Listen & Speak</button>
                    <button style="background-color: #dc3545; color: #fff;" onclick="triggerAutomation()">🦾 Run Autonomous Interpreter Action</button>
                </div>
                
                <script>
                    async function sendMessage(overrideText = null, speakResponse = false, requiresCoding = false) {
                        const input = document.getElementById('chat-input');
                        const chatBox = document.getElementById('chat-box');
                        const message = overrideText || input.value.trim();
                        if (!message) return;
                        
                        // Add User message
                        chatBox.innerHTML += `<p style="margin: 5px 0; color: #c5c6c7;"><b>User:</b> ${message}</p>`;
                        if(!overrideText) input.value = '';
                        chatBox.scrollTop = chatBox.scrollHeight;
                        
                        try {
                            const response = await fetch('/api/chat', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({ message: message, requires_coding: requiresCoding, speak_response: speakResponse })
                            });
                            const data = await response.json();
                            
                            // Format response replacing newlines with <br> for HTML
                            const formattedReply = data.reply.replace(/\\n/g, '<br>');
                            chatBox.innerHTML += `<p style="margin: 10px 0; color: #ffcc00;"><b>Fietao:</b> ${formattedReply}</p>`;
                            chatBox.scrollTop = chatBox.scrollHeight;
                        } catch (error) {
                            chatBox.innerHTML += `<p style="margin: 5px 0; color: #ff0000;"><b>System Error:</b> Cannot connect to API!</p>`;
                        }
                    }

                    function triggerVision() {
                        const loadingMsg = "Please take a screenshot using your vision module and analyze what is on my screen right now.";
                        sendMessage(loadingMsg, false, false);
                    }
                    
                    async function triggerVoice() {
                        const chatBox = document.getElementById('chat-box');
                        chatBox.innerHTML += `<p style="margin: 5px 0; color: #ffcc00;"><b>[System] Listening to your microphone... Speak now!</b></p>`;
                        chatBox.scrollTop = chatBox.scrollHeight;
                        
                        try {
                            const response = await fetch('/api/listen');
                            const data = await response.json();
                            
                            if (data.text.startsWith("(")) {
                                chatBox.innerHTML += `<p style="margin: 5px 0; color: #c5c6c7;"><b>System:</b> ${data.text}</p>`;
                            } else {
                                sendMessage(data.text, true, false);
                            }
                        } catch (err) {
                            chatBox.innerHTML += `<p style="margin: 5px 0; color: #ff0000;"><b>Microphone Error:</b> Could not access local mic.</p>`;
                        }
                    }
                    
                    function triggerAutomation() {
                        const input = document.getElementById('chat-input');
                        const message = input.value.trim();
                        if (!message) {
                            alert("Please type a command in the box first! (e.g. 'Open the calculator app')");
                            return;
                        }
                        // Send as autonomous action (requires_coding = true)
                        sendMessage(message, false, true);
                    }
                </script>
            </div>
            
            <div class="panel">
                <h3>📜 Task History & Execution</h3>
                <p>Check the server terminal logs to see live Python code generated and executed by Open Interpreter.</p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/chat")
def chat_with_fietao(req: ChatRequest):
    """Passes the chat request from the UI straight to the Ollama Brain."""
    
    # Check if the user is asking strictly for the autonomous Open Interpreter Module
    if req.requires_coding:
        # Trigger the python autonomous script writer via background thread
        response = agent.execute_action(req.message)
        return {"reply": response}
    
    # Check if the user is asking the vision module to look at the screen
    if "analyze what is on my screen" in req.message.lower() or "look at my screen" in req.message.lower():
        # Inject the OCR text from the UI tool
        seen_text = vision.read_text_from_screen()
        modified_prompt = f"{req.message}\n\n[SYSTEM INJECTION: The Vision module just took a screenshot. The text visible on the user's screen right now is: '{seen_text}'. Respond to the user naturally based on what you saw.]"
        response = brain.think(prompt=modified_prompt, requires_coding=False)
    else:
        # Standard brain chat
        response = brain.think(prompt=req.message, requires_coding=False)
        
    # Trigger speaker if requested (e.g., from the Voice button)
    if req.speak_response:
        voice.speak(response)
        
    return {"reply": response}

@app.get("/api/listen")
def listen_to_mic():
    """Triggers the physical microphone listener on the server machine."""
    text = voice.listen()
    return {"text": text}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Fietao API Layer is active."}
