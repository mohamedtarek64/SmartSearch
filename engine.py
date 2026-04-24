import re
import os
import math
import string
import json
from collections import defaultdict, Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure NLTK data is available
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

class IREngine:
    def __init__(self, k1=1.5, b=0.75):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.index = defaultdict(dict)  # term -> {doc_id: tf}
        self.doc_metadata = {}           # doc_id -> {title, snippet, url}
        self.doc_lengths = {}            # doc_id -> total_tokens
        self.num_docs = 0
        self.k1 = k1
        self.b = b
        self.avg_doc_length = 0

    def preprocess(self, text):
        """Clean and normalize text: Tokenization, Stop Word Removal, Stemming."""
        if not text or not isinstance(text, str):
            return []
        
        text = text.lower()
        # Remove punctuation and numbers
        text = re.sub(f"[{re.escape(string.punctuation)}0-9]", " ", text)
        
        tokens = nltk.word_tokenize(text)
        
        # Filter stop words and keep tokens with length >= 2 (like 'AI')
        cleaned = [t for t in tokens if t not in self.stop_words and len(t) >= 2]
        
        # Stemming (Porter)
        return [self.stemmer.stem(t) for t in cleaned]

    def add_document(self, doc_id, text, metadata=None):
        """Index a single document."""
        doc_id = str(doc_id)
        title = metadata.get("title", "") if metadata else ""
        combined_text = f"{title} {text}"
        
        tokens = self.preprocess(combined_text)
        if not tokens:
            return
            
        self.doc_lengths[doc_id] = len(tokens)
        self.doc_metadata[doc_id] = metadata or {"title": title or f"Doc {doc_id}", "snippet": text[:200]}
        
        term_freq = Counter(tokens)
        for term, freq in term_freq.items():
            self.index[term][doc_id] = freq
        
        self.num_docs += 1

    def _get_avgdl(self):
        if self.num_docs == 0: return 0
        return sum(self.doc_lengths.values()) / self.num_docs

    def search(self, query, top_k=10):
        query_terms = self.preprocess(query)
        if not query_terms or self.num_docs == 0:
            return []

        avgdl = self._get_avgdl()
        scores = defaultdict(float)
        
        for term in query_terms:
            postings = self.index.get(term, {})
            df = len(postings)
            if df == 0: continue
            
            # BM25 IDF
            idf = math.log((self.num_docs - df + 0.5) / (df + 0.5) + 1.0)
            
            for doc_id, freq in postings.items():
                dl = self.doc_lengths.get(doc_id, avgdl)
                # BM25 Scoring Formula
                numerator = freq * (self.k1 + 1)
                denominator = freq + self.k1 * (1 - self.b + self.b * (dl / avgdl))
                scores[doc_id] += idf * (numerator / denominator)

        # Rank and format results
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [{
            "id": doc_id,
            "score": round(score, 4),
            "metadata": self.doc_metadata.get(doc_id, {})
        } for doc_id, score in ranked]

    def save_index(self, filename="index.json"):
        data = {
            "index": self.index,
            "metadata": self.doc_metadata,
            "lengths": self.doc_lengths,
            "num_docs": self.num_docs,
            "k1": self.k1, "b": self.b
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f"Index saved with {self.num_docs} documents.")

    def load_index(self, filename="index.json"):
        if not os.path.exists(filename):
            return False
        with open(filename, 'r') as f:
            data = json.load(f)
            self.index = data.get("index", {})
            self.doc_metadata = data.get("metadata", {})
            self.doc_lengths = data.get("lengths", {})
            self.num_docs = data.get("num_docs", 0)
            self.k1 = data.get("k1", 1.5)
            self.b = data.get("b", 0.75)
        return True
