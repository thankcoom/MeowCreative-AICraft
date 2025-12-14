#!/usr/bin/env python3
"""
Google Trends 數據源
抓取台灣/全球即時熱門搜尋趨勢
"""

import json
import ssl
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Optional

# 處理 SSL 證書問題
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class GoogleTrendsSource:
    """Google Trends 數據抓取器"""

    def __init__(self, region: str = "TW", language: str = "zh-TW"):
        self.region = region
        self.language = language
        self.base_url = "https://trends.google.com.tw/trending/rss"

    def fetch_realtime_trends(self, limit: int = 20) -> list[dict]:
        """
        抓取即時熱門搜尋

        Returns:
            list of trend items with title, traffic, and related queries
        """
        try:
            url = f"{self.base_url}?geo={self.region}"

            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                    'Accept-Language': self.language
                }
            )

            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                content = response.read().decode('utf-8')

            # 解析 RSS XML
            trends = self._parse_rss(content)
            return trends[:limit]

        except Exception as e:
            print(f"[Google Trends] 抓取失敗: {e}")
            return []

    def _parse_rss(self, xml_content: str) -> list[dict]:
        """解析 RSS 內容"""
        import re

        trends = []

        # 簡單的 XML 解析 (避免依賴外部庫)
        items = re.findall(r'<item>(.*?)</item>', xml_content, re.DOTALL)

        for idx, item in enumerate(items):
            title_match = re.search(r'<title>(.*?)</title>', item)
            traffic_match = re.search(r'<ht:approx_traffic>(.*?)</ht:approx_traffic>', item)
            news_match = re.findall(r'<ht:news_item_title>(.*?)</ht:news_item_title>', item)

            if title_match:
                title = title_match.group(1).strip()
                traffic = traffic_match.group(1) if traffic_match else "N/A"

                # 清理 traffic 數字
                traffic_num = self._parse_traffic(traffic)

                trends.append({
                    "rank": idx + 1,
                    "title": title,
                    "traffic": traffic,
                    "traffic_num": traffic_num,
                    "related_news": news_match[:3] if news_match else [],
                    "source": "google_trends",
                    "region": self.region,
                    "fetched_at": datetime.now().isoformat()
                })

        return trends

    def _parse_traffic(self, traffic_str: str) -> int:
        """將 '100K+' 這類字串轉換為數字"""
        if not traffic_str or traffic_str == "N/A":
            return 0

        traffic_str = traffic_str.replace("+", "").replace(",", "").strip()

        multipliers = {
            'K': 1000,
            'M': 1000000,
            'B': 1000000000
        }

        for suffix, mult in multipliers.items():
            if suffix in traffic_str.upper():
                num_part = traffic_str.upper().replace(suffix, "")
                try:
                    return int(float(num_part) * mult)
                except:
                    return 0

        try:
            return int(traffic_str)
        except:
            return 0

    def search_interest(self, keyword: str, timeframe: str = "now 7-d") -> dict:
        """
        查詢特定關鍵字的搜尋熱度

        Args:
            keyword: 要查詢的關鍵字
            timeframe: 時間範圍 (now 1-H, now 4-H, now 1-d, now 7-d)

        Returns:
            interest data with trend direction
        """
        # 注意：完整的 interest over time 需要 pytrends 庫
        # 這裡提供基本框架，實際使用建議安裝 pytrends
        return {
            "keyword": keyword,
            "timeframe": timeframe,
            "note": "完整功能需安裝 pytrends: pip install pytrends"
        }


def main():
    """測試 Google Trends 抓取"""
    print("=" * 60)
    print("Google Trends 台灣即時熱門搜尋")
    print("=" * 60)

    source = GoogleTrendsSource(region="TW")
    trends = source.fetch_realtime_trends(limit=20)

    if not trends:
        print("無法取得趨勢數據，請檢查網路連線")
        return

    print(f"\n抓取時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"共 {len(trends)} 筆熱門搜尋\n")

    for trend in trends:
        print(f"#{trend['rank']:2d} | {trend['title']}")
        print(f"     搜尋量: {trend['traffic']}")
        if trend['related_news']:
            print(f"     相關: {trend['related_news'][0][:50]}...")
        print()

    # 輸出 JSON
    output_file = ".claude/skills/trend-monitor/outputs/google_trends_latest.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "source": "google_trends",
                "region": "TW",
                "fetched_at": datetime.now().isoformat(),
                "trends": trends
            }, f, ensure_ascii=False, indent=2)
        print(f"\n已儲存至: {output_file}")
    except Exception as e:
        print(f"\n儲存失敗: {e}")


if __name__ == "__main__":
    main()
