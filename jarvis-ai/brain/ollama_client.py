import ollama

class BrainClient:
    def __init__(self, default_model: str = "llama3.1:8b", coder_model: str = "qwen2.5-coder:7b"):
        self.default_model = default_model
        self.coder_model = coder_model
        
        # Give Fietao a personality
        self.system_prompt = {
            'role': 'system',
            'content': "You are Fietao, a highly advanced local AI assistant. You are concise, highly intelligent, and helpful. You manage the user's local computer systems."
        }
        
        # Initialize conversation memory
        self.conversation_history = [self.system_prompt]

    def think(self, prompt: str, requires_coding: bool = False):
        """
        Sends a prompt to the local Ollama instance, maintaining conversational memory.
        """
        model_to_use = self.coder_model if requires_coding else self.default_model
        
        # Add user's prompt to history
        self.conversation_history.append({'role': 'user', 'content': prompt})
        
        # Keep context window manageable (System prompt + last 10 messages)
        if len(self.conversation_history) > 11:
            self.conversation_history = [self.system_prompt] + self.conversation_history[-10:]

        try:
            response = ollama.chat(model=model_to_use, messages=self.conversation_history)
            ai_message = response['message']['content']
            
            # Add AI's response to history
            self.conversation_history.append({'role': 'assistant', 'content': ai_message})
            
            return ai_message
        except Exception as e:
            # Remove the failed user prompt so memory stays intact
            if self.conversation_history[-1]['role'] == 'user':
                self.conversation_history.pop()
            return f"Error connecting to Ollama Brain: {e}"
            
    def clear_memory(self):
        """Wipes the short-term conversation memory."""
        self.conversation_history = [self.system_prompt]

brain = BrainClient()
