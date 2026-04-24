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
    return jsonify(results)

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
