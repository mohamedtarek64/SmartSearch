import math
import json
import os
import re

class IREngine:
    def __init__(self, k1=1.5, b=0.75):
        self.index = {}          # term -> {doc_id: frequency}
        self.doc_metadata = {}    # doc_id -> metadata (title, url, etc)
        self.doc_lengths = {}     # doc_id -> token count
        self.avg_doc_len = 0      
        self.num_docs = 0         
        self.k1 = k1
        self.b = b

    def preprocess(self, text):
        """
        Standardizes text using:
        1. Normalization (lowercase)
        2. Tokenization (re.findall)
        3. Stop Word Removal
        4. Stemming (Simple Suffix Removal for academic compliance)
        """
        if not text: return []
        text = str(text).lower()
        words = re.findall(r'[a-z]{2,}', text) 
        
        stop_words = {'the', 'is', 'at', 'on', 'and', 'a', 'an', 'to', 'in', 'of', 'for', 'with', 'it', 'that', 'this', 'from', 'by', 'was', 'were', 'be'}
        
        # Simple Stemming Logic (Suffix Removal)
        stemmed_words = []
        for w in words:
            if w not in stop_words:
                # Basic stemming rules to satisfy the project requirement
                if w.endswith('ies'): w = w[:-3] + 'y'
                elif w.endswith('es'): w = w[:-2]
                elif w.endswith('s') and not w.endswith('ss'): w = w[:-1]
                elif w.endswith('ing'): w = w[:-3]
                elif w.endswith('ed'): w = w[:-2]
                stemmed_words.append(w)
                
        return stemmed_words

    def add_document(self, doc_id, text, metadata):
        """Indexes a document and updates statistics."""
        words = self.preprocess(text)
        if not words: return

        self.num_docs += 1
        self.doc_lengths[doc_id] = len(words)
        self.doc_metadata[doc_id] = metadata

        for word in words:
            if word not in self.index:
                self.index[word] = {}
            self.index[word][doc_id] = self.index[word].get(doc_id, 0) + 1

        total_len = sum(self.doc_lengths.values())
        self.avg_doc_len = total_len / self.num_docs

    def search(self, query, top_n=10):
        """Returns ranked results using the BM25 algorithm."""
        query_words = self.preprocess(query)
        scores = {}

        if not query_words or self.num_docs == 0:
            return []

        for word in query_words:
            if word not in self.index:
                continue

            # IDF calculation
            df = len(self.index[word])
            idf = math.log((self.num_docs - df + 0.5) / (df + 0.5) + 1.0)

            # Accumulate BM25 scores for each document containing the word
            for doc_id, tf in self.index[word].items():
                d_len = self.doc_lengths[doc_id]
                
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (d_len / self.avg_doc_len))
                
                if doc_id not in scores: scores[doc_id] = 0
                scores[doc_id] += idf * (numerator / denominator)

        # Sort and format top results
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return [{
            "id": f"REF-{doc_id[:6].upper()}",
            "score": round(score, 2),
            "metadata": self.doc_metadata.get(doc_id, {})
        } for doc_id, score in sorted_results]

    def save_index(self, path="index.json"):
        """Persists the search index to a JSON file."""
        data = {
            "index": self.index,
            "metadata": self.doc_metadata,
            "lengths": self.doc_lengths,
            "avg_len": self.avg_doc_len,
            "num_docs": self.num_docs
        }
        with open(path, 'w') as f:
            json.dump(data, f)

    def load_index(self, path="index.json"):
        """Loads index from disk."""
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    self.index = data["index"]
                    self.doc_metadata = data["metadata"]
                    self.doc_lengths = data["lengths"]
                    self.avg_doc_len = data["avg_len"]
                    self.num_docs = data["num_docs"]
                return True
            except:
                return False
        return False
