#!/usr/bin/env python3
"""
動態參考作者匹配系統
根據文章主題自動選擇最合適的參考作者

版本: 1.0.0
建立日期: 2025-10-24
"""

import yaml
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple


class DynamicReferenceSelector:
    """動態參考作者選擇器"""

    def __init__(self, db_path: str = ".claude/config/reference-authors-db.yaml"):
        """
        初始化選擇器

        Args:
            db_path: 參考作者資料庫路徑
        """
        self.db_path = Path(db_path)
        self.db = self._load_database()
        self.matching_config = self.db.get('matching_rules', {})

    def _load_database(self) -> Dict[str, Any]:
        """載入參考作者資料庫"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ 找不到資料庫: {self.db_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"❌ YAML 解析錯誤: {e}")
            return {}

    def _normalize_text(self, text: str) -> str:
        """
        標準化文本（轉小寫、去標點）

        Args:
            text: 原始文本

        Returns:
            str: 標準化後的文本
        """
        # 轉小寫
        text = text.lower()
        # 移除標點符號（保留中英文和數字）
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        return text

    def _calculate_match_score(self, topic: str, category_keywords: List[str]) -> float:
        """
        計算主題與分類關鍵字的匹配分數

        Args:
            topic: 文章主題
            category_keywords: 分類的關鍵字列表

        Returns:
            float: 匹配分數 (0.0 - 1.0)
        """
        normalized_topic = self._normalize_text(topic)
        topic_words = set(normalized_topic.split())

        # 計算匹配的關鍵字數量
        matches = 0
        total_keywords = len(category_keywords)

        for keyword in category_keywords:
            normalized_keyword = self._normalize_text(keyword)

            # 檢查完整匹配或部分匹配
            if normalized_keyword in normalized_topic or any(
                normalized_keyword in word or word in normalized_keyword
                for word in topic_words
            ):
                matches += 1

        # 計算匹配分數
        score = matches / total_keywords if total_keywords > 0 else 0.0

        return score

    def select_authors(
        self,
        topic: str,
        max_authors: int = 2
    ) -> List[Dict[str, Any]]:
        """
        根據主題選擇最合適的參考作者

        Args:
            topic: 文章主題
            max_authors: 最多返回作者數量

        Returns:
            List[Dict]: 推薦的作者列表
        """
        if not self.db or 'topic_categories' not in self.db:
            print("⚠️  資料庫為空或格式錯誤")
            return self._get_fallback_authors(max_authors)

        topic_categories = self.db['topic_categories']
        category_scores = []

        # 計算每個分類的匹配分數
        for category_name, category_data in topic_categories.items():
            keywords = category_data.get('keywords', [])
            score = self._calculate_match_score(topic, keywords)

            if score > 0:
                category_scores.append({
                    'category': category_name,
                    'score': score,
                    'data': category_data
                })

        # 按分數排序
        category_scores.sort(key=lambda x: x['score'], reverse=True)

        # 檢查最低匹配分數
        min_score = self.matching_config.get('keyword_matching', {}).get('min_match_score', 0.3)

        # 收集推薦作者
        recommended_authors = []
        authors_per_category = max_authors  # 每個分類最多推薦的作者數

        for category_info in category_scores:
            # 只選擇分數達標的分類
            if category_info['score'] < min_score:
                continue

            reference_authors = category_info['data'].get('reference_authors', [])

            # 從該分類選擇作者（優先選擇第一位）
            for author in reference_authors[:authors_per_category]:
                if len(recommended_authors) >= max_authors:
                    break

                recommended_authors.append({
                    'name': author['name'],
                    'blog': author['blog'],
                    'style_notes': author.get('style_notes', ''),
                    'strengths': author.get('strengths', []),
                    'best_for': author.get('best_for', []),
                    'category': category_info['category'],
                    'match_score': category_info['score'],
                    'article_examples': author.get('article_examples', [])
                })

            if len(recommended_authors) >= max_authors:
                break

        # 如果沒有找到足夠的作者，使用預設作者
        if len(recommended_authors) < max_authors:
            fallback = self._get_fallback_authors(max_authors - len(recommended_authors))
            recommended_authors.extend(fallback)

        return recommended_authors[:max_authors]

    def _get_fallback_authors(self, count: int = 2) -> List[Dict[str, Any]]:
        """
        取得預設的回退作者

        Args:
            count: 需要的作者數量

        Returns:
            List[Dict]: 預設作者列表
        """
        default_authors = self.db.get('default_authors', {}).get('fallback', [])

        fallback_authors = []
        for author in default_authors[:count]:
            fallback_authors.append({
                'name': author['name'],
                'blog': author['blog'],
                'style_notes': '通用技術寫作風格',
                'strengths': ['清晰的技術解析', '實用的範例'],
                'best_for': ['技術文章', '教學內容'],
                'category': 'default',
                'match_score': 0.1,
                'article_examples': []
            })

        return fallback_authors

    def get_matching_report(self, topic: str) -> str:
        """
        生成詳細的匹配報告（用於調試和展示）

        Args:
            topic: 文章主題

        Returns:
            str: Markdown 格式的匹配報告
        """
        authors = self.select_authors(topic, max_authors=2)

        report = f"# 參考作者匹配報告\n\n"
        report += f"**主題**: {topic}\n\n"
        report += f"**匹配時間**: {self._get_timestamp()}\n\n"
        report += "---\n\n"
        report += "## 推薦作者\n\n"

        for i, author in enumerate(authors, 1):
            report += f"### {i}. {author['name']}\n\n"
            report += f"- **部落格**: {author['blog']}\n"
            report += f"- **風格特色**: {author['style_notes']}\n"
            report += f"- **匹配分類**: {author['category']}\n"
            report += f"- **匹配分數**: {author['match_score']:.2f}\n\n"

            report += "**優勢**:\n"
            for strength in author.get('strengths', []):
                report += f"- {strength}\n"
            report += "\n"

            report += "**最適合主題**:\n"
            for topic_type in author.get('best_for', []):
                report += f"- {topic_type}\n"
            report += "\n"

            if author.get('article_examples'):
                report += "**範例文章**:\n"
                for example in author['article_examples']:
                    report += f"- {example}\n"
                report += "\n"

            report += "---\n\n"

        report += "## 使用建議\n\n"
        report += "### Style Matcher Agent 應該:\n\n"
        report += "1. **分析推薦作者的文章範例**\n"
        report += "   - 研讀上述範例文章,提取寫作模式\n"
        report += "   - 注意標題、開頭、結構、語氣的特色\n\n"

        report += "2. **融合風格特色到新文章**\n"
        for author in authors:
            report += f"   - {author['name']}: {author['style_notes']}\n"
        report += "\n"

        report += "3. **保持平衡**\n"
        report += "   - 學習風格但不抄襲內容\n"
        report += "   - 保持喵哩文創的獨特調性\n"
        report += "   - 確保技術準確性優先於風格模仿\n\n"

        return report

    def _get_timestamp(self) -> str:
        """取得當前時間戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """命令行使用範例"""
    import sys

    selector = DynamicReferenceSelector()

    if len(sys.argv) < 2:
        print("用法:")
        print("  python dynamic_references.py test <主題>     # 測試匹配")
        print("  python dynamic_references.py report <主題>   # 生成完整報告")
        print("\n範例:")
        print("  python dynamic_references.py test \"Claude Code AI 自動化應用\"")
        print("  python dynamic_references.py report \"量化交易策略回測\"")
        return

    command = sys.argv[1]

    if command == "test" and len(sys.argv) >= 3:
        # 測試模式：顯示推薦作者
        topic = " ".join(sys.argv[2:])
        print(f"\n🔍 主題: {topic}\n")

        authors = selector.select_authors(topic, max_authors=2)

        print("📚 推薦參考作者:\n")
        for i, author in enumerate(authors, 1):
            print(f"{i}. {author['name']}")
            print(f"   部落格: {author['blog']}")
            print(f"   分類: {author['category']}")
            print(f"   匹配分數: {author['match_score']:.2f}")
            print(f"   風格: {author['style_notes']}")
            print()

    elif command == "report" and len(sys.argv) >= 3:
        # 報告模式：生成詳細報告
        topic = " ".join(sys.argv[2:])
        report = selector.get_matching_report(topic)
        print(report)

        # 可選：儲存報告到檔案
        output_file = Path("output") / "reference_matching_report.md"
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 報告已儲存至: {output_file}")

    else:
        print("❌ 未知命令或缺少參數")
        print("使用 'python dynamic_references.py' 查看用法")


if __name__ == "__main__":
    main()
