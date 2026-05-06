from flask import Flask, render_template, request, jsonify
from engine import IREngine
import os

app = Flask(__name__)
engine = IREngine()

# Load the index if it exists
INDEX_FILE = "index.json"
if os.path.exists(INDEX_FILE):
    engine.load_index(INDEX_FILE)
else:
    print("Warning: index.json not found. Please run data_collector.py to populate the search engine.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Return top 10 results
    results = engine.search(query, top_k=10)
    
    # Calculate Real-time Metrics for the demonstration
    query_terms = engine.preprocess(query)
    tp = 0
    if query_terms:
        for res in results:
            content = (res["metadata"].get("title", "") + " " + res["metadata"].get("snippet", "")).lower()
            # If any of the query's main terms are found, consider it relevant
            if any(term in content for term in query_terms):
                tp += 1
    
    precision = tp / len(results) if results else 0
    # For demo purposes, we assume there are at least 5 relevant docs for any meaningful query
    assumed_total_relevant = 5
    recall = min(tp / assumed_total_relevant, 1.0)
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return jsonify({
        "results": results,
        "metrics": {
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1, 2),
            "relevant_found": tp
        }
    })

@app.route('/stats')
def stats():
    # Provide system statistics for the dashboard
    return jsonify({
        "total_docs": engine.num_docs,
        "total_terms": len(engine.index),
        "avg_dl": round(engine._get_avgdl(), 2)
    })

if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts
    app.run(debug=True, port=5001)
