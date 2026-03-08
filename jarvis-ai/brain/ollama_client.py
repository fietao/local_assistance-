import ollama

class BrainClient:
    def __init__(self, default_model: str = "llama3.1:8b", coder_model: str = "qwen2.5-coder:7b"):
        self.default_model = default_model
        self.coder_model = coder_model

    def think(self, prompt: str, requires_coding: bool = False):
        """
        Sends a prompt to the local Ollama instance.
        """
        model_to_use = self.coder_model if requires_coding else self.default_model
        
        try:
            response = ollama.chat(model=model_to_use, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error connecting to Ollama Brain: {e}"

brain = BrainClient()
