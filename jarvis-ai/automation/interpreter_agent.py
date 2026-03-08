import threading
from interpreter import interpreter

class InterpreterAgent:
    def __init__(self, model="ollama/qwen2.5-coder:7b"):
        # Configure open interpreter to use the local Ollama coding model
        interpreter.offline = True
        interpreter.llm.model = model
        interpreter.llm.api_base = "http://localhost:11434"
        
        # Give full autonomous permissions
        interpreter.auto_run = True
        interpreter.safe_mode = "off"
        
        # Instruct the system to act gracefully
        interpreter.system_message += (
            "You are Fietao's autonomous action module. You have permission to write scripts, "
            "read files, create folders, and run Python code. Also you can control the mouse and keyboard "
            "using standard libraries (pyautogui)."
        )
        
        self.is_running = False

    def execute_action(self, task: str):
        """Runs the open-interpreter agent in a background thread."""
        if self.is_running:
            return "Fietao's action hands are already busy executing another task!"
            
        def _run_interpreter():
            self.is_running = True
            try:
                print(f"[Automation] Starting autonomous task: {task}")
                # This will automatically spin up standard interpreter execution loop in the background!
                interpreter.chat(task)
                print("[Automation] Task Completed.")
            except Exception as e:
                print(f"[Automation Error] {e}")
            finally:
                self.is_running = False
                
        threading.Thread(target=_run_interpreter, daemon=True).start()
        return f"Autonomous agent has started executing: '{task}' in the background."

agent = InterpreterAgent()
