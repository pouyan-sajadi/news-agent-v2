import re
import uuid
import json
from datetime import datetime
from newspaper import Article
import serpapi
from app.config import SERPAPI_KEY, NUM_SOURCES
from app.core.logger import logger
import logging

logger = logging.getLogger(__name__)

def clean_text(text):
    # Remove ASCII control characters and escape remaining ones
    text = re.sub(r'[\x00-\x1F\x7F]', ' ', text)
    text = text.replace('\\', '\\\\').replace('"', '\\"')
    return text.strip()

def fetch_full_article(url):
    logger.debug(f"Attempting to fetch article from URL: {url}")
    try:
        article = Article(url)
        article.download()
        article.parse()
        logger.debug(f"Parsed article from {url}, length={len(article.text)} chars")
        return article.text
    except Exception as e:
        return f"[Failed to fetch full article: {e}]"

def search_news(topic):
    
    logger.debug("Calling SerpAPI...")

    client = serpapi.Client(api_key=SERPAPI_KEY)

    params = {
        "engine": "google",
        "q": f"{topic} news {datetime.now().strftime('%Y-%m')}",
        "tbm": "nws",  
        "num": NUM_SOURCES
    }
    logger.debug(f"Search parameters: {params}")

    try:
        results = client.search(params)
        news_results = results.get("news_results", [])
        logger.info(f"🔍 Found {len(news_results)} results from SerpAPI")
        for i, item in enumerate(news_results):
            logger.info(f"{i+1}. {item.get('title', 'No title')}")

    except Exception as e:
        return f"[Error fetching search results: {e}]"

    if not news_results:
        return f"No news found for {topic}."

    compiled = []
    for item in news_results:
        full_text = fetch_full_article(item.get("link", ""))
        compiled.append({
            "id": str(uuid.uuid4()),  
            "title": item.get("title", "").strip(),
            "source": item.get("source", "").strip(),
            "date": item.get("date", "").strip(),
            "url": item.get("link", "").strip(),
            "content": clean_text(full_text)
            
        })

    return json.dumps(compiled, indent=2, ensure_ascii=False)
