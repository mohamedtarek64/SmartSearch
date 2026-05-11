import os
import hashlib
import pandas as pd
from engine import IREngine
from scraper import get_all_diverse_data

INDEX_FILE = "index.json"

def run_automated_pipeline():
    """
    Automated data ingestion pipeline:
    1. Scrape fresh articles.
    2. Save to local CSV archive.
    3. Filter and index unique content.
    4. Save searchable JSON index.
    """
    print("--- Starting Data Ingestion Pipeline ---")
    
    engine = IREngine()
    engine.load_index(INDEX_FILE)
    
    articles = get_all_diverse_data()
    if not articles:
        print("No new data to process.")
        return

    # Update CSV Archive
    df = pd.DataFrame(articles)
    df.to_csv("public_dataset.csv", index=False)
    print(f"Archive updated with {len(articles)} items.")

    # Process and Index (Strict Deduplication by Title)
    indexed_titles = {meta.get("title", "").lower().strip() for meta in engine.doc_metadata.values()}
    newly_added = 0

    for art in articles:
        title = str(art.get("title", "No Title")).strip()
        url = str(art.get("url", "#"))
        
        if title.lower() not in indexed_titles and url != "#":
            doc_id = hashlib.md5(url.encode()).hexdigest()
            content = str(art.get("content", ""))
            
            meta = {
                "title": title,
                "url": url,
                "source": str(art.get("source", "Web")),
                "snippet": content[:150] + "...",
                "timestamp": "Recently Indexed"
            }
            
            engine.add_document(doc_id, content, meta)
            indexed_titles.add(title.lower())
            newly_added += 1

    engine.save_index(INDEX_FILE)
    
    print(f"--- Pipeline Finished ---")
    print(f"Newly Indexed: {newly_added}")
    print(f"Total searchable documents: {engine.num_docs}")

if __name__ == "__main__":
    run_automated_pipeline()
