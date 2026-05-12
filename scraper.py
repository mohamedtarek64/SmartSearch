import requests
from bs4 import BeautifulSoup
import feedparser
import time
import os
import re

def clean_text(text):
    """Deep cleans text by removing HTML artifacts and special characters."""
    if not text: return ""
    text = re.sub(r'(&#?\w+;)', ' ', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
    return " ".join(text.split()).strip()

def scrape_rss_feed(url, source_name):
    """Fetches and cleans entries from a specific RSS feed."""
    print(f"Scraping: {source_name}...")
    articles = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = clean_text(entry.title)
            desc = entry.get('summary', entry.get('description', ''))
            content = clean_text(BeautifulSoup(desc, 'html.parser').get_text())
            
            if len(title) > 10 and len(content) > 20:
                articles.append({
                    "title": title,
                    "content": content,
                    "url": entry.link,
                    "source": source_name
                })
    except Exception:
        pass 
    return articles



def get_all_diverse_data():
    """Aggregates data from global RSS sources and local storage."""
    all_data = []
    
    # Mega List of High-Quality Global Sources
    sources = [
        ("https://www.wired.com/feed/rss", "Wired"),
        ("https://feeds.bbci.co.uk/news/technology/rss.xml", "BBC Tech"),
        ("https://feeds.bbci.co.uk/news/science_and_environment/rss.xml", "BBC Science"),
        ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC World"),
        ("https://hnrss.org/frontpage", "Hacker News"),
        ("http://rss.cnn.com/rss/cnn_tech.rss", "CNN Tech"),
        ("https://www.theverge.com/rss/index.xml", "The Verge"),
        ("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "NYT Tech"),
        ("https://www.nasa.gov/rss/dyn/breaking_news.rss", "NASA"),
        ("https://feeds.feedburner.com/TechCrunch/", "TechCrunch"),
        ("https://www.zdnet.com/news/rss.xml", "ZDNet"),
        ("https://www.technologyreview.com/feed/", "MIT Tech"),
        ("https://www.engadget.com/rss.xml", "Engadget"),
        ("https://www.gizmodo.com/rss", "Gizmodo"),
        ("https://www.techradar.com/rss", "TechRadar"),
        ("https://www.extremetech.com/feed", "ExtremeTech"),
        ("https://arstechnica.com/feed/", "Ars Technica"),
        ("https://www.reutersagency.com/feed/?best-topics=technology&post_type=best", "Reuters Tech"),
        ("https://www.forbes.com/technology/feed/", "Forbes Tech"),
        ("https://www.independent.co.uk/tech/rss", "Independent Tech"),
        ("https://www.theguardian.com/world/rss", "The Guardian World"),
        ("https://www.nature.com/nature.rss", "Nature Journal"),
        ("https://www.scientificamerican.com/section/news/rss/", "Scientific American"),
        ("https://mashable.com/feeds/rss/all", "Mashable"),
        ("https://www.cnet.com/rss/news/", "CNET News"),
        ("https://www.digitaltrends.com/feed/", "Digital Trends"),
        ("https://venturebeat.com/feed/", "VentureBeat"),
        ("https://www.slashdot.org/index.rss", "Slashdot"),
        ("https://www.computerworld.com/index.rss", "Computerworld"),
        ("https://www.infoworld.com/index.rss", "InfoWorld"),
        ("https://www.pcworld.com/index.rss", "PCWorld"),
        ("https://www.macworld.com/index.rss", "Macworld"),
        ("https://www.techadvisor.com/feed/", "Tech Advisor"),
        ("https://www.techmeme.com/feed.xml", "TechMeme"),
        ("https://www.science.org/rss/news_current.xml", "Science Magazine"),
        ("https://api.quantamagazine.org/feed/", "Quanta Magazine"),
        ("https://www.popsci.com/feed/", "Popular Science"),
        ("https://www.gutenberg.org/cache/epub/feeds/pg_new.rss", "Project Gutenberg")
    ]
    
    for url, name in sources:
        all_data.extend(scrape_rss_feed(url, name))
        time.sleep(0.05)


    # Final Deduplication by URL
    unique_data = []
    seen_urls = set()
    for item in all_data:
        if item['url'] not in seen_urls:
            unique_data.append(item)
            seen_urls.add(item['url'])

    return unique_data

if __name__ == "__main__":
    data = get_all_diverse_data()
    print(f"Total articles aggregated: {len(data)}")
