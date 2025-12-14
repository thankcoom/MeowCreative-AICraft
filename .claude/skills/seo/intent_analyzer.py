#!/usr/bin/env python3
"""
SEO 搜尋意圖分析器
分析關鍵字的搜尋意圖，並提供結構化建議

版本: 1.0.0
建立日期: 2025-10-24
"""

import re
import yaml
import json
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class SearchIntent(Enum):
    """搜尋意圖類型"""
    TUTORIAL = "教學型"           # 如何做X、步驟、指南
    INFORMATIONAL = "資訊型"      # 什麼是X、介紹、說明
    COMPARISON = "比較型"         # X vs Y、差異、哪個好
    REVIEW = "評價型"             # X好用嗎、評測、推薦
    TRANSACTIONAL = "交易型"      # 購買X、價格、費用
    PROBLEM_SOLVING = "問題解決型" # 如何解決、錯誤修復、疑難排解


class IntentAnalyzer:
    """搜尋意圖分析器"""

    def __init__(self, rules_path: str = ".claude/skills/seo/intent_rules.yaml"):
        """
        初始化分析器

        Args:
            rules_path: 意圖規則配置檔路徑
        """
        self.rules_path = Path(rules_path)
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """載入意圖匹配規則"""
        if not self.rules_path.exists():
            # 如果規則檔不存在，使用內建規則
            return self._get_default_rules()

        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except (yaml.YAMLError, IOError) as e:
            print(f"⚠️  載入規則檔失敗: {e}")
            return self._get_default_rules()

    def _get_default_rules(self) -> Dict[str, Any]:
        """取得預設的意圖匹配規則"""
        return {
            'intent_patterns': {
                'tutorial': {
                    'keywords': ['如何', '怎麼', '教學', '步驟', '指南', '方法', '手把手', '完整', '實作'],
                    'weight': 1.0
                },
                'informational': {
                    'keywords': ['是什麼', '介紹', '說明', '原理', '為什麼', '定義', '概念', '解析'],
                    'weight': 0.9
                },
                'comparison': {
                    'keywords': ['比較', 'vs', '差異', '哪個好', '推薦', '選擇', '對比'],
                    'weight': 1.0
                },
                'review': {
                    'keywords': ['好用嗎', '評測', '評價', '心得', '優缺點', '值得'],
                    'weight': 0.8
                },
                'problem_solving': {
                    'keywords': ['解決', '修復', '錯誤', '問題', '無法', '失敗', '不能', '疑難'],
                    'weight': 1.0
                }
            }
        }

    def analyze(self, keyword: str, article_content: Optional[str] = None) -> Dict[str, Any]:
        """
        分析關鍵字的搜尋意圖

        Args:
            keyword: 主要關鍵字
            article_content: 文章內容（可選，用於匹配度分析）

        Returns:
            Dict: 分析結果
        """
        # 標準化關鍵字
        normalized_keyword = keyword.lower().strip()

        # 計算各意圖的匹配分數
        intent_scores = {}
        patterns = self.rules.get('intent_patterns', {})

        for intent_type, config in patterns.items():
            keywords = config.get('keywords', [])
            weight = config.get('weight', 1.0)

            # 計算匹配數量
            matches = sum(1 for kw in keywords if kw in normalized_keyword)
            score = matches * weight

            if score > 0:
                intent_scores[intent_type] = score

        # 確定主要意圖
        if not intent_scores:
            # 如果沒有匹配，預設為資訊型
            primary_intent = 'informational'
            confidence = 0.5
        else:
            # 選擇分數最高的意圖
            primary_intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[primary_intent]
            total_score = sum(intent_scores.values())
            confidence = max_score / total_score if total_score > 0 else 0.5

        # 取得意圖對應的建議
        recommendations = self._get_recommendations(primary_intent)

        # 如果有文章內容，進行匹配度分析
        match_score = None
        match_details = None
        if article_content:
            match_score, match_details = self._analyze_content_match(
                article_content,
                primary_intent,
                recommendations
            )

        return {
            'keyword': keyword,
            'primary_intent': primary_intent,
            'intent_label': self._get_intent_label(primary_intent),
            'confidence': round(confidence, 2),
            'all_scores': intent_scores,
            'recommendations': recommendations,
            'match_score': match_score,
            'match_details': match_details,
            'analyzed_at': datetime.now().isoformat()
        }

    def _get_intent_label(self, intent_type: str) -> str:
        """取得意圖的中文標籤"""
        labels = {
            'tutorial': SearchIntent.TUTORIAL.value,
            'informational': SearchIntent.INFORMATIONAL.value,
            'comparison': SearchIntent.COMPARISON.value,
            'review': SearchIntent.REVIEW.value,
            'transactional': SearchIntent.TRANSACTIONAL.value,
            'problem_solving': SearchIntent.PROBLEM_SOLVING.value
        }
        return labels.get(intent_type, '未知')

    def _get_recommendations(self, intent_type: str) -> Dict[str, Any]:
        """根據意圖類型取得結構化建議"""
        recommendations = {
            'tutorial': {
                'title_format': '【完整指南】如何{action} - {benefit}',
                'title_examples': [
                    '【完整指南】如何使用 Claude Code 建立 AI Agent - 10分鐘快速上手',
                    '手把手教你用 Python 打造量化交易系統 - 從零到實戰'
                ],
                'must_include': [
                    '前置準備清單（環境、工具、知識要求）',
                    '逐步操作步驟（帶編號、帶截圖）',
                    '每個步驟的預期結果',
                    '常見錯誤和解決方法',
                    '進階技巧和最佳實踐',
                    '完整的可執行範例'
                ],
                'structure_template': [
                    '## 引言（為什麼需要學這個）',
                    '## 前置準備',
                    '## 步驟一：...',
                    '## 步驟二：...',
                    '## 常見問題',
                    '## 進階技巧',
                    '## 總結與下一步'
                ],
                'tone': '友善指導、循序漸進、鼓勵性',
                'cta': '立即嘗試、下載範例、加入社群'
            },
            'informational': {
                'title_format': '{topic}完全解析 - {unique_angle}',
                'title_examples': [
                    'Claude Code 完全解析 - 5個你不知道的強大功能',
                    'AI Agent 系統架構深度剖析 - 從原理到實踐'
                ],
                'must_include': [
                    '清晰的定義（What）',
                    '工作原理（How）',
                    '為什麼重要（Why）',
                    '實際應用場景',
                    '優缺點分析',
                    '與相關概念的比較'
                ],
                'structure_template': [
                    '## 引言（背景和重要性）',
                    '## 定義和核心概念',
                    '## 工作原理',
                    '## 實際應用場景',
                    '## 優缺點分析',
                    '## 總結'
                ],
                'tone': '專業客觀、深入淺出、結構清晰',
                'cta': '深入閱讀、訂閱更新、相關文章'
            },
            'comparison': {
                'title_format': '{option1} vs {option2}：{decision_guide}',
                'title_examples': [
                    'Claude Code vs GitHub Copilot：2025 AI 編程工具選擇指南',
                    'Python vs JavaScript 量化交易：哪個更適合你？'
                ],
                'must_include': [
                    '對比表格（功能、價格、優缺點）',
                    '各自的優勢場景',
                    '適合的用戶類型',
                    '效能/價格比較',
                    '決策框架或流程圖',
                    '實際測試數據'
                ],
                'structure_template': [
                    '## 引言（為什麼需要比較）',
                    '## 快速對比表',
                    '## {Option1} 深度分析',
                    '## {Option2} 深度分析',
                    '## 使用場景建議',
                    '## 決策指南',
                    '## 總結建議'
                ],
                'tone': '客觀中立、數據驅動、實用導向',
                'cta': '開始試用、查看定價、諮詢建議'
            },
            'review': {
                'title_format': '{product}深度評測 - {time_period}使用心得',
                'title_examples': [
                    'Claude Code 深度評測 - 30天實戰使用心得',
                    'FinMind API 量化交易評價 - 值得投資嗎？'
                ],
                'must_include': [
                    '評測環境和背景',
                    '優點列表（具體案例）',
                    '缺點列表（真實問題）',
                    '實際使用數據或截圖',
                    '與預期的差異',
                    '是否推薦（明確結論）'
                ],
                'structure_template': [
                    '## 評測背景',
                    '## 核心優勢',
                    '## 主要缺點',
                    '## 實測數據',
                    '## 適合對象',
                    '## 最終評分',
                    '## 是否推薦'
                ],
                'tone': '真誠坦率、有依據、平衡觀點',
                'cta': '查看官網、免費試用、閱讀更多評測'
            },
            'problem_solving': {
                'title_format': '解決{problem} - {solution_count}種有效方法',
                'title_examples': [
                    '解決 Claude Code 無法連接問題 - 5種診斷方法',
                    '修復量化回測錯誤 - 完整排查指南'
                ],
                'must_include': [
                    '問題症狀描述',
                    '可能的原因分析',
                    '解決方案（按優先級排序）',
                    '每個方案的適用情況',
                    '預防措施',
                    '何時需要尋求專業協助'
                ],
                'structure_template': [
                    '## 問題描述',
                    '## 原因分析',
                    '## 解決方案一（最常見）',
                    '## 解決方案二',
                    '## 解決方案三',
                    '## 預防措施',
                    '## 總結'
                ],
                'tone': '解決導向、務實高效、同理心',
                'cta': '嘗試解決、求助社群、聯繫支援'
            }
        }

        return recommendations.get(intent_type, recommendations['informational'])

    def _analyze_content_match(
        self,
        content: str,
        intent_type: str,
        recommendations: Dict[str, Any]
    ) -> tuple[float, Dict[str, Any]]:
        """
        分析文章內容與意圖的匹配度

        Args:
            content: 文章內容
            intent_type: 意圖類型
            recommendations: 意圖建議

        Returns:
            tuple: (匹配分數, 匹配詳情)
        """
        must_include = recommendations.get('must_include', [])

        # 檢查必要元素
        matches = []
        misses = []

        # 簡化的關鍵字匹配邏輯
        keyword_mapping = {
            '前置準備': ['前置', '準備', '環境', '安裝', '要求'],
            '步驟': ['步驟', 'step', '第一', '第二', '首先', '接著'],
            '常見錯誤': ['錯誤', '問題', '注意', '避免'],
            '定義': ['定義', '是什麼', '指的是', '意思'],
            '原理': ['原理', '運作', '如何工作', '機制'],
            '優缺點': ['優點', '缺點', '好處', '限制', '優勢', '劣勢'],
            '對比': ['比較', '對比', 'vs', '差異'],
            '表格': ['|', '表格'],
        }

        content_lower = content.lower()

        for item in must_include:
            item_lower = item.lower()
            found = False

            # 檢查項目中的關鍵字
            for key, keywords in keyword_mapping.items():
                if key in item:
                    if any(kw in content_lower for kw in keywords):
                        matches.append(item)
                        found = True
                        break

            if not found:
                # 直接檢查項目文字
                if any(word in content_lower for word in item_lower.split()):
                    matches.append(item)
                else:
                    misses.append(item)

        # 計算匹配分數
        total = len(must_include)
        matched = len(matches)
        match_score = matched / total if total > 0 else 1.0

        match_details = {
            'total_requirements': total,
            'matched': matched,
            'missing': len(misses),
            'matched_items': matches,
            'missing_items': misses
        }

        return round(match_score, 2), match_details

    def generate_report(
        self,
        analysis_result: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        生成 Markdown 格式的分析報告

        Args:
            analysis_result: 分析結果
            output_path: 輸出檔案路徑（可選）

        Returns:
            str: Markdown 報告內容
        """
        report = []

        # 標題
        report.append("# SEO 搜尋意圖分析報告\n")
        report.append(f"**分析時間**: {analysis_result['analyzed_at']}\n")
        report.append("---\n")

        # 關鍵字和意圖
        report.append("## 🎯 主要關鍵字\n")
        report.append(f"**關鍵字**: {analysis_result['keyword']}\n")

        report.append("\n## 📊 意圖分類\n")
        report.append(f"- **主要意圖**: {analysis_result['intent_label']} ({analysis_result['primary_intent']})\n")
        report.append(f"- **信心度**: {analysis_result['confidence'] * 100:.0f}%\n")

        # 其他可能的意圖
        if analysis_result.get('all_scores'):
            report.append("\n**其他可能意圖**:\n")
            for intent, score in sorted(
                analysis_result['all_scores'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                if intent != analysis_result['primary_intent']:
                    report.append(f"- {self._get_intent_label(intent)}: {score}\n")

        # 推薦結構
        rec = analysis_result.get('recommendations', {})

        report.append("\n## 💡 推薦文章結構\n")
        report.append(f"### 標題格式\n")
        report.append(f"```\n{rec.get('title_format', 'N/A')}\n```\n")

        report.append("\n**範例標題**:\n")
        for example in rec.get('title_examples', []):
            report.append(f"- {example}\n")

        report.append("\n### 必須包含的元素\n")
        for item in rec.get('must_include', []):
            report.append(f"- {item}\n")

        report.append("\n### 建議結構\n")
        report.append("```markdown\n")
        for section in rec.get('structure_template', []):
            report.append(f"{section}\n")
        report.append("```\n")

        report.append("\n### 語氣風格\n")
        report.append(f"- **建議語氣**: {rec.get('tone', 'N/A')}\n")
        report.append(f"- **行動呼籲 (CTA)**: {rec.get('cta', 'N/A')}\n")

        # 如果有匹配度分析
        if analysis_result.get('match_score') is not None:
            match_score = analysis_result['match_score']
            match_details = analysis_result['match_details']

            report.append("\n## 📈 當前文章匹配度\n")
            report.append(f"**匹配分數**: {match_score:.2f} / 1.0\n")

            # 用進度條表示
            progress = int(match_score * 20)
            bar = "█" * progress + "░" * (20 - progress)
            report.append(f"```\n{bar} {match_score * 100:.0f}%\n```\n")

            report.append(f"\n### 匹配詳情\n")
            report.append(f"- 必要元素總數: {match_details['total_requirements']}\n")
            report.append(f"- 已包含: {match_details['matched']}\n")
            report.append(f"- 缺少: {match_details['missing']}\n")

            if match_details.get('matched_items'):
                report.append("\n✅ **已包含的元素**:\n")
                for item in match_details['matched_items']:
                    report.append(f"- {item}\n")

            if match_details.get('missing_items'):
                report.append("\n⚠️ **缺少的元素**:\n")
                for item in match_details['missing_items']:
                    report.append(f"- {item}\n")

            # 優化建議
            report.append("\n## 🔧 優化建議\n")
            if match_score >= 0.9:
                report.append("✅ **文章結構非常符合搜尋意圖！**\n")
                report.append("- 維持當前結構\n")
                report.append("- 確保內容深度和品質\n")
            elif match_score >= 0.7:
                report.append("⚠️ **文章基本符合搜尋意圖，但有改進空間**\n")
                report.append("\n建議補充:\n")
                for item in match_details.get('missing_items', [])[:3]:
                    report.append(f"1. 增加「{item}」相關內容\n")
            else:
                report.append("❌ **文章結構與搜尋意圖差異較大**\n")
                report.append("\n強烈建議:\n")
                report.append(f"1. 按照「{rec.get('title_format', '')}」格式調整標題\n")
                report.append(f"2. 重新組織文章結構，參考上述建議結構\n")
                report.append(f"3. 補充缺少的必要元素（特別是前 {min(3, len(match_details.get('missing_items', [])))} 項）\n")

        # 參考資料
        report.append("\n## 📚 參考資料\n")
        report.append("- [Google 搜尋意圖指南](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)\n")
        report.append("- SEO 意圖匹配最佳實踐\n")

        report_content = "".join(report)

        # 如果指定輸出路徑，儲存檔案
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)

            print(f"✅ 報告已儲存至: {output_file}")

        return report_content


def main():
    """命令行使用介面"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='SEO 搜尋意圖分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 分析關鍵字
  python intent_analyzer.py analyze "如何使用 Claude Code"

  # 分析並產生報告
  python intent_analyzer.py analyze "Claude Code 教學" --output output/intent_analysis.md

  # 分析關鍵字並比對文章
  python intent_analyzer.py analyze "AI Agent 開發" --article output/session_xxx/final_article.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用指令')

    # analyze 子命令
    analyze_parser = subparsers.add_parser('analyze', help='分析關鍵字的搜尋意圖')
    analyze_parser.add_argument('keyword', help='要分析的關鍵字')
    analyze_parser.add_argument('--article', '-a', help='文章檔案路徑（用於匹配度分析）')
    analyze_parser.add_argument('--output', '-o', help='報告輸出路徑')
    analyze_parser.add_argument('--json', action='store_true', help='以 JSON 格式輸出')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'analyze':
        analyzer = IntentAnalyzer()

        # 讀取文章內容（如果提供）
        article_content = None
        if args.article:
            article_path = Path(args.article)
            if article_path.exists():
                with open(article_path, 'r', encoding='utf-8') as f:
                    article_content = f.read()
                print(f"📄 已載入文章: {args.article}\n")
            else:
                print(f"⚠️  找不到文章檔案: {args.article}\n")

        # 執行分析
        print(f"🔍 分析關鍵字: {args.keyword}\n")
        result = analyzer.analyze(args.keyword, article_content)

        if args.json:
            # JSON 輸出
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Markdown 報告
            report = analyzer.generate_report(result, args.output)

            if not args.output:
                print(report)


if __name__ == "__main__":
    main()
