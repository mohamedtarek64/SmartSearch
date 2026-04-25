import requests
from bs4 import BeautifulSoup
import feedparser
import pandas as pd
import time
import json
import os

def scrape_rss_feed(url, source_name):
    """
    General function to fetch data from RSS feeds (Reliable and fast).
    Works for: News sites, Reddit, etc.
    """
    print(f"📡 Fetching from {source_name} (RSS)...")
    articles = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            # Some feeds use 'description', others 'summary'
            content = entry.get('summary', entry.get('description', ''))
            # Clean HTML from content if any
            clean_content = BeautifulSoup(content, 'html.parser').get_text()
            
            articles.append({
                "title": title,
                "content": clean_content,
                "url": entry.link,
                "source": source_name,
                "type": "Live News/Feed"
            })
        print(f"✅ Success: Found {len(articles)} entries in {source_name}.")
        return articles
    except Exception as e:
        print(f"❌ Failed to fetch {source_name}: {e}")
        return []

def fetch_reddit_data(subreddit="technology"):
    """Reddit can be accessed via RSS without an API key for public data."""
    url = f"https://www.reddit.com/r/{subreddit}/.rss"
    # Reddit RSS requires a custom User-Agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SmartSearch/1.0'}
    try:
        response = requests.get(url, headers=headers)
        feed = feedparser.parse(response.content)
        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "content": BeautifulSoup(entry.summary, 'html.parser').get_text(),
                "url": entry.link,
                "source": f"Reddit (r/{subreddit})",
                "type": "Social Media"
            })
        return articles
    except:
        return []

def load_public_datasets():
    """
    Simulates loading from public datasets (e.g., CSV files from Kaggle).
    We will generate a small internal dataset if no files exist.
    """
    print("📂 Loading Public Datasets...")
    dataset_path = "public_dataset.csv"
    
    if os.path.exists(dataset_path):
        try:
            df = pd.read_csv(dataset_path)
            # Assume columns: title, content
            return df.to_dict('records')
        except:
            return []
    else:
        # Generate a small sample dataset for demonstration
        data = [
            {"title": "Global Warming Trends 2024", "content": "Analysis of temperature changes across the Arctic circle.", "source": "Public Dataset", "type": "Science"},
            {"title": "SpaceX Starship Launch Data", "content": "Telemetry data from the latest orbital test flight.", "source": "Public Dataset", "type": "Space"},
            {"title": "Deep Learning Research Paper", "content": "A study on Transformer architectures for NLP tasks.", "source": "Public Dataset", "type": "Education"}
        ]
        return data

def fetch_digitized_books():
    """Project Gutenberg provides an RSS feed for new books."""
    url = "https://www.gutenberg.org/cache/epub/feeds/pg_new.rss"
    return scrape_rss_feed(url, "Project Gutenberg (Books)")

def get_all_diverse_data():
    """Main aggregator for all sources."""
    all_data = []
    
    # 1. News Sites via RSS
    news_sources = [
        ("https://www.wired.com/feed/rss", "Wired"),
        ("https://feeds.bbci.co.uk/news/technology/rss.xml", "BBC Technology"),
        ("https://hnrss.org/frontpage", "Hacker News")
    ]
    
    for url, name in news_sources:
        all_data.extend(scrape_rss_feed(url, name))
        time.sleep(0.5)

    # 2. Social Media (Reddit)
    all_data.extend(fetch_reddit_data("technology"))
    all_data.extend(fetch_reddit_data("science"))

    # 3. Public Datasets
    all_data.extend(load_public_datasets())

    # 4. Digitized Books
    all_data.extend(fetch_digitized_books())

    return all_data

if __name__ == "__main__":
    # Test the scraper
    data = get_all_diverse_data()
    print(f"\nTotal items collected: {len(data)}")
