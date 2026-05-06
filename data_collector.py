import os
import json
import hashlib
from engine import IREngine
from scraper import get_all_diverse_data

INDEX_FILE = "index.json"

def make_fingerprint(article):
    """Create a stable key to detect duplicates across runs."""
    url = (article.get("url") or "").strip().lower()
    if url and url != "#":
        return f"url::{url}"

    title = (article.get("title") or "").strip().lower()
    content = (article.get("content") or "").strip().lower()
    raw = f"{title}|{content[:300]}"
    return f"hash::{hashlib.sha1(raw.encode('utf-8')).hexdigest()}"

def run_automated_collection():
    """
    Main entry point for data collection using Web Scraping, APIs, and Datasets.
    Incrementally updates the index from diverse sources.
    """
    print("="*50)
    print("SMARTSEARCH: MULTI-SOURCE DATA COLLECTION")
    print("="*50)
    
    # Initialize Engine
    engine = IREngine()
    existing_docs = 0
    if os.path.exists(INDEX_FILE) and engine.load_index(INDEX_FILE):
        existing_docs = engine.num_docs
        print(f"Loaded existing index with {existing_docs} documents.")
    
    # 1. Fetch data from all sources (News, Reddit, Books, Datasets)
    articles = get_all_diverse_data()
    
    if not articles:
        print("Error: No articles were scraped. Check internet connection.")
        return

    print(f"Success: Scraped {len(articles)} live articles.")

    existing_fingerprints = set()
    for meta in engine.doc_metadata.values():
        url = (meta.get("url") or "").strip().lower()
        if url and url != "#":
            existing_fingerprints.add(f"url::{url}")

        title = (meta.get("title") or "").strip().lower()
        snippet = (meta.get("snippet") or "").strip().lower()
        if title or snippet:
            raw = f"{title}|{snippet[:300]}"
            existing_fingerprints.add(f"hash::{hashlib.sha1(raw.encode('utf-8')).hexdigest()}")
    
    # 2. Index the scraped data
    added_count = 0
    skipped_count = 0

    for article in articles:
        fingerprint = make_fingerprint(article)
        if fingerprint in existing_fingerprints:
            skipped_count += 1
            continue

        title = article['title']
        content = article['content']
        
        meta = {
            "title": title,
            "snippet": content[:160] + ("..." if len(content) > 160 else ""),
            "source": article.get("source", "Diverse Web"),
            "url": article.get("url", "#"),
            "timestamp": "Just now"
        }
        
        new_doc_id = f"scraped_{engine.num_docs}"
        engine.add_document(new_doc_id, content, meta)
        existing_fingerprints.add(fingerprint)
        added_count += 1
        
        if added_count % 10 == 0:
            print(f"Indexed {added_count} new documents...")

    print(f"Skipped duplicates: {skipped_count}")
    print(f"Added new documents: {added_count}")
    print(f"Total documents now: {engine.num_docs}")

    # 3. Save the final index
    engine.save_index(INDEX_FILE)
    print("\n" + "="*50)
    print("SYSTEM READY: Search index updated from live web data!")
    print("="*50)

if __name__ == "__main__":
    run_automated_collection()
