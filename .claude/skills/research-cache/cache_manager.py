#!/usr/bin/env python3
"""
研究快取管理器
用於快取市場研究結果，避免重複研究相同主題

版本: 1.0.0
建立日期: 2025-10-24
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any


class ResearchCache:
    """研究結果快取管理器"""

    def __init__(self, cache_dir: str = ".cache/research"):
        """
        初始化快取管理器

        Args:
            cache_dir: 快取目錄路徑
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # 建立統計檔案
        self.stats_file = self.cache_dir / "cache_stats.json"
        if not self.stats_file.exists():
            self._init_stats()

    def _init_stats(self):
        """初始化統計資料"""
        stats = {
            "total_cached": 0,
            "total_hits": 0,
            "total_misses": 0,
            "total_time_saved_seconds": 0,
            "created_at": datetime.now().isoformat()
        }
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    def _get_cache_key(self, topic: str) -> str:
        """
        生成主題的快取鍵

        Args:
            topic: 主題關鍵字

        Returns:
            str: MD5 hash 作為快取鍵
        """
        # 標準化主題（小寫、去空格）
        normalized_topic = topic.lower().strip().replace(" ", "_")

        # 使用 MD5 hash 作為檔案名（避免特殊字符問題）
        hash_key = hashlib.md5(normalized_topic.encode('utf-8')).hexdigest()

        return f"{normalized_topic}_{hash_key[:8]}"

    def get(self, topic: str, max_age_hours: int = 24) -> Optional[Dict[str, Any]]:
        """
        取得快取的研究結果

        Args:
            topic: 主題關鍵字
            max_age_hours: 最大快取時間（小時）

        Returns:
            Dict 或 None: 快取的研究結果,如果過期或不存在則返回 None
        """
        cache_key = self._get_cache_key(topic)
        cache_file = self.cache_dir / f"{cache_key}.json"

        # 檢查快取檔案是否存在
        if not cache_file.exists():
            self._update_stats("miss")
            return None

        # 讀取快取
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  讀取快取失敗: {e}")
            self._update_stats("miss")
            return None

        # 檢查快取是否過期
        cached_time = datetime.fromisoformat(cache_data['cached_at'])
        age = datetime.now() - cached_time

        if age > timedelta(hours=max_age_hours):
            print(f"⏰ 快取已過期 (年齡: {age.total_seconds() / 3600:.1f} 小時)")
            self._update_stats("miss")
            return None

        # 快取命中
        print(f"✅ 快取命中! 主題: {topic}")
        print(f"   快取時間: {cache_data['cached_at']}")
        print(f"   年齡: {age.total_seconds() / 60:.1f} 分鐘")

        # 更新統計（假設每次研究節省2.5分鐘）
        self._update_stats("hit", time_saved=150)

        return cache_data

    def set(self, topic: str, research_data: Dict[str, Any], metadata: Optional[Dict] = None):
        """
        儲存研究結果到快取

        Args:
            topic: 主題關鍵字
            research_data: 研究結果數據
            metadata: 額外的元數據（可選）
        """
        cache_key = self._get_cache_key(topic)
        cache_file = self.cache_dir / f"{cache_key}.json"

        # 準備快取數據
        cache_data = {
            "topic": topic,
            "cached_at": datetime.now().isoformat(),
            "cache_key": cache_key,
            "metadata": metadata or {},
            "data": research_data
        }

        # 儲存快取
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)

            print(f"💾 研究結果已快取: {topic}")
            print(f"   快取檔案: {cache_file.name}")

            self._update_stats("cached")

        except IOError as e:
            print(f"❌ 快取儲存失敗: {e}")

    def _update_stats(self, event_type: str, time_saved: int = 0):
        """
        更新快取統計

        Args:
            event_type: 事件類型 (hit/miss/cached)
            time_saved: 節省的時間（秒）
        """
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)

            # 更新統計
            if event_type == "hit":
                stats["total_hits"] += 1
                stats["total_time_saved_seconds"] += time_saved
            elif event_type == "miss":
                stats["total_misses"] += 1
            elif event_type == "cached":
                stats["total_cached"] += 1

            stats["last_updated"] = datetime.now().isoformat()

            # 儲存統計
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

        except (IOError, json.JSONDecodeError):
            pass  # 統計更新失敗不影響主功能

    def get_stats(self) -> Dict[str, Any]:
        """取得快取統計資料"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)

            # 計算命中率
            total_requests = stats["total_hits"] + stats["total_misses"]
            hit_rate = (stats["total_hits"] / total_requests * 100) if total_requests > 0 else 0

            # 計算節省時間
            time_saved_minutes = stats["total_time_saved_seconds"] / 60

            stats["hit_rate_percent"] = round(hit_rate, 1)
            stats["time_saved_minutes"] = round(time_saved_minutes, 1)

            return stats

        except (IOError, json.JSONDecodeError):
            return {}

    def clear_expired(self, max_age_days: int = 30):
        """
        清除過期的快取

        Args:
            max_age_days: 保留的最大天數
        """
        expired_count = 0
        cutoff_time = datetime.now() - timedelta(days=max_age_days)

        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name == "cache_stats.json":
                continue

            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                cached_time = datetime.fromisoformat(cache_data['cached_at'])

                if cached_time < cutoff_time:
                    cache_file.unlink()
                    expired_count += 1
                    print(f"🗑️  刪除過期快取: {cache_data['topic']}")

            except (IOError, json.JSONDecodeError, KeyError):
                continue

        print(f"\n✅ 清理完成，刪除了 {expired_count} 個過期快取")

    def list_cached_topics(self) -> list:
        """列出所有已快取的主題"""
        topics = []

        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name == "cache_stats.json":
                continue

            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                cached_time = datetime.fromisoformat(cache_data['cached_at'])
                age = datetime.now() - cached_time

                topics.append({
                    "topic": cache_data['topic'],
                    "cached_at": cache_data['cached_at'],
                    "age_hours": round(age.total_seconds() / 3600, 1),
                    "cache_file": cache_file.name
                })

            except (IOError, json.JSONDecodeError, KeyError):
                continue

        # 按時間排序（最新的在前）
        topics.sort(key=lambda x: x['cached_at'], reverse=True)

        return topics


def main():
    """命令行使用範例"""
    import sys

    cache = ResearchCache()

    if len(sys.argv) < 2:
        print("用法:")
        print("  python cache_manager.py stats          # 顯示統計")
        print("  python cache_manager.py list           # 列出快取主題")
        print("  python cache_manager.py clear [days]   # 清除過期快取")
        print("  python cache_manager.py get <topic>    # 取得快取")
        return

    command = sys.argv[1]

    if command == "stats":
        # 顯示統計
        stats = cache.get_stats()
        print("\n📊 快取統計")
        print("=" * 50)
        print(f"總快取數: {stats.get('total_cached', 0)}")
        print(f"快取命中: {stats.get('total_hits', 0)}")
        print(f"快取未命中: {stats.get('total_misses', 0)}")
        print(f"命中率: {stats.get('hit_rate_percent', 0)}%")
        print(f"節省時間: {stats.get('time_saved_minutes', 0)} 分鐘")

    elif command == "list":
        # 列出所有快取
        topics = cache.list_cached_topics()
        print("\n📋 已快取的主題")
        print("=" * 50)
        for i, topic_info in enumerate(topics, 1):
            print(f"{i}. {topic_info['topic']}")
            print(f"   快取時間: {topic_info['cached_at']}")
            print(f"   年齡: {topic_info['age_hours']} 小時")
            print()

    elif command == "clear":
        # 清除過期快取
        max_days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        print(f"\n🗑️  清除 {max_days} 天前的快取...")
        cache.clear_expired(max_age_days=max_days)

    elif command == "get":
        # 取得特定主題的快取
        if len(sys.argv) < 3:
            print("❌ 請提供主題關鍵字")
            return

        topic = sys.argv[2]
        result = cache.get(topic)

        if result:
            print(f"\n✅ 找到快取: {topic}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n❌ 找不到快取: {topic}")

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
