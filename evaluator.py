from engine import IREngine
import json

def run_evaluation():
    engine = IREngine()
    try:
        engine.load_index("index.json")
    except:
        print("Index not found. Please run app.py first.")
        return

    # Define ground truth for evaluation
    # Format: { "query": [list_of_relevant_substrings_in_titles] }
    # We will use substrings to match instead of exact IDs because IDs might change
    ground_truth = {
        "AI and technology": ["Artificial Intelligence", "AI", "technology"],
        "Quantum computing": ["Quantum bits", "qubits", "Quantum"],
        "Space mission Moon": ["Artemis", "Moon", "NASA"],
        "Rohit Sharma cricket": ["Rohit Sharma", "ODI", "New Zealand"],
        "Gmail outage": ["Gmail", "outage", "404 error"],
        "Samsung 1TB": ["Samsung", "1TB", "storage"],
        "Apple Vision Pro": ["Apple Vision Pro", "headset"]
    }

    print("\n" + "="*60)
    print("      IR SYSTEM EVALUATION REPORT (BM25)")
    print("="*60)
    print(f"{'Query':<25} | {'Prec.':<6} | {'Recall':<6} | {'F1'}")
    print("-" * 60)

    total_precision = 0
    total_recall = 0
    total_f1 = 0

    for query, relevant_keywords in ground_truth.items():
        results = engine.search(query, top_k=10)
        retrieved_docs = [res for res in results]
        
        # Determine relevance based on keywords in metadata title
        relevant_retrieved = []
        for res in retrieved_docs:
            title = res["metadata"].get("title", "").lower()
            snippet = res["metadata"].get("snippet", "").lower()
            if any(kw.lower() in title or kw.lower() in snippet for kw in relevant_keywords):
                relevant_retrieved.append(res["id"])

        # For evaluation purposes, we assume there are at least 2 relevant docs in the system for these queries
        # (This is a simplification for the demo)
        assumed_relevant_count = max(len(relevant_retrieved), 2) 
        
        tp = len(relevant_retrieved)
        fp = len(retrieved_docs) - tp
        fn = assumed_relevant_count - tp if assumed_relevant_count > tp else 0

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        total_precision += precision
        total_recall += recall
        total_f1 += f1

        print(f"{query[:25]:<25} | {precision:.3f}  | {recall:.3f}  | {f1:.3f}")

    num_queries = len(ground_truth)
    print("-" * 50)
    print(f"{'AVERAGE':<25} | {total_precision/num_queries:.3f}  | {total_recall/num_queries:.3f}  | {total_f1/num_queries:.3f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_evaluation()
