import os
import shutil
from app.simple_graph import SimpleKnowledgeGraph

def test_manual_graph_operations():
    print("Testing manual graph operations...")
    
    # Use a temporary path for testing
    test_path = "data/test_graph.json"
    if os.path.exists(test_path):
        os.remove(test_path)
        
    kg = SimpleKnowledgeGraph(path=test_path)
    
    # Manually add triplets
    kg.add_triplet("Apple", "iPhone", "released")
    kg.add_triplet("iPhone", "2007", "released_in")
    kg.add_triplet("Steve Jobs", "Apple", "founded")
    
    # Test get_neighbors
    neighbors_apple = kg.get_neighbors("Apple", hops=1)
    print(f"Neighbors of Apple (1 hop): {neighbors_apple}")
    assert "iPhone" in neighbors_apple
    assert "Steve Jobs" in neighbors_apple
    
    neighbors_jobs = kg.get_neighbors("Steve Jobs", hops=2)
    print(f"Neighbors of Steve Jobs (2 hops): {neighbors_jobs}")
    assert "iPhone" in neighbors_jobs
    
    # Test save and load
    kg.save_graph()
    assert os.path.exists(test_path)
    
    kg2 = SimpleKnowledgeGraph(path=test_path)
    kg2.load_graph()
    assert len(kg2.graph.nodes) == 4
    
    print("Manual graph operations test passed!")
    
    # Cleanup
    if os.path.exists(test_path):
        os.remove(test_path)

if __name__ == "__main__":
    test_manual_graph_operations()
