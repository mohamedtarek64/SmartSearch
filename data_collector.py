import os
import hashlib
from engine import IREngine
from scraper import get_all_diverse_data

INDEX_FILE = "index.json"

def run_automated_pipeline():
    """
    Direct Index Update Pipeline:
    Scrapes fresh news data and updates the Inverted Index directly.
    """
    engine = IREngine()
    engine.load_index(INDEX_FILE)
    
    print("--- Scraping Fresh Data for Index Update ---")
    articles = get_all_diverse_data()
    if not articles:
        return

    # Direct Update to index.json
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
            
            engine.add_document(doc_id, content, meta)
            indexed_titles.add(title.lower())
            newly_added += 1

    engine.save_index(INDEX_FILE)
    print(f"--- Index Updated Successfully ---")
    print(f"Newly added to index: {newly_added}")
    print(f"Total searchable documents: {engine.num_docs}")

if __name__ == "__main__":
    run_automated_pipeline()
