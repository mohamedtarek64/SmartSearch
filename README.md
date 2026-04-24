# 🔍 SmartSearch: Advanced Information Retrieval System

## 1. Project Overview
**SmartSearch** is a high-performance Information Retrieval (IR) system designed for academic and research environments. It demonstrates the full pipeline of modern search technology, from automated data acquisition to sophisticated ranking algorithms.

## 2. Data Acquisition (Web Scraping)
Unlike static systems, SmartSearch implements a **Dynamic Web Crawler** to ensure data freshness and relevance.
- **Technology**: Built using `BeautifulSoup4` and `Requests` for robust HTML parsing.
- **Automated Workflow**: The `scraper.py` module autonomously navigates news portals (e.g., BBC, Reuters) to extract headlines and summaries.
- **Live Integration**: The system converts unstructured web content into structured metadata for indexing.

## 3. Text Preprocessing Pipeline
To ensure high-quality retrieval, every document passes through an intensive NLP pipeline in `engine.py`:
1.  **Tokenization**: Segmenting raw text into discrete semantic units (Tokens).
2.  **Normalization**: Removing noise (punctuation, numbers) and converting to lowercase.
3.  **Stop-word Removal**: Eliminating high-frequency, low-meaning words (e.g., "is", "the").
4.  **Stemming**: Applying the **Porter Stemmer** to reduce words to their linguistic roots (e.g., "calculating" → "calcul"), improving recall across different word forms.

## 4. Search & Ranking Engine
The core of the system utilizes advanced mathematical models to rank documents by relevance:
- **Inverted Index**: A high-efficiency data structure mapping terms to document locations.
- **BM25 Algorithm (Best Matching 25)**: We upgraded from basic TF-IDF to the BM25 probabilistic model, which is the industry standard for search engines.
- **Parameters**: Standard tuning ($k1=1.5, b=0.75$) accounts for term frequency saturation and document length normalization.

## 5. Web Interface (SaaS Dashboard)
- **Frontend**: A premium "Glassmorphic" dashboard designed with Vanilla CSS for maximum performance.
- **Real-time Analytics**: Displays live stats including document count, unique term density, and average document length.
- **Search Experience**: Features debounced instant search, relevance scoring, and detailed document cards.

## 6. System Evaluation
The effectiveness is measured using `evaluator.py` based on standard IR metrics:
- **Precision**: How many retrieved documents are actually relevant.
- **Recall**: How many of the total relevant documents were successfully found.
- **F1-Score**: The harmonic mean of Precision and Recall.

