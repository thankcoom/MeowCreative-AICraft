#!/usr/bin/env python3
"""
PTT 熱門文章數據源
抓取各看板熱門文章
"""

import json
import re
import ssl
import urllib.request
from datetime import datetime
from typing import Optional

# 處理 SSL 證書問題
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class PTTSource:
    """PTT 熱門文章抓取器"""

    def __init__(self):
        self.base_url = "https://www.ptt.cc"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Cookie': 'over18=1'  # 跳過年齡驗證
        }

    def fetch_board_hot(self, board: str, limit: int = 20) -> list[dict]:
        """
        抓取指定看板的熱門文章

        Args:
            board: 看板名稱 (如 Gossiping, Tech_Job)
            limit: 抓取數量

        Returns:
            list of hot articles
        """
        try:
            url = f"{self.base_url}/bbs/{board}/index.html"

            req = urllib.request.Request(url, headers=self.headers)

            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                content = response.read().decode('utf-8')

            articles = self._parse_board_page(content, board)

            # 按推文數排序
            articles.sort(key=lambda x: x['push_count'], reverse=True)

            return articles[:limit]

        except Exception as e:
            print(f"[PTT] 抓取 {board} 失敗: {e}")
            return []

    def _parse_board_page(self, html: str, board: str) -> list[dict]:
        """解析看板頁面"""
        articles = []

        # 找出所有文章區塊
        pattern = r'<div class="r-ent">(.*?)</div>\s*</div>'
        matches = re.findall(pattern, html, re.DOTALL)

        for match in matches:
            article = self._parse_article_entry(match, board)
            if article:
                articles.append(article)

        return articles

    def _parse_article_entry(self, html: str, board: str) -> Optional[dict]:
        """解析單篇文章"""
        # 推文數
        push_match = re.search(r'<span class="[^"]*hl[^"]*">([^<]*)</span>', html)
        push_str = push_match.group(1).strip() if push_match else "0"

        # 轉換推文數
        if push_str == "爆":
            push_count = 100
        elif push_str.startswith("X"):
            push_count = -10  # 噓文多
        elif push_str == "":
            push_count = 0
        else:
            try:
                push_count = int(push_str)
            except:
                push_count = 0

        # 標題和連結
        title_match = re.search(r'<a href="([^"]+)">([^<]+)</a>', html)
        if not title_match:
            return None

        link = title_match.group(1)
        title = title_match.group(2).strip()

        # 過濾公告和刪除文
        if title.startswith("[公告]") or title == "(本文已被刪除)":
            return None

        # 作者
        author_match = re.search(r'<div class="author">([^<]+)</div>', html)
        author = author_match.group(1).strip() if author_match else "unknown"

        # 日期
        date_match = re.search(r'<div class="date">([^<]+)</div>', html)
        date = date_match.group(1).strip() if date_match else ""

        return {
            "title": title,
            "author": author,
            "push_count": push_count,
            "date": date,
            "link": f"{self.base_url}{link}",
            "board": board,
            "source": "ptt",
            "fetched_at": datetime.now().isoformat()
        }

    def fetch_multiple_boards(self, boards: list[str], min_push: int = 30) -> list[dict]:
        """
        抓取多個看板的熱門文章

        Args:
            boards: 看板列表
            min_push: 最低推文數門檻

        Returns:
            合併並排序的熱門文章
        """
        all_articles = []

        for board in boards:
            print(f"[PTT] 抓取 {board}...")
            articles = self.fetch_board_hot(board, limit=30)
            all_articles.extend(articles)

        # 過濾低推文數
        filtered = [a for a in all_articles if a['push_count'] >= min_push]

        # 按推文數排序
        filtered.sort(key=lambda x: x['push_count'], reverse=True)

        return filtered

    def extract_keywords(self, title: str) -> list[str]:
        """從標題提取關鍵字"""
        # 移除常見標籤
        title = re.sub(r'\[[^\]]+\]', '', title)
        title = re.sub(r'Re:', '', title)
        title = re.sub(r'Fw:', '', title)

        # 簡單分詞 (可以用 jieba 提升效果)
        words = title.strip().split()
        return [w for w in words if len(w) > 1]


def main():
    """測試 PTT 抓取"""
    print("=" * 60)
    print("PTT 熱門文章抓取")
    print("=" * 60)

    source = PTTSource()

    # 測試看板
    test_boards = ["Gossiping", "Tech_Job", "Stock"]

    all_hot = source.fetch_multiple_boards(test_boards, min_push=30)

    print(f"\n抓取時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"共 {len(all_hot)} 篇熱門文章 (推文 ≥30)\n")

    for idx, article in enumerate(all_hot[:20], 1):
        push_display = "爆" if article['push_count'] >= 100 else str(article['push_count'])
        print(f"#{idx:2d} [{article['board']:12s}] {push_display:>3s}推 | {article['title'][:40]}")

    # 輸出 JSON
    output_file = ".claude/skills/trend-monitor/outputs/ptt_hot_latest.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "source": "ptt",
                "boards": test_boards,
                "min_push": 30,
                "fetched_at": datetime.now().isoformat(),
                "articles": all_hot
            }, f, ensure_ascii=False, indent=2)
        print(f"\n已儲存至: {output_file}")
    except Exception as e:
        print(f"\n儲存失敗: {e}")


if __name__ == "__main__":
    main()
