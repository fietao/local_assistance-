import threading
from interpreter import interpreter

class InterpreterAgent:
    def __init__(self, model="ollama/qwen2.5-coder:7b"):
        # Configure open interpreter to use the local Ollama coding model
        interpreter.offline = True
        interpreter.llm.model = model
        interpreter.llm.api_base = "http://localhost:11434"
        
        # INTERACTIVE MODE: Ask user before running code, allow Fietao to ask questions!
        interpreter.auto_run = False
        interpreter.safe_mode = "ask"
        
        # Instruct the system to act gracefully and interactively
        interpreter.system_message += (
            "You are Fietao's autonomous coding module. You have permission to write scripts, "
            "read files, create folders, and run Python code. "
            "CRITICAL RULE: If a user's project request is vague, or you need more information "
            "to write the correct code, you MUST stop and ask the user clarifying questions "
            "before proceeding with writing the code."
        )
        
        self.is_running = False

    def execute_action(self, task: str):
        """Runs the open-interpreter agent in a background thread."""
        if self.is_running:
            return "Fietao's coding hands are already busy executing another task!"
            
        def _run_interpreter():
            self.is_running = True
            try:
                print(f"\\n================================================")
                print(f"[Fietao Auto-Coder] Starting Task: {task}")
                print(f"WARNING: I will ask you for permission in this terminal before executing code.")
                print(f"================================================\\n")
                
                # This spins up the interactive interpreter loop in the terminal
                interpreter.chat(task)
                
                print("\\n[Fietao Auto-Coder] Task Completed.\\n")
            except Exception as e:
                print(f"\\n[Fietao Auto-Coder Error] {e}\\n")
            finally:
                self.is_running = False
                
        # Start in background so dashboard API doesn't hang
        threading.Thread(target=_run_interpreter, daemon=True).start()
        
        return (
            f"I have started the autonomous coding agent for task: '{task}'. "
            f"Please check your VS Code Terminal— I will be writing code there and I will "
            f"pause to ask you for permission before I run any scripts!"
        )

agent = InterpreterAgent()
