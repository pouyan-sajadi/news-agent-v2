import re
import uuid
import json
from datetime import datetime
from newspaper import Article
import serpapi
from app.config import SERPAPI_KEY, NUM_SOURCES

def clean_text(text):
    # Removes control characters (ASCII 0–31 and 127)
    return re.sub(r'[\x00-\x1f\x7f]', '', text).strip()

def fetch_full_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"[Failed to fetch full article: {e}]"

def search_news(topic):
    client = serpapi.Client(api_key=SERPAPI_KEY)

    params = {
        "engine": "google",
        "q": f"{topic} news {datetime.now().strftime('%Y-%m')}",
        "tbm": "nws",  
        "num": NUM_SOURCES
    }

    try:
        results = client.search(params)
        news_results = results.get("news_results", [])
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
