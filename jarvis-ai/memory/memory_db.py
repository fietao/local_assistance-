import chromadb
from chromadb.config import Settings
import datetime
import os

class DeepMemory:
    def __init__(self):
        # We will save the memory DB directly in the memory folder so it persists locally
        self.db_path = os.path.join(os.path.dirname(__file__), "chroma_data")
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Get or create our permanent collection for Fietao
        self.collection = self.client.get_or_create_collection(
            name="fietao_long_term_memory",
            metadata={"hnsw:space": "cosine"} # Good for semantic similarity
        )
        
    def memorize(self, text: str, context_source: str = "user_chat"):
        """Saves a piece of information into Fietao's permanent long-term memory."""
        # Generate a unique ID based on timestamp
        doc_id = f"mem_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        try:
            self.collection.add(
                documents=[text],
                metadatas=[{"source": context_source, "timestamp": str(datetime.datetime.now())}],
                ids=[doc_id]
            )
            print(f"[DeepMemory] Safely stored new permanent memory: '{text}'")
            return True
        except Exception as e:
            print(f"[DeepMemory Error] failed to save to ChromaDB: {e}")
            return False

    def recall(self, query: str, n_results: int = 2) -> str:
        """Searches deep memory for facts most relevant to the given query."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Extract only the actual text chunks from memory
            found_memories = results['documents'][0]
            
            if not found_memories:
                return ""
                
            # Combine the memories into a readable format for the Brain
            return "\n".join([f"- {mem}" for mem in found_memories])
            
        except Exception as e:
            print(f"[DeepMemory Error] failed to query ChromaDB: {e}")
            return ""

# Export a single instance to be used by the rest of the application
memory_db = DeepMemory()
