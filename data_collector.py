import os
import hashlib
import pandas as pd
from engine import IREngine

INDEX_FILE = "index.json"

def run_automated_pipeline():
    if not os.path.exists("public_dataset.csv"):
        print("Error: public_dataset.csv not found.")
        return

    print("--- Rebuilding Index from Local CSV Dataset ---")
    engine = IREngine()
    
    # Load current dataset
    df = pd.read_csv("public_dataset.csv")
    articles = df.to_dict('records')
    
    indexed_count = 0
    for art in articles:
        title = str(art.get("title", "No Title")).strip()
        url = str(art.get("url", "#"))
        doc_id = hashlib.md5(url.encode()).hexdigest()
        content = str(art.get("content", ""))
        
        # Minimal metadata for JSON (Search Index)
        meta = {
            "title": title,
            "url": url,
            "source": str(art.get("source", "Archive"))
        }
        
        engine.add_document(doc_id, content, meta)
        indexed_count += 1

    engine.save_index(INDEX_FILE)
    print(f"--- Sync Finished ---")
    print(f"Total documents indexed: {indexed_count}")

if __name__ == "__main__":
    run_automated_pipeline()
