#!/usr/bin/env python3
"""
熱度評分系統
整合多數據源，計算綜合熱度分數
"""

import json
import os
import yaml
from datetime import datetime
from typing import Optional

class HeatScorer:
    """熱度評分引擎"""

    def __init__(self, config_path: str = ".claude/config/trend-monitor.yaml"):
        self.config = self._load_config(config_path)
        self.weights = self.config.get('scoring', {}).get('weights', {
            'google_trends': 0.30,
            'ptt': 0.25,
            'dcard': 0.15,
            'youtube': 0.15,
            'news': 0.15
        })
        self.thresholds = self.config.get('scoring', {}).get('thresholds', {
            'immediate': 80,
            'watch': 60,
            'skip': 0
        })

    def _load_config(self, path: str) -> dict:
        """載入配置檔"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except:
            return {}

    def calculate_heat_score(self, topic_data: dict) -> dict:
        """
        計算單一話題的熱度分數

        Args:
            topic_data: 包含各數據源資訊的話題數據

        Returns:
            包含熱度分數和推薦行動的結果
        """
        scores = {}
        total_weight = 0

        # Google Trends 分數
        if 'google_trends' in topic_data:
            gt = topic_data['google_trends']
            gt_score = self._score_google_trends(gt)
            scores['google_trends'] = gt_score
            total_weight += self.weights.get('google_trends', 0)

        # PTT 分數
        if 'ptt' in topic_data:
            ptt = topic_data['ptt']
            ptt_score = self._score_ptt(ptt)
            scores['ptt'] = ptt_score
            total_weight += self.weights.get('ptt', 0)

        # 計算加權平均
        if total_weight > 0:
            weighted_sum = sum(
                scores.get(src, 0) * self.weights.get(src, 0)
                for src in scores
            )
            final_score = weighted_sum / total_weight
        else:
            final_score = 0

        # 判斷推薦行動
        action = self._get_recommended_action(final_score)

        # 生成寫作角度建議
        angles = self._suggest_angles(topic_data)

        return {
            "topic": topic_data.get('keyword', topic_data.get('title', 'Unknown')),
            "heat_score": round(final_score, 1),
            "source_scores": scores,
            "trend": self._detect_trend(topic_data),
            "recommended_action": action,
            "suggested_angles": angles,
            "calculated_at": datetime.now().isoformat()
        }

    def _score_google_trends(self, data: dict) -> float:
        """計算 Google Trends 分數"""
        rank = data.get('rank', 100)
        traffic_num = data.get('traffic_num', 0)

        # 排名分數 (前 5 名 = 100分, 前 10 = 80分, 前 20 = 60分)
        if rank <= 5:
            rank_score = 100
        elif rank <= 10:
            rank_score = 80
        elif rank <= 20:
            rank_score = 60
        else:
            rank_score = max(0, 50 - rank)

        # 流量分數
        if traffic_num >= 500000:
            traffic_score = 100
        elif traffic_num >= 200000:
            traffic_score = 80
        elif traffic_num >= 100000:
            traffic_score = 60
        elif traffic_num >= 50000:
            traffic_score = 40
        else:
            traffic_score = 20

        return (rank_score * 0.4 + traffic_score * 0.6)

    def _score_ptt(self, data: dict) -> float:
        """計算 PTT 分數"""
        push_count = data.get('push_count', 0)
        article_count = data.get('article_count', 1)  # 相關文章數

        # 推文分數
        if push_count >= 100:  # 爆
            push_score = 100
        elif push_count >= 70:
            push_score = 80
        elif push_count >= 50:
            push_score = 60
        elif push_count >= 30:
            push_score = 40
        else:
            push_score = max(0, push_count)

        # 文章數量加成
        if article_count >= 10:
            count_bonus = 20
        elif article_count >= 5:
            count_bonus = 10
        else:
            count_bonus = 0

        return min(100, push_score + count_bonus)

    def _detect_trend(self, data: dict) -> str:
        """偵測趨勢方向"""
        # 簡化版本：可以根據歷史數據比較
        velocity = data.get('velocity', 1.0)

        if velocity >= 2.0:
            return "rising_fast"
        elif velocity >= 1.2:
            return "rising"
        elif velocity >= 0.8:
            return "stable"
        else:
            return "falling"

    def _get_recommended_action(self, score: float) -> str:
        """根據分數決定行動建議"""
        if score >= self.thresholds.get('immediate', 80):
            return "immediate"  # 立即寫作
        elif score >= self.thresholds.get('watch', 60):
            return "watch"      # 持續關注
        else:
            return "skip"       # 略過

    def _suggest_angles(self, data: dict) -> list[str]:
        """建議寫作角度"""
        topic = data.get('keyword', data.get('title', ''))
        angles = []

        # 基本角度
        angles.append(f"教學型：如何理解/使用 {topic}")
        angles.append(f"觀點型：為什麼 {topic} 很重要")
        angles.append(f"整理型：{topic} 完整懶人包")

        # 根據來源添加特定角度
        if 'ptt' in data:
            angles.append(f"鄉民觀點：PTT 熱議 {topic} 的 5 個重點")

        if 'google_trends' in data:
            angles.append(f"趨勢分析：{topic} 為什麼突然爆紅？")

        return angles[:5]  # 最多 5 個角度


def aggregate_trends(google_trends: list, ptt_articles: list) -> list[dict]:
    """
    整合多數據源，找出重疊的熱門話題

    Args:
        google_trends: Google Trends 數據
        ptt_articles: PTT 熱門文章

    Returns:
        整合後的話題列表，含各來源資訊
    """
    topics = {}

    # 處理 Google Trends
    for trend in google_trends:
        keyword = trend['title'].lower()
        topics[keyword] = {
            'keyword': trend['title'],
            'google_trends': {
                'rank': trend['rank'],
                'traffic': trend['traffic'],
                'traffic_num': trend['traffic_num']
            }
        }

    # 處理 PTT (嘗試匹配關鍵字)
    for article in ptt_articles:
        title_lower = article['title'].lower()

        # 檢查是否與現有話題相關
        matched = False
        for keyword in list(topics.keys()):
            if keyword in title_lower or any(word in title_lower for word in keyword.split()):
                # 找到匹配
                if 'ptt' not in topics[keyword]:
                    topics[keyword]['ptt'] = {
                        'push_count': article['push_count'],
                        'article_count': 1,
                        'articles': [article]
                    }
                else:
                    topics[keyword]['ptt']['article_count'] += 1
                    topics[keyword]['ptt']['push_count'] = max(
                        topics[keyword]['ptt']['push_count'],
                        article['push_count']
                    )
                    topics[keyword]['ptt']['articles'].append(article)
                matched = True
                break

        # 沒匹配到，作為獨立話題
        if not matched and article['push_count'] >= 50:
            key = article['title'][:20].lower()
            topics[key] = {
                'keyword': article['title'],
                'ptt': {
                    'push_count': article['push_count'],
                    'article_count': 1,
                    'articles': [article]
                }
            }

    return list(topics.values())


def main():
    """測試熱度評分"""
    print("=" * 60)
    print("熱度評分系統測試")
    print("=" * 60)

    scorer = HeatScorer()

    # 模擬數據
    test_topics = [
        {
            'keyword': 'AI 人工智慧',
            'google_trends': {'rank': 3, 'traffic_num': 200000},
            'ptt': {'push_count': 85, 'article_count': 5}
        },
        {
            'keyword': '比特幣',
            'google_trends': {'rank': 1, 'traffic_num': 500000},
            'ptt': {'push_count': 100, 'article_count': 12}
        },
        {
            'keyword': '某政治人物',
            'google_trends': {'rank': 2, 'traffic_num': 300000},
            'ptt': {'push_count': 100, 'article_count': 20}
        }
    ]

    results = []
    for topic in test_topics:
        result = scorer.calculate_heat_score(topic)
        results.append(result)

        print(f"\n話題: {result['topic']}")
        print(f"  熱度分數: {result['heat_score']}/100")
        print(f"  趨勢: {result['trend']}")
        print(f"  建議行動: {result['recommended_action']}")
        print(f"  寫作角度:")
        for angle in result['suggested_angles'][:3]:
            print(f"    - {angle}")

    # 輸出結果
    output_file = ".claude/skills/trend-monitor/outputs/heat_scores_latest.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "calculated_at": datetime.now().isoformat(),
                "results": results
            }, f, ensure_ascii=False, indent=2)
        print(f"\n已儲存至: {output_file}")
    except Exception as e:
        print(f"\n儲存失敗: {e}")


if __name__ == "__main__":
    main()
