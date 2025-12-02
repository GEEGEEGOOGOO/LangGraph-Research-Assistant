# app/simple_graph.py
import networkx as nx
import json
import os
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

# Initialize LLM for extraction
# We will initialize inside the class to ensure env vars are loaded

EXTRACTION_PROMPT = """
You are an expert at extracting knowledge from text.
Extract entities and relationships from the following text.
Return the result as a JSON object with a list of "triplets".
Each triplet should have:
- "source": The source entity
- "target": The target entity
- "relation": The relationship between them

Example:
Text: "Apple released the iPhone in 2007."
Output: {{
    "triplets": [
        {{"source": "Apple", "target": "iPhone", "relation": "released"}},
        {{"source": "iPhone", "target": "2007", "relation": "released_in"}}
    ]
}}

Text: {text}
"""

class SimpleKnowledgeGraph:
    def __init__(self, path: str = "data/graph.json"):
        self.graph = nx.Graph()
        self.path = path
        
        # Initialize LLM
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            print("[INFO] Using Gemini API for graph extraction.")
            self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_api_key, temperature=0)
        else:
            print("[INFO] Using OpenAI API for graph extraction.")
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            
        self.prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)

    def add_triplet(self, source: str, target: str, relation: str):
        """Adds a triplet to the graph."""
        self.graph.add_node(source)
        self.graph.add_node(target)
        self.graph.add_edge(source, target, relation=relation)

    def process_document(self, document: Document):
        """Extracts triplets from a document and adds them to the graph."""
        print(f"[INFO] Processing document: {document.page_content[:50]}...")
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"text": document.page_content})
            # Parse JSON from the response content
            # This is a simplified parsing logic. In production, use structured output parsing.
            content = response.content.strip()
            
            # Clean up markdown code blocks
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            
            if content.endswith("```"):
                content = content[:-3]
                
            content = content.strip()
            
            data = json.loads(content)
            
            for triplet in data.get("triplets", []):
                self.add_triplet(triplet["source"], triplet["target"], triplet["relation"])
            
            print(f"[SUCCESS] Added {len(data.get('triplets', []))} triplets.")
        except Exception as e:
            print(f"[ERROR] Failed to process document: {e}")

    def get_neighbors(self, entity: str, hops: int = 1) -> List[str]:
        """Returns a list of neighboring entities within `hops` distance."""
        if entity not in self.graph:
            return []
        
        neighbors = set()
        current_layer = {entity}
        visited = {entity}
        
        for _ in range(hops):
            next_layer = set()
            for node in current_layer:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_layer.add(neighbor)
                        neighbors.add(neighbor)
            current_layer = next_layer
            
        return list(neighbors)

    def save_graph(self):
        """Saves the graph to a JSON file."""
        data = nx.node_link_data(self.graph)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(data, f)
        print(f"[INFO] Graph saved to {self.path}")

    def load_graph(self):
        """Loads the graph from a JSON file."""
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                data = json.load(f)
            self.graph = nx.node_link_graph(data)
            print(f"[INFO] Graph loaded from {self.path}")
        else:
            print(f"[WARN] Graph file not found at {self.path}, starting empty.")

    def search(self, query: str) -> List[str]:
        """
        Simple search implementation:
        1. Extract entities from query (simplified: just use the query as entity or split)
        2. Find neighbors
        """
        # Simplified entity extraction from query for now
        # In a real app, use the same LLM extraction or keyword matching
        words = query.split()
        results = set()
        for word in words:
            # Try exact match first
            neighbors = self.get_neighbors(word, hops=2)
            results.update(neighbors)
            
            # Try case-insensitive match if needed (not implemented here for speed)
            
        return list(results)
