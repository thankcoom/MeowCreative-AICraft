#!/usr/bin/env python3
"""
熱點掃描主程式
整合多數據源，輸出熱門話題排行
"""

import argparse
import json
import os
import sys
from datetime import datetime

# 添加路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sources.google_trends import GoogleTrendsSource
from sources.ptt import PTTSource
from analyzers.heat_scorer import HeatScorer, aggregate_trends


def scan_all_sources(config: dict = None) -> dict:
    """掃描所有數據源"""
    results = {
        "scan_time": datetime.now().isoformat(),
        "sources": {},
        "aggregated": [],
        "top_topics": []
    }

    # 1. Google Trends
    print("\n[1/3] 掃描 Google Trends...")
    gt_source = GoogleTrendsSource(region="TW")
    gt_trends = gt_source.fetch_realtime_trends(limit=20)
    results["sources"]["google_trends"] = gt_trends
    print(f"      取得 {len(gt_trends)} 筆熱門搜尋")

    # 2. PTT
    print("[2/3] 掃描 PTT 熱門文章...")
    ptt_source = PTTSource()
    ptt_boards = ["Gossiping", "Tech_Job", "Stock", "Lifeismoney"]
    ptt_articles = ptt_source.fetch_multiple_boards(ptt_boards, min_push=30)
    results["sources"]["ptt"] = ptt_articles
    print(f"      取得 {len(ptt_articles)} 篇熱門文章")

    # 3. 整合與評分
    print("[3/3] 整合數據並評分...")
    aggregated = aggregate_trends(gt_trends, ptt_articles)

    scorer = HeatScorer()
    scored_topics = []

    for topic in aggregated:
        scored = scorer.calculate_heat_score(topic)
        scored_topics.append(scored)

    # 按熱度排序
    scored_topics.sort(key=lambda x: x['heat_score'], reverse=True)

    results["aggregated"] = scored_topics
    results["top_topics"] = scored_topics[:10]

    return results


def print_results(results: dict, top_n: int = 20):
    """輸出結果"""
    print("\n" + "=" * 70)
    print(f"🔥 熱點掃描結果 - {results['scan_time'][:19]}")
    print("=" * 70)

    print("\n📊 熱門話題排行 (綜合熱度)")
    print("-" * 70)

    for idx, topic in enumerate(results['top_topics'][:top_n], 1):
        score = topic['heat_score']
        action = topic['recommended_action']

        # 熱度指示條
        bar_len = int(score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)

        # 行動標籤
        if action == "immediate":
            action_tag = "🚀 立即寫"
        elif action == "watch":
            action_tag = "👀 關注中"
        else:
            action_tag = "⏸️ 略過"

        print(f"\n#{idx:2d} {topic['topic'][:35]:<35}")
        print(f"    熱度: [{bar}] {score:5.1f}/100  {action_tag}")

        # 來源資訊
        sources_info = []
        if 'google_trends' in topic.get('source_scores', {}):
            sources_info.append("Google")
        if 'ptt' in topic.get('source_scores', {}):
            sources_info.append("PTT")
        if sources_info:
            print(f"    來源: {', '.join(sources_info)}")

        # 寫作角度 (只顯示前 2 個)
        if topic.get('suggested_angles'):
            print(f"    角度: {topic['suggested_angles'][0]}")

    # 統計摘要
    print("\n" + "=" * 70)
    print("📈 統計摘要")
    print("-" * 70)

    immediate = len([t for t in results['top_topics'] if t['recommended_action'] == 'immediate'])
    watch = len([t for t in results['top_topics'] if t['recommended_action'] == 'watch'])

    print(f"  🚀 立即寫作: {immediate} 個話題")
    print(f"  👀 持續關注: {watch} 個話題")
    print(f"  📰 Google Trends: {len(results['sources'].get('google_trends', []))} 筆")
    print(f"  💬 PTT 熱門: {len(results['sources'].get('ptt', []))} 篇")


def save_results(results: dict, output_dir: str = ".claude/skills/trend-monitor/outputs"):
    """儲存結果"""
    os.makedirs(output_dir, exist_ok=True)

    # 完整結果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = os.path.join(output_dir, f"scan_{timestamp}.json")

    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 最新結果 (覆蓋)
    latest_path = os.path.join(output_dir, "scan_latest.json")
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 結果已儲存:")
    print(f"   - {full_path}")
    print(f"   - {latest_path}")

    return full_path


def main():
    parser = argparse.ArgumentParser(description="熱點掃描工具")
    parser.add_argument("--source", default="all",
                        help="數據源 (all, google_trends, ptt)")
    parser.add_argument("--top", type=int, default=20,
                        help="顯示前 N 個話題")
    parser.add_argument("--output", default=".claude/skills/trend-monitor/outputs",
                        help="輸出目錄")
    parser.add_argument("--json-only", action="store_true",
                        help="只輸出 JSON，不顯示表格")

    args = parser.parse_args()

    print("🔍 開始熱點掃描...")

    # 執行掃描
    results = scan_all_sources()

    # 顯示結果
    if not args.json_only:
        print_results(results, top_n=args.top)

    # 儲存結果
    save_results(results, args.output)

    # 輸出可立即行動的話題
    immediate_topics = [t for t in results['top_topics'] if t['recommended_action'] == 'immediate']
    if immediate_topics:
        print("\n" + "=" * 70)
        print("⚡ 建議立即行動的話題:")
        print("=" * 70)
        for t in immediate_topics[:3]:
            print(f"\n  📝 {t['topic']}")
            print(f"     熱度: {t['heat_score']}/100")
            print(f"     建議角度: {t['suggested_angles'][0]}")


if __name__ == "__main__":
    main()
