#!/usr/bin/env python3
"""
AI Overviews Summary Generator
為 Google AI Overviews 生成優化的摘要框

Google AI Overviews 在 2025 年 9 月已覆蓋 30% 的美國桌面查詢
關鍵優化要素：
- 50-70 字的簡潔摘要
- 直接回答目標問題
- 簡單易懂的語言
- 快速切入重點

Version: 1.0.0
Date: 2025-11-04
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SummaryBox:
    """摘要框數據結構"""
    title: str  # 問題或主題
    summary: str  # 50-70 字摘要
    word_count: int  # 字數
    key_points: List[str]  # 3-5 個關鍵點
    readability_score: float  # 可讀性分數 (0-100)
    quality_status: str  # excellent/good/needs_improvement


class SummaryGenerator:
    """AI Overviews 摘要生成器"""

    def __init__(self):
        self.target_length_min = 50
        self.target_length_max = 70
        self.max_key_points = 5

    def generate_from_article(
        self,
        article_path: str,
        target_keyword: Optional[str] = None
    ) -> SummaryBox:
        """
        從文章生成 AI Overviews 優化的摘要

        Args:
            article_path: 文章檔案路徑
            target_keyword: 目標關鍵字（可選）

        Returns:
            SummaryBox: 生成的摘要框
        """
        # 讀取文章
        content = self._read_article(article_path)

        # 提取標題
        title = self._extract_title(content, target_keyword)

        # 生成摘要
        summary = self._generate_summary(content, target_keyword)

        # 提取關鍵點
        key_points = self._extract_key_points(content)

        # 計算字數
        word_count = len(summary)

        # 評估可讀性
        readability_score = self._calculate_readability(summary)

        # 判斷品質
        quality_status = self._assess_quality(
            word_count,
            readability_score,
            key_points
        )

        return SummaryBox(
            title=title,
            summary=summary,
            word_count=word_count,
            key_points=key_points,
            readability_score=readability_score,
            quality_status=quality_status
        )

    def _read_article(self, article_path: str) -> str:
        """讀取文章內容"""
        with open(article_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_title(self, content: str, keyword: Optional[str]) -> str:
        """
        提取或生成問題形式的標題
        AI Overviews 偏好問答格式
        """
        # 嘗試從 frontmatter 提取
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            # 從第一個 H1 提取
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = h1_match.group(1) if h1_match else "文章摘要"

        # 如果標題不是問句，嘗試轉換
        if not any(q in title for q in ['什麼', '如何', '為什麼', '怎麼', '?', '？']):
            # 根據關鍵字生成問句
            if keyword:
                if '教學' in title or '指南' in title:
                    title = f"如何{keyword}？"
                elif '是什麼' not in title:
                    title = f"什麼是{keyword}？"

        return title

    def _generate_summary(self, content: str, keyword: Optional[str]) -> str:
        """
        生成 50-70 字的快速摘要

        策略：
        1. 提取文章第一段
        2. 找到核心論述
        3. 簡化為 50-70 字
        """
        # 移除 frontmatter
        content_without_fm = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # 提取第一段（通常包含核心資訊）
        paragraphs = [p.strip() for p in content_without_fm.split('\n\n') if p.strip()]

        # 過濾掉標題和太短的段落
        first_meaningful_para = None
        for para in paragraphs:
            # 跳過標題
            if para.startswith('#'):
                continue
            # 跳過太短的段落
            if len(para) < 30:
                continue
            # 跳過圖片、連結等
            if para.startswith('![') or para.startswith('[TOC]'):
                continue

            first_meaningful_para = para
            break

        if not first_meaningful_para:
            first_meaningful_para = paragraphs[0] if paragraphs else "無法提取摘要"

        # 清理 markdown 格式
        summary = self._clean_markdown(first_meaningful_para)

        # 截取到 50-70 字
        summary = self._truncate_to_target_length(summary)

        return summary

    def _clean_markdown(self, text: str) -> str:
        """移除 markdown 格式標記"""
        # 移除粗體
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # 移除斜體
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        # 移除連結
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        # 移除程式碼
        text = re.sub(r'`(.+?)`', r'\1', text)
        # 移除標題符號
        text = re.sub(r'^#+\s+', '', text)

        return text.strip()

    def _truncate_to_target_length(self, text: str) -> str:
        """
        截取到目標長度（50-70字）
        保持句子完整性
        """
        if len(text) <= self.target_length_max:
            return text

        # 尋找第一個句號、問號或驚嘆號
        sentence_ends = []
        for match in re.finditer(r'[。！？.!?]', text):
            pos = match.end()
            if pos >= self.target_length_min:
                sentence_ends.append(pos)

        if sentence_ends:
            # 選擇最接近 60 字的位置
            target = 60
            best_pos = min(sentence_ends, key=lambda x: abs(x - target))

            if best_pos <= self.target_length_max + 10:  # 允許稍微超過
                return text[:best_pos]

        # 如果找不到合適的斷點，在 70 字附近斷開
        truncated = text[:self.target_length_max]

        # 嘗試在最後一個空格或標點斷開
        last_space = max(
            truncated.rfind('，'),
            truncated.rfind('、'),
            truncated.rfind(' ')
        )

        if last_space > self.target_length_min:
            truncated = truncated[:last_space]

        return truncated + '...'

    def _extract_key_points(self, content: str) -> List[str]:
        """
        提取 3-5 個關鍵點
        優先從列表和小標題提取
        """
        key_points = []

        # 策略 1: 從 H2 標題提取
        h2_matches = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        for h2 in h2_matches[:self.max_key_points]:
            # 清理標題
            clean_h2 = self._clean_markdown(h2)
            # 移除序號
            clean_h2 = re.sub(r'^\d+[\.\、]\s*', '', clean_h2)
            key_points.append(clean_h2)

        # 如果 H2 不夠，從列表項提取
        if len(key_points) < 3:
            list_matches = re.findall(r'^[\-\*]\s+(.+)$', content, re.MULTILINE)
            for item in list_matches:
                if len(key_points) >= self.max_key_points:
                    break

                clean_item = self._clean_markdown(item)
                # 過濾太短的項目
                if len(clean_item) < 5:
                    continue
                # 避免重複
                if clean_item not in key_points:
                    key_points.append(clean_item)

        return key_points[:self.max_key_points]

    def _calculate_readability(self, text: str) -> float:
        """
        計算可讀性分數 (0-100)

        考慮因素：
        - 句子長度（越短越好）
        - 常用詞比例（越高越好）
        - 複雜標點（越少越好）
        """
        score = 100.0

        # 因素 1: 平均句子長度
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if sentences:
            avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)

            # 理想句子長度：10-20 字
            if avg_sentence_length > 25:
                score -= 15
            elif avg_sentence_length > 20:
                score -= 5

        # 因素 2: 複雜字詞（專業術語、英文等）
        # 簡化：檢測英文單詞和專業術語
        english_words = re.findall(r'[a-zA-Z]{4,}', text)
        if len(english_words) > 3:
            score -= 10

        # 因素 3: 複雜標點
        complex_punctuation = len(re.findall(r'[；：、「」『』【】]', text))
        if complex_punctuation > 3:
            score -= 5

        # 因素 4: 數字和數據（適量好，過多不好）
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 5:
            score -= 5

        return max(0, min(100, score))

    def _assess_quality(
        self,
        word_count: int,
        readability: float,
        key_points: List[str]
    ) -> str:
        """
        評估摘要品質

        Returns:
            'excellent' | 'good' | 'needs_improvement'
        """
        # 檢查字數
        length_ok = self.target_length_min <= word_count <= self.target_length_max + 10

        # 檢查可讀性
        readability_ok = readability >= 80

        # 檢查關鍵點
        key_points_ok = 3 <= len(key_points) <= 5

        # 評級
        if length_ok and readability_ok and key_points_ok:
            return 'excellent'
        elif length_ok and (readability_ok or key_points_ok):
            return 'good'
        else:
            return 'needs_improvement'

    def generate_markdown_report(
        self,
        summary_box: SummaryBox,
        output_path: Optional[str] = None
    ) -> str:
        """
        生成 Markdown 格式的 AI Overviews 優化報告

        Args:
            summary_box: 摘要框資料
            output_path: 輸出檔案路徑（可選）

        Returns:
            str: Markdown 格式報告
        """
        # 狀態 emoji
        status_emoji = {
            'excellent': '🟢',
            'good': '🟡',
            'needs_improvement': '🔴'
        }

        # 生成報告
        report = f"""# AI Overviews 摘要優化報告

## 📊 摘要框

### 問題/主題
**{summary_box.title}**

### 快速回答摘要
{summary_box.summary}

---

## 📈 品質指標

- **字數**: {summary_box.word_count} 字 (目標: 50-70)
- **可讀性分數**: {summary_box.readability_score:.1f}/100
- **關鍵點數量**: {len(summary_box.key_points)} 個
- **整體品質**: {status_emoji[summary_box.quality_status]} {summary_box.quality_status.upper()}

---

## 🎯 關鍵點 ({len(summary_box.key_points)} 個)

"""
        # 加入關鍵點
        for i, point in enumerate(summary_box.key_points, 1):
            report += f"{i}. {point}\n"

        report += "\n---\n\n## ✅ AI Overviews 優化檢查表\n\n"

        # 檢查項目
        length_ok = 50 <= summary_box.word_count <= 80
        readability_ok = summary_box.readability_score >= 80
        key_points_ok = 3 <= len(summary_box.key_points) <= 5

        report += f"- {'✅' if length_ok else '❌'} **字數適中** (50-70字，允許誤差)\n"
        report += f"- {'✅' if readability_ok else '❌'} **可讀性高** (分數 >= 80)\n"
        report += f"- {'✅' if key_points_ok else '❌'} **關鍵點完整** (3-5個)\n"
        report += f"- {'✅' if '?' in summary_box.title or '？' in summary_box.title else '⚠️'} **問答格式** (標題為問句)\n"

        report += "\n---\n\n## 💡 優化建議\n\n"

        # 根據品質提供建議
        if summary_box.quality_status == 'excellent':
            report += "🎉 **摘要品質優秀！** 完全符合 AI Overviews 優化標準。\n\n"
            report += "建議：\n"
            report += "- 確保在文章開頭使用此摘要\n"
            report += "- 考慮加入 FAQ Schema markup\n"
            report += "- 在 Meta Description 中使用類似的簡潔表達\n"

        elif summary_box.quality_status == 'good':
            report += "👍 **摘要品質良好**，但有改進空間：\n\n"

            if not length_ok:
                if summary_box.word_count < 50:
                    report += "- ⚠️ **摘要太短**：補充更多關鍵資訊，目標 50-70 字\n"
                else:
                    report += "- ⚠️ **摘要稍長**：精簡表達，移除冗餘詞彙\n"

            if not readability_ok:
                report += "- ⚠️ **可讀性可改進**：使用更簡單的詞彙，縮短句子\n"

            if not key_points_ok:
                if len(summary_box.key_points) < 3:
                    report += "- ⚠️ **關鍵點太少**：補充到 3-5 個關鍵點\n"
                else:
                    report += "- ⚠️ **關鍵點過多**：精簡到最重要的 3-5 個\n"

        else:  # needs_improvement
            report += "⚠️ **摘要需要改進**，建議重寫：\n\n"

            report += "**問題診斷**：\n"
            if not length_ok:
                report += f"- 字數問題：當前 {summary_box.word_count} 字，目標 50-70 字\n"
            if not readability_ok:
                report += f"- 可讀性問題：當前 {summary_box.readability_score:.1f} 分，目標 >= 80 分\n"
            if not key_points_ok:
                report += f"- 關鍵點問題：當前 {len(summary_box.key_points)} 個，目標 3-5 個\n"

            report += "\n**重寫建議**：\n"
            report += "1. 使用簡單、直白的語言\n"
            report += "2. 第一句話直接回答問題\n"
            report += "3. 避免專業術語和複雜句式\n"
            report += "4. 確保關鍵點清晰且可操作\n"

        report += "\n---\n\n## 📚 參考資料\n\n"
        report += "- Google AI Overviews 在 2025 年 9 月覆蓋 30% 的美國桌面查詢\n"
        report += "- 99%+ 的 AI Overviews 來源來自 Top 10 搜尋結果\n"
        report += "- E-E-A-T 在 AI Overviews 中被視為 'Non-Negotiable'\n"
        report += "- 建議使用 FAQ Schema 增加被引用機會\n"

        report += f"\n---\n\n*報告生成時間: {self._get_timestamp()}*\n"

        # 如果指定輸出路徑，寫入檔案
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ AI Overviews 報告已生成: {output_path}")

        return report

    def _get_timestamp(self) -> str:
        """取得當前時間戳記"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    """命令行介面"""
    parser = argparse.ArgumentParser(
        description='為 Google AI Overviews 生成優化的摘要框'
    )
    parser.add_argument(
        'article',
        help='文章檔案路徑'
    )
    parser.add_argument(
        '-k', '--keyword',
        help='目標關鍵字（可選）'
    )
    parser.add_argument(
        '-o', '--output',
        help='輸出報告路徑（可選）'
    )

    args = parser.parse_args()

    # 創建生成器
    generator = SummaryGenerator()

    # 生成摘要
    print(f"🔍 分析文章: {args.article}")
    summary_box = generator.generate_from_article(
        args.article,
        args.keyword
    )

    # 生成報告
    report = generator.generate_markdown_report(
        summary_box,
        args.output
    )

    # 如果沒有指定輸出路徑，列印到終端
    if not args.output:
        print("\n" + report)

    # 顯示狀態
    status_emoji = {
        'excellent': '🟢',
        'good': '🟡',
        'needs_improvement': '🔴'
    }

    print(f"\n{status_emoji[summary_box.quality_status]} 摘要品質: {summary_box.quality_status.upper()}")
    print(f"📊 字數: {summary_box.word_count}")
    print(f"📈 可讀性: {summary_box.readability_score:.1f}/100")


if __name__ == '__main__':
    main()
