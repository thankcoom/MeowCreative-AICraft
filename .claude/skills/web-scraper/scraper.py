import requests
from bs4 import BeautifulSoup
import json
import sys

def scrape_article(url):
    """抓取文章內容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取主要內容
        article = soup.find('article') or soup.find('main') or soup.find(class_='content')

        title = soup.find('h1')
        title_text = title.get_text().strip() if title else ''

        content_text = article.get_text(separator='\n').strip() if article else ''
        content_html = str(article) if article else ''

        return {
            'success': True,
            'title': title_text,
            'content': content_text,
            'html': content_html,
            'url': url
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    result = scrape_article(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
