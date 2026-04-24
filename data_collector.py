import os
import json
from engine import IREngine
from scraper import get_all_live_data

def run_automated_collection():
    """
    Main entry point for data collection using Web Scraping.
    Builds a fresh index from live web data.
    """
    print("="*50)
    print("SMARTSEARCH: LIVE WEB SCRAPING INITIATED")
    print("="*50)
    
    # Initialize Engine
    engine = IREngine()
    
    # 1. Fetch data via Scraping
    articles = get_all_live_data()
    
    if not articles:
        print("Error: No articles were scraped. Check internet connection.")
        return

    print(f"Success: Scraped {len(articles)} live articles.")
    
    # 2. Index the scraped data
    for i, article in enumerate(articles):
        title = article['title']
        content = article['content']
        
        meta = {
            "title": title,
            "snippet": content[:160] + ("..." if len(content) > 160 else ""),
            "source": "Web Scraper (Live News)",
            "timestamp": "Just now"
        }
        
        engine.add_document(f"scraped_{i}", content, meta)
        
        if i % 10 == 0 and i > 0:
            print(f"Indexed {i} documents...")

    # 3. Save the final index
    engine.save_index("index.json")
    print("\n" + "="*50)
    print("SYSTEM READY: Search index built from live web data!")
    print("="*50)

if __name__ == "__main__":
    run_automated_collection()
