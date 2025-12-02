import os
import shutil
from langchain_core.documents import Document
from app.simple_graph import SimpleKnowledgeGraph
from dotenv import load_dotenv

# Load env vars to get GEMINI_API_KEY
load_dotenv(override=True)

def test_gemini_extraction():
    print("Testing Gemini extraction pipeline...")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("[SKIP] GEMINI_API_KEY not found in env. Skipping test.")
        return
    
    key = os.getenv("GEMINI_API_KEY")
    # print(f"[DEBUG] Loaded GEMINI_API_KEY: {key[:5]}...{key[-5:]}")

    # Use a temporary path for testing
    test_path = "data/test_graph_gemini.json"
    if os.path.exists(test_path):
        os.remove(test_path)
        
    kg = SimpleKnowledgeGraph(path=test_path)
    
    # Test document
    text = "Google DeepMind developed Gemini, a multimodal AI model."
    doc = Document(page_content=text)
    
    # Process document (this calls the LLM)
    kg.process_document(doc)
    
    # Verify results
    neighbors = kg.get_neighbors("Gemini", hops=1)
    print(f"Neighbors of Gemini: {neighbors}")
    
    # We expect 'Google DeepMind' or 'multimodal AI model' to be related
    assert len(neighbors) > 0
    
    print("Gemini extraction test passed!")
    
    # Cleanup
    if os.path.exists(test_path):
        os.remove(test_path)

if __name__ == "__main__":
    test_gemini_extraction()
