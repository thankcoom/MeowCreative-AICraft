#!/usr/bin/env python3
"""
熱點自動寫作觸發器
掃描熱點 → 篩選 → 觸發寫作流程
"""

import argparse
import json
import os
import sys
from datetime import datetime

# 添加路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scan import scan_all_sources


def filter_topics(topics: list, domain_filter: dict = None) -> list:
    """
    根據領域過濾話題

    Args:
        topics: 話題列表
        domain_filter: 領域過濾設定

    Returns:
        過濾後的話題
    """
    if not domain_filter or not domain_filter.get('enabled'):
        return topics

    include_keywords = domain_filter.get('include', [])
    exclude_keywords = domain_filter.get('exclude', [])

    filtered = []
    for topic in topics:
        title = topic.get('topic', '').lower()

        # 檢查排除關鍵字
        excluded = any(kw.lower() in title for kw in exclude_keywords)
        if excluded:
            continue

        # 如果有 include 設定，必須匹配其中之一
        if include_keywords:
            included = any(kw.lower() in title for kw in include_keywords)
            if not included:
                continue

        filtered.append(topic)

    return filtered


def generate_writing_prompt(topic: dict) -> str:
    """
    根據熱點話題生成寫作提示

    Args:
        topic: 話題數據

    Returns:
        寫作提示字串
    """
    keyword = topic.get('topic', '')
    angles = topic.get('suggested_angles', [])
    heat_score = topic.get('heat_score', 0)

    # 選擇最佳角度
    best_angle = angles[0] if angles else f"關於 {keyword} 的完整分析"

    prompt = f"""
## 熱點寫作任務

### 話題資訊
- **關鍵字**: {keyword}
- **熱度分數**: {heat_score}/100
- **建議角度**: {best_angle}

### 寫作要求
1. 標題要搶眼、有時效感
2. 開頭直接切入熱點，說明為何現在很紅
3. 提供實用的觀點或整理
4. 結尾要有 CTA (留言、分享、訂閱)

### 參考角度
"""
    for idx, angle in enumerate(angles[:5], 1):
        prompt += f"{idx}. {angle}\n"

    prompt += """
### 執行流程
請使用完整的 v2.6.0 寫作流程，特別注意：
- SEO 優化 (搜尋意圖明確)
- 時效性標記 (2024/2025)
- 社群分享優化
"""

    return prompt.strip()


def trigger_writing(topic: dict, dry_run: bool = True) -> dict:
    """
    觸發寫作流程

    Args:
        topic: 話題數據
        dry_run: 是否只預覽不執行

    Returns:
        執行結果
    """
    prompt = generate_writing_prompt(topic)

    result = {
        "topic": topic.get('topic'),
        "heat_score": topic.get('heat_score'),
        "prompt": prompt,
        "triggered_at": datetime.now().isoformat(),
        "dry_run": dry_run
    }

    if dry_run:
        print("\n" + "=" * 60)
        print("📝 寫作任務預覽 (Dry Run)")
        print("=" * 60)
        print(prompt)
        print("\n" + "-" * 60)
        print("💡 實際執行請加上 --execute 參數")
    else:
        # 實際觸發寫作 - 儲存 prompt 到檔案
        output_dir = ".claude/skills/trend-monitor/outputs/writing_tasks"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_file = os.path.join(output_dir, f"task_{timestamp}.md")

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(prompt)

        result["task_file"] = task_file
        print(f"\n✅ 寫作任務已建立: {task_file}")
        print("\n使用以下指令開始寫作:")
        print(f"  claude \"請根據 {task_file} 的指示撰寫文章\"")

    return result


def main():
    parser = argparse.ArgumentParser(description="熱點自動寫作觸發器")
    parser.add_argument("--min-score", type=float, default=70,
                        help="最低熱度分數門檻 (預設: 70)")
    parser.add_argument("--max-topics", type=int, default=3,
                        help="最多處理話題數 (預設: 3)")
    parser.add_argument("--execute", action="store_true",
                        help="實際執行 (否則只預覽)")
    parser.add_argument("--include", nargs="+",
                        help="只包含這些關鍵字的話題")
    parser.add_argument("--exclude", nargs="+",
                        help="排除這些關鍵字的話題")

    args = parser.parse_args()

    print("🔥 熱點自動寫作系統")
    print("=" * 60)

    # 1. 掃描熱點
    print("\n[Step 1] 掃描熱點...")
    scan_results = scan_all_sources()

    # 2. 過濾話題
    print("\n[Step 2] 過濾話題...")
    domain_filter = {
        'enabled': bool(args.include or args.exclude),
        'include': args.include or [],
        'exclude': args.exclude or ['政治', '八卦', '緋聞']
    }

    topics = scan_results.get('top_topics', [])
    filtered = filter_topics(topics, domain_filter)

    # 3. 篩選高熱度話題
    actionable = [t for t in filtered if t.get('heat_score', 0) >= args.min_score]
    actionable = actionable[:args.max_topics]

    print(f"\n找到 {len(actionable)} 個可行動話題 (熱度 ≥ {args.min_score})")

    if not actionable:
        print("\n⚠️ 沒有符合條件的熱點話題")
        print("   建議: 降低 --min-score 或調整過濾條件")
        return

    # 4. 觸發寫作
    print("\n[Step 3] 生成寫作任務...")
    results = []
    for topic in actionable:
        result = trigger_writing(topic, dry_run=not args.execute)
        results.append(result)

    # 5. 儲存結果
    output_file = ".claude/skills/trend-monitor/outputs/auto_write_latest.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "triggered_at": datetime.now().isoformat(),
            "min_score": args.min_score,
            "dry_run": not args.execute,
            "tasks": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n💾 結果已儲存: {output_file}")


if __name__ == "__main__":
    main()
