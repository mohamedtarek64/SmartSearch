import os
import hashlib
import pandas as pd
from engine import IREngine
from scraper import get_all_diverse_data

INDEX_FILE = "index.json"

def run_automated_pipeline():
    """
    Search Engine Sync Pipeline:
    Synchronizes the search engine index with both live web data 
    and the local CSV reference archive.
    """
    engine = IREngine()
    
    # Load existing index if it exists
    if os.path.exists(INDEX_FILE):
        engine.load_index(INDEX_FILE)
    
    print("--- Aggregates data from diverse sources ---")
    # Fetching data from the aggregation pipeline
    articles = get_all_diverse_data()
    if not articles:
        print("No new data identified.")
        return

    # Track currently indexed titles to avoid duplicates
    indexed_titles = {meta.get("title", "").lower().strip() for meta in engine.doc_metadata.values()}
    newly_added = 0

    for art in articles:
        title = str(art.get("title", "No Title")).strip()
        url = str(art.get("url", "#"))
        
        # Deduplication check
        if title.lower() not in indexed_titles and url != "#":
            doc_id = hashlib.md5(url.encode()).hexdigest()
            content = str(art.get("content", ""))
            
            meta = {
                "title": title,
                "url": url,
                "source": str(art.get("source", "Web"))
            }
            
            # Optimization: Index BOTH title and content to improve ranking for exact matches
            engine.add_document(doc_id, f"{title} {content}", meta)
            
            indexed_titles.add(title.lower())
            newly_added += 1

    # Save the updated index back to JSON
    engine.save_index(INDEX_FILE)
    print(f"--- Update Complete ---")
    print(f"Newly indexed items: {newly_added}")
    print(f"Total documents in engine: {engine.num_docs}")

if __name__ == "__main__":
    run_automated_pipeline()
