from flask import Flask, render_template, request, jsonify
from engine import IREngine
import os

app = Flask(__name__)
engine = IREngine()

# Load or Initialize the index
INDEX_FILE = "index.json"
if os.path.exists(INDEX_FILE):
    engine.load_index(INDEX_FILE)
else:
    # Initial Sample Data to get started
    sample_data = [
        ("AI and Medicine", "Artificial Intelligence is revolutionizing diagnosis and surgery in modern hospitals."),
        ("Quantum Computing", "Quantum bits or qubits allow for exponentially faster calculations than classical bits."),
        ("Climate Change 2024", "Rising sea levels and extreme weather patterns are a global concern for the next decade."),
        ("Space Exploration", "NASA's Artemis mission aims to land the first woman and next man on the Moon by 2025."),
        ("Cybersecurity Trends", "Zero-trust architecture is becoming the standard for protecting enterprise data."),
        ("Blockchain Beyond Crypto", "Supply chain tracking and voting systems are new frontiers for blockchain technology."),
        ("The Future of EVs", "Electric vehicles are reaching price parity with gasoline cars due to battery advances."),
        ("Deep Learning in Vision", "Convolutional neural networks have enabled breakthroughs in facial recognition."),
        ("Renewable Energy", "Solar and wind energy costs have dropped by 80% over the last decade."),
        ("The Metaverse", "Virtual and augmented reality are creating new ways for people to interact socially.")
    ]
    for i, (title, content) in enumerate(sample_data):
        engine.add_document(i, content, {"title": title, "snippet": content[:150]})
    engine.save_index(INDEX_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = engine.search(query)
    return jsonify(results)

@app.route('/stats')
def stats():
    return jsonify({
        "total_docs": engine.num_docs,
        "total_terms": len(engine.index),
        "avg_dl": round(engine._calculate_avgdl(), 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
