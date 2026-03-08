import ollama
from memory.memory_db import memory_db

class BrainClient:
    def __init__(self, default_model: str = "llama3.1:8b", coder_model: str = "qwen2.5-coder:7b"):
        self.default_model = default_model
        self.coder_model = coder_model
        
        # Give Fietao a personality
        self.system_prompt = {
            'role': 'system',
            'content': "You are Fietao, a highly advanced local AI assistant. You are concise, highly intelligent, and helpful. You manage the user's local computer systems. You have access to deep persistent memory."
        }
        
        # Initialize conversation memory
        self.conversation_history = [self.system_prompt]

    def _extract_and_store_memory(self, user_prompt: str):
        """Silently analyzes the prompt to determine if there is a permanent fact to save."""
        # A very lightweight LLM check to see if we should write to ChromaDB
        check_prompt = f"Does the following user statement contain a permanent personal fact, preference, or important detail to remember about the user? Only answer with 'YES' or 'NO'. \\nStatement: '{user_prompt}'"
        try:
            decision = ollama.chat(model=self.coder_model, messages=[{"role": "user", "content": check_prompt}])
            if "YES" in decision['message']['content'].upper():
                # Ask it to summarize the fact clearly
                summary_prompt = f"Summarize the core fact about the user from this text in one short sentence: '{user_prompt}'"
                fact = ollama.chat(model=self.coder_model, messages=[{"role": "user", "content": summary_prompt}])
                
                # Save it permanently to our Vector Database!
                memory_db.memorize(fact['message']['content'])
        except Exception as e:
            print(f"[Brain] Memory storage check failed: {e}")


    def think(self, prompt: str, requires_coding: bool = False):
        """
        Sends a prompt to the local Ollama instance, maintaining conversational memory.
        """
        model_to_use = self.coder_model if requires_coding else self.default_model
        
        # 1. Silently check if we should memorize this new information
        self._extract_and_store_memory(prompt)
        
        # 2. Recall any deeply relevant facts from ChromaDB
        past_knowledge = memory_db.recall(prompt)
        
        if past_knowledge:
            # Inject the deep memories into the thought process
            enriched_prompt = f"[SYSTEM MEMORY RECALL: Based on your deep long-term memory, here are facts that might be relevant to the user's current request:\\n{past_knowledge}]\\n\\nUser Request: {prompt}"
        else:
            enriched_prompt = prompt
        
        # Add user's enriched prompt to history
        self.conversation_history.append({'role': 'user', 'content': enriched_prompt})
        
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
