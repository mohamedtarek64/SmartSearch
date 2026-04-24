import re
import os
import math
import string
import json
from collections import defaultdict, Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Ensure NLTK data is available
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
except:
    pass

class IREngine:
    def __init__(self, k1=1.5, b=0.75):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
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
        
        # Lowercase and remove punctuation/numbers
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}0-9]", " ", text)
        
        # Tokenize
        tokens = nltk.word_tokenize(text)
        
        # Filter stop words and short tokens
        cleaned = [t for t in tokens if t not in self.stop_words and len(t) >= 2]
        
        # Stemming (Porter) - more aggressive than lemmatization for IR
        stemmed = [self.stemmer.stem(t) for t in cleaned]
        return stemmed

    def add_document(self, doc_id, text, metadata=None):
        """Index a single document. Merges title into text for better searchability."""
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
        # Update avg length incrementally or recompute at end
        # For now, we'll recompute avgdl in search or save

    def _calculate_avgdl(self):
        if self.num_docs == 0:
            return 0
        return sum(self.doc_lengths.values()) / self.num_docs

    def get_idf(self, term):
        df = len(self.index.get(term, {}))
        if df == 0:
            return 0
        # BM25 IDF formula
        return math.log((self.num_docs - df + 0.5) / (df + 0.5) + 1.0)

    def search(self, query, top_k=10):
        query_terms = self.preprocess(query)
        if not query_terms or self.num_docs == 0:
            return []

        avgdl = self._calculate_avgdl()
        scores = defaultdict(float)
        
        for term in query_terms:
            idf = self.get_idf(term)
            postings = self.index.get(term, {})
            
            for doc_id, freq in postings.items():
                doc_id = str(doc_id) # Ensure doc_id is string for consistent dict keys
                dl = self.doc_lengths.get(int(doc_id) if doc_id.isdigit() else doc_id, 1)
                
                # BM25 formula
                numerator = freq * (self.k1 + 1)
                denominator = freq + self.k1 * (1 - self.b + self.b * (dl / avgdl))
                scores[doc_id] += idf * (numerator / denominator)

        # Sort and return with metadata
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for doc_id, score in ranked:
            metadata = self.doc_metadata.get(doc_id) or self.doc_metadata.get(int(doc_id))
            results.append({
                "id": doc_id,
                "score": round(score, 4),
                "metadata": metadata
            })
        return results

    def save_index(self, filename="index.json"):
        data = {
            "index": self.index,
            "metadata": self.doc_metadata,
            "lengths": self.doc_lengths,
            "num_docs": self.num_docs,
            "k1": self.k1,
            "b": self.b
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
            # Convert length keys to int where possible
            raw_lengths = data.get("lengths", {})
            self.doc_lengths = {}
            for k, v in raw_lengths.items():
                try:
                    self.doc_lengths[int(k)] = v
                except:
                    self.doc_lengths[k] = v
            self.num_docs = data.get("num_docs", 0)
            self.k1 = data.get("k1", 1.5)
            self.b = data.get("b", 0.75)
        return True
