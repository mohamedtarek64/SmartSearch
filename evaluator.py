import os
import json
from engine import IREngine

def run_evaluation():
    engine = IREngine()
    if os.path.exists("index.json"):
        engine.load_index("index.json")
    else:
        print("Index not found. Please run data_collector.py first.")
        return

    # Dynamic Ground Truth: Keywords that SHOULD appear in relevant documents
    # This is more robust for a live web scraping system than fixed IDs
    ground_truth = {
        "Artificial Intelligence": ["ai", "intelligence", "neural", "learning"],
        "Space Exploration": ["nasa", "moon", "space", "artemis", "orbit"],
        "Modern Technology": ["tech", "digital", "software", "innovation"],
        "Future Science": ["research", "discovery", "scientist", "breakthrough"]
    }

    print("\n" + "="*60)
    print("      IR SYSTEM EVALUATION REPORT (BM25 Engine)")
    print("="*60)
    print(f"{'Query Topic':<25} | {'Prec.':<6} | {'Recall':<6} | {'F1'}")
    print("-" * 60)

    total_precision = 0
    total_recall = 0
    num_queries = len(ground_truth)

    for query, relevant_keywords in ground_truth.items():
        results = engine.search(query, top_k=10)
        
        # A document is considered "relevant" if it contains any of the target keywords
        # in its title or snippet.
        tp = 0
        for res in results:
            title = res["metadata"].get("title", "").lower()
            snippet = res["metadata"].get("snippet", "").lower()
            if any(kw.lower() in title or kw.lower() in snippet for kw in relevant_keywords):
                tp += 1
        
        # Metrics Calculation
        # Precision: % of retrieved docs that are relevant
        precision = tp / len(results) if len(results) > 0 else 0
        
        # Recall: Since we don't have a fixed total of relevant docs in a live system,
        # we assume a baseline of 5 relevant docs per topic for this evaluation.
        assumed_relevant_total = 5 
        recall = tp / assumed_relevant_total if assumed_relevant_total > 0 else 0
        
        # F1 Score
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        total_precision += precision
        total_recall += recall
        
        print(f"{query:<25} | {precision:<6.2f} | {recall:<6.2f} | {f1:.2f}")

    avg_p = total_precision / num_queries
    avg_r = total_recall / num_queries
    
    print("-" * 60)
    print(f"{'AVERAGE SYSTEM METRICS':<25} | {avg_p:<6.2f} | {avg_r:<6.2f} | {(2*avg_p*avg_r)/(avg_p+avg_r) if (avg_p+avg_r)>0 else 0:.2f}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_evaluation()
