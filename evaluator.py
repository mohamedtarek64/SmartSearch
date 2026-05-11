import os
import time
from engine import IREngine

def run_performance_test():
    """Evaluates search engine speed and result quality."""
    engine = IREngine()
    
    if not os.path.exists("index.json"):
        print("Error: index.json not found. Run the ingestion pipeline first.")
        return
    
    engine.load_index("index.json")
    
    print("\n" + "="*55)
    print("      SMARTSEARCH PRO - SYSTEM PERFORMANCE REPORT")
    print("="*55)

    # Test queries across different domains
    test_queries = [
        "Artificial Intelligence", 
        "Space Exploration", 
        "Global Technology", 
        "Scientific Research"
    ]

    for query in test_queries:
        start_time = time.perf_counter()
        results = engine.search(query, top_n=5)
        end_time = time.perf_counter()
        
        latency = (end_time - start_time) * 1000
        
        print(f"\nQuery: '{query}'")
        print(f"Status: Found {len(results)} items")
        print(f"Latency: {latency:.2f}ms")
        
        for i, res in enumerate(results):
            title = res['metadata'].get('title', 'Unknown Title')
            print(f"  [{i+1}] {title[:65]}...")

    print("\n" + "="*55)
    print(f"Total Indexed Documents: {engine.num_docs}")
    print("Engine Status: ACTIVE & OPTIMIZED")
    print("="*55 + "\n")

if __name__ == "__main__":
    run_performance_test()
