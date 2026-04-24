import requests
from bs4 import BeautifulSoup
import os
import time

def scrape_news_source(url, source_name):
    print(f"Scraping {source_name}...")
    articles = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for headings which are typically headlines
        for h_tag in soup.find_all(['h1', 'h2', 'h3']):
            title = h_tag.text.strip()
            # Basic heuristic: headlines are usually 5-25 words
            if 20 < len(title) < 200:
                # Try to find a nearby summary
                parent = h_tag.parent
                summary = ""
                # Search for a paragraph in the same container
                p_tag = parent.find('p') or h_tag.find_next('p')
                if p_tag:
                    summary = p_tag.text.strip()
                
                if not summary or len(summary) < 10:
                    summary = "Live headline update from our news crawler."
                
                articles.append({"title": title, "content": summary})

        return articles
    except Exception as e:
        print(f"Failed to scrape {source_name}: {e}")
        return []

def get_all_live_data():
    sources = [
        ("https://www.theverge.com/tech", "The Verge"),
        ("https://www.wired.com/category/science/", "Wired Science"),
        ("https://www.bbc.com/news/technology", "BBC Technology"),
        ("https://news.ycombinator.com/", "Hacker News")
    ]
    
    all_articles = []
    for url, name in sources:
        data = scrape_news_source(url, name)
        all_articles.extend(data)
        time.sleep(1)
        
    return all_articles
