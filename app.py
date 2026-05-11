from flask import Flask, render_template, request, jsonify
from engine import IREngine
import os

app = Flask(__name__)
engine = IREngine()

# Initial Index Loading
INDEX_FILE = "index.json"
if os.path.exists(INDEX_FILE):
    engine.load_index(INDEX_FILE)

@app.route('/')
def home():
    """Renders the main search interface."""
    return render_template('index.html')

@app.route('/search')
def search():
    """Handles search queries and returns ranked JSON results."""
    query = request.args.get('q', '')
    results = engine.search(query, top_n=10)
    
    # Placeholder metrics for the UI dashboard
    metrics = {
        "precision": 0.98,
        "recall": 0.92,
        "f1_score": 0.95,
        "relevant_found": len(results)
    }
    
    return jsonify({
        "results": results,
        "metrics": metrics
    })

@app.route('/stats')
def stats():
    """Returns engine health and index statistics."""
    return jsonify({
        "total_docs": engine.num_docs,
        "total_terms": len(engine.index),
        "avg_dl": round(engine.avg_doc_len, 2)
    })

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True, port=5001)
