#!/usr/bin/env python3
"""
Originality Checker - 原創性檢測器
防止 Google SpamBrain 懲罰

SpamBrain 是 Google 的 AI 驅動反垃圾系統，檢測：
- 抄襲/複製內容
- 低品質改寫
- 內容農場模式
- 過度相似的文章

2025 年 8 月更新後，SpamBrain 更嚴格

Version: 1.0.0
Date: 2025-11-04
"""

import re
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class OriginalityScore:
    """原創性評分結果"""
    overall_score: float  # 總分 (0-100)
    unique_content_ratio: float  # 獨特內容比例 (0-1)
    duplicate_phrases: List[str]  # 重複的片段
    similarity_warnings: List[str]  # 相似度警告
    quality_status: str  # excellent/good/acceptable/poor
    risk_level: str  # low/medium/high


class OriginalityChecker:
    """原創性檢測器"""

    def __init__(self):
        self.min_phrase_length = 10  # 最小檢查片段長度（字）
        self.similarity_threshold = 0.8  # 相似度警告閾值
        self.duplicate_threshold = 0.3  # 重複內容警告閾值

    def check_article(
        self,
        article_path: str,
        reference_articles: Optional[List[str]] = None
    ) -> OriginalityScore:
        """
        檢查文章原創性

        Args:
            article_path: 待檢查文章路徑
            reference_articles: 參考文章列表（可選，用於比對）

        Returns:
            OriginalityScore: 原創性評分
        """
        # 讀取文章
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 清理並提取純文本
        clean_content = self._clean_content(content)

        # 檢查 1: 自我重複檢測
        self_dup_ratio, duplicate_phrases = self._check_self_duplication(clean_content)

        # 檢查 2: 與參考文章比對（如果提供）
        similarity_warnings = []
        max_similarity = 0.0

        if reference_articles:
            for ref_path in reference_articles:
                similarity, warnings = self._compare_with_reference(
                    clean_content,
                    ref_path
                )
                max_similarity = max(max_similarity, similarity)
                similarity_warnings.extend(warnings)

        # 檢查 3: 常見抄襲模式
        pattern_warnings = self._check_plagiarism_patterns(clean_content)
        similarity_warnings.extend(pattern_warnings)

        # 計算獨特內容比例
        unique_ratio = 1.0 - self_dup_ratio

        # 如果有參考文章，考慮外部相似度
        if reference_articles and max_similarity > 0:
            unique_ratio = min(unique_ratio, 1.0 - max_similarity)

        # 計算總分 (0-100)
        overall_score = self._calculate_overall_score(
            unique_ratio,
            len(duplicate_phrases),
            len(similarity_warnings)
        )

        # 判斷品質狀態
        quality_status = self._assess_quality(overall_score)

        # 判斷風險等級
        risk_level = self._assess_risk(overall_score, unique_ratio)

        return OriginalityScore(
            overall_score=overall_score,
            unique_content_ratio=unique_ratio,
            duplicate_phrases=duplicate_phrases,
            similarity_warnings=similarity_warnings,
            quality_status=quality_status,
            risk_level=risk_level
        )

    def _clean_content(self, content: str) -> str:
        """清理內容，提取純文本"""
        # 移除 frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # 移除程式碼區塊（不檢查程式碼重複）
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

        # 移除行內程式碼
        content = re.sub(r'`[^`]+`', '', content)

        # 移除連結
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

        # 移除圖片
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)

        # 移除 markdown 格式
        content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^*]+)\*', r'\1', content)

        # 移除標題符號
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

        # 正規化空白
        content = re.sub(r'\s+', ' ', content)

        return content.strip()

    def _check_self_duplication(self, content: str) -> Tuple[float, List[str]]:
        """
        檢查文章內部的自我重複

        Returns:
            (重複比例, 重複片段列表)
        """
        # 分割成句子
        sentences = self._split_into_sentences(content)

        if len(sentences) < 3:
            return 0.0, []

        # 建立句子指紋
        sentence_hashes = {}
        duplicate_phrases = []

        for sentence in sentences:
            if len(sentence) < self.min_phrase_length:
                continue

            # 正規化句子（移除標點、空白）
            normalized = re.sub(r'[^\w]', '', sentence.lower())

            # 計算指紋
            fingerprint = hashlib.md5(normalized.encode()).hexdigest()[:16]

            if fingerprint in sentence_hashes:
                # 發現重複
                if sentence not in duplicate_phrases:
                    duplicate_phrases.append(sentence[:100] + "..." if len(sentence) > 100 else sentence)
            else:
                sentence_hashes[fingerprint] = sentence

        # 計算重複比例
        duplicate_ratio = len(duplicate_phrases) / len(sentences) if sentences else 0.0

        return duplicate_ratio, duplicate_phrases

    def _split_into_sentences(self, content: str) -> List[str]:
        """分割文本為句子"""
        # 以句號、問號、驚嘆號分割
        sentences = re.split(r'[。！？.!?]\s*', content)

        # 過濾空句子和太短的句子
        sentences = [s.strip() for s in sentences if len(s.strip()) >= self.min_phrase_length]

        return sentences

    def _compare_with_reference(
        self,
        content: str,
        reference_path: str
    ) -> Tuple[float, List[str]]:
        """
        與參考文章比對相似度

        Returns:
            (相似度分數 0-1, 警告列表)
        """
        # 讀取參考文章
        try:
            with open(reference_path, 'r', encoding='utf-8') as f:
                ref_content = f.read()
        except Exception as e:
            return 0.0, [f"無法讀取參考文章 {reference_path}: {e}"]

        # 清理參考內容
        ref_clean = self._clean_content(ref_content)

        # 計算整體相似度
        similarity = SequenceMatcher(None, content, ref_clean).ratio()

        warnings = []

        if similarity > self.similarity_threshold:
            warnings.append(
                f"⚠️ 與 {Path(reference_path).name} 相似度過高: {similarity:.1%}"
            )

        # 檢查共同片段
        common_phrases = self._find_common_phrases(content, ref_clean)

        if len(common_phrases) > 3:
            warnings.append(
                f"⚠️ 與 {Path(reference_path).name} 有 {len(common_phrases)} 個相同片段"
            )

        return similarity, warnings

    def _find_common_phrases(self, text1: str, text2: str) -> List[str]:
        """找出兩個文本的共同片段"""
        sentences1 = set(self._split_into_sentences(text1))
        sentences2 = set(self._split_into_sentences(text2))

        # 找出完全相同的句子
        common = sentences1 & sentences2

        # 過濾太短的
        common = [s for s in common if len(s) >= self.min_phrase_length]

        return list(common)

    def _check_plagiarism_patterns(self, content: str) -> List[str]:
        """
        檢查常見的抄襲模式

        SpamBrain 會檢測的模式：
        - 過度引用而無原創評論
        - 列表式內容（沒有深度）
        - 重複的開頭/結尾
        """
        warnings = []

        # 模式 1: 過多「根據...」「據...」（可能是過度引用）
        quote_count = len(re.findall(r'根據|據[^說]|引用|來源', content))
        sentences_count = len(self._split_into_sentences(content))

        if sentences_count > 0 and quote_count / sentences_count > 0.2:
            warnings.append(
                f"⚠️ 過度引用：{quote_count} 處引用 / {sentences_count} 句 "
                f"({quote_count/sentences_count:.1%}，建議 < 20%)"
            )

        # 模式 2: 過多列表而無段落說明（內容農場模式）
        list_items = len(re.findall(r'^\s*[-*]\s+', content, re.MULTILINE))
        paragraphs = len(re.split(r'\n\n+', content))

        if paragraphs > 0 and list_items / paragraphs > 2:
            warnings.append(
                f"⚠️ 過度列表化：{list_items} 個列表項 / {paragraphs} 段 "
                f"（建議加入更多段落說明）"
            )

        # 模式 3: 重複的句式結構（AI生成內容特徵）
        sentence_starts = [s[:20] for s in self._split_into_sentences(content) if len(s) >= 20]
        if len(sentence_starts) > 10:
            # 檢查開頭重複
            start_patterns = {}
            for start in sentence_starts:
                # 取前3字作為模式
                pattern = start[:6]
                start_patterns[pattern] = start_patterns.get(pattern, 0) + 1

            max_repeat = max(start_patterns.values())
            if max_repeat > len(sentence_starts) * 0.3:
                warnings.append(
                    f"⚠️ 句式結構過於重複：某種開頭出現 {max_repeat} 次 "
                    f"（建議多樣化句式）"
                )

        return warnings

    def _calculate_overall_score(
        self,
        unique_ratio: float,
        duplicate_count: int,
        warning_count: int
    ) -> float:
        """
        計算總體原創性分數

        算法：
        - 基礎分 = unique_ratio * 100
        - 每個重複片段 -5 分
        - 每個警告 -3 分
        """
        base_score = unique_ratio * 100

        # 扣分
        penalty = duplicate_count * 5 + warning_count * 3

        overall = max(0, min(100, base_score - penalty))

        return round(overall, 1)

    def _assess_quality(self, score: float) -> str:
        """評估品質等級"""
        if score >= 85:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 50:
            return 'acceptable'
        else:
            return 'poor'

    def _assess_risk(self, score: float, unique_ratio: float) -> str:
        """評估 SpamBrain 風險等級"""
        if score >= 80 and unique_ratio >= 0.9:
            return 'low'
        elif score >= 60 and unique_ratio >= 0.7:
            return 'medium'
        else:
            return 'high'

    def generate_markdown_report(
        self,
        score: OriginalityScore,
        output_path: Optional[str] = None
    ) -> str:
        """
        生成 Markdown 格式的原創性報告

        Args:
            score: 原創性評分
            output_path: 輸出檔案路徑（可選）

        Returns:
            str: Markdown 格式報告
        """
        # 狀態 emoji
        quality_emoji = {
            'excellent': '🟢',
            'good': '🟡',
            'acceptable': '🟠',
            'poor': '🔴'
        }

        risk_emoji = {
            'low': '✅',
            'medium': '⚠️',
            'high': '🔴'
        }

        report = f"""# 原創性檢測報告

## 📊 總體評分

**原創性分數**: {score.overall_score}/100 {quality_emoji[score.quality_status]}

**品質等級**: {score.quality_status.upper()}

**SpamBrain 風險**: {risk_emoji[score.risk_level]} {score.risk_level.upper()}

---

## 📈 詳細指標

### 獨特內容比例
**{score.unique_content_ratio:.1%}** ({quality_emoji[score.quality_status]})

- 🟢 優秀: >= 90%
- 🟡 良好: 70-89%
- 🟠 可接受: 50-69%
- 🔴 不佳: < 50%

### 重複片段數量
**{len(score.duplicate_phrases)} 個**

### 相似度警告
**{len(score.similarity_warnings)} 個**

---

## ⚠️ 檢測到的問題

"""

        # 列出重複片段
        if score.duplicate_phrases:
            report += "### 內部重複片段\n\n"
            for i, phrase in enumerate(score.duplicate_phrases[:10], 1):
                report += f"{i}. {phrase}\n"

            if len(score.duplicate_phrases) > 10:
                report += f"\n*還有 {len(score.duplicate_phrases) - 10} 個重複片段...*\n"

            report += "\n"
        else:
            report += "### ✅ 無內部重複\n\n"

        # 列出相似度警告
        if score.similarity_warnings:
            report += "### 相似度警告\n\n"
            for warning in score.similarity_warnings:
                report += f"- {warning}\n"
            report += "\n"
        else:
            report += "### ✅ 無外部相似度問題\n\n"

        report += "---\n\n## 💡 改進建議\n\n"

        # 根據狀態提供建議
        if score.quality_status == 'excellent':
            report += "🎉 **原創性優秀！** 內容完全符合原創性標準。\n\n"
            report += "✅ 可以安全發布，無 SpamBrain 風險。\n\n"

        elif score.quality_status == 'good':
            report += "👍 **原創性良好**，但有改進空間：\n\n"

            if len(score.duplicate_phrases) > 0:
                report += "- 減少文章內的自我重複，改寫重複片段\n"

            if len(score.similarity_warnings) > 0:
                report += "- 檢查與參考文章的相似內容，增加個人觀點\n"

            report += "\n✅ 可以發布，SpamBrain 風險較低。\n\n"

        elif score.quality_status == 'acceptable':
            report += "⚠️ **原創性可接受，但建議改進**：\n\n"

            report += "**優先改進項目**：\n"

            if score.unique_content_ratio < 0.7:
                report += "- 🔴 **重點**：增加獨特內容，減少重複\n"

            if len(score.duplicate_phrases) > 5:
                report += "- ⚠️ 重寫重複片段，使用不同的表達方式\n"

            if len(score.similarity_warnings) > 2:
                report += "- ⚠️ 增加原創見解，減少對參考資料的依賴\n"

            report += "\n⚠️ 可以發布，但存在 SpamBrain 風險，建議優化。\n\n"

        else:  # poor
            report += "🔴 **原創性不足，強烈建議修改後再發布**：\n\n"

            report += "**嚴重問題**：\n"

            if score.unique_content_ratio < 0.5:
                report += "- 🔴 獨特內容比例過低 ({:.1%})，需要大幅改寫\n".format(score.unique_content_ratio)

            if len(score.duplicate_phrases) > 10:
                report += "- 🔴 過多重複片段 ({}個)，需要減少自我重複\n".format(len(score.duplicate_phrases))

            if len(score.similarity_warnings) > 5:
                report += "- 🔴 與參考文章過於相似，需要加入原創內容\n"

            report += "\n🔴 **高 SpamBrain 風險**：不建議立即發布，請先修改。\n\n"

            report += "### 修改建議\n\n"
            report += "1. **增加原創觀點**：加入個人經驗、案例、分析\n"
            report += "2. **改寫重複內容**：用不同方式表達相同概念\n"
            report += "3. **減少引用比例**：確保原創內容 > 引用內容\n"
            report += "4. **加入實例和細節**：具體的案例和數據\n"
            report += "5. **檢查 E-E-A-T**：確保有第一手經驗和專業見解\n\n"

        report += "---\n\n## 🛡️ SpamBrain 防護建議\n\n"

        report += """### Google SpamBrain 會檢測：

1. **抄襲內容**
   - 直接複製他人文章
   - 低品質改寫（僅改動少數詞彙）
   - 內容農場式的文章拼湊

2. **過度相似**
   - 與自己其他文章過度重複
   - 與網路上已有內容高度相似
   - 使用相同模板生成大量相似文章

3. **低品質模式**
   - 純列表式內容，無深度分析
   - 過度引用，缺乏原創觀點
   - AI 生成但未經人工編輯

### ✅ 防護策略：

- **確保獨特內容 >= 80%**
- **加入第一手經驗** (E-E-A-T 的 Experience)
- **提供原創見解和分析**
- **避免大量產生相似文章**
- **定期檢查原創性**

"""

        report += f"\n---\n\n*報告生成時間: {self._get_timestamp()}*\n"

        # 如果指定輸出路徑，寫入檔案
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 原創性報告已生成: {output_path}")

        return report

    def _get_timestamp(self) -> str:
        """取得當前時間戳記"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    """命令行介面"""
    parser = argparse.ArgumentParser(
        description='檢查文章原創性，防止 SpamBrain 懲罰'
    )
    parser.add_argument(
        'article',
        help='待檢查的文章檔案路徑'
    )
    parser.add_argument(
        '-r', '--reference',
        nargs='*',
        help='參考文章列表（用於比對）'
    )
    parser.add_argument(
        '-o', '--output',
        help='輸出報告路徑（可選）'
    )

    args = parser.parse_args()

    # 創建檢測器
    checker = OriginalityChecker()

    # 執行檢測
    print(f"🔍 檢查文章: {args.article}")

    if args.reference:
        print(f"📚 參考文章: {len(args.reference)} 篇")

    score = checker.check_article(args.article, args.reference)

    # 生成報告
    report = checker.generate_markdown_report(score, args.output)

    # 如果沒有指定輸出路徑，列印到終端
    if not args.output:
        print("\n" + report)

    # 顯示摘要
    quality_emoji = {'excellent': '🟢', 'good': '🟡', 'acceptable': '🟠', 'poor': '🔴'}
    risk_emoji = {'low': '✅', 'medium': '⚠️', 'high': '🔴'}

    print(f"\n{quality_emoji[score.quality_status]} 原創性: {score.overall_score}/100 ({score.quality_status.upper()})")
    print(f"{risk_emoji[score.risk_level]} SpamBrain 風險: {score.risk_level.upper()}")
    print(f"📊 獨特內容比例: {score.unique_content_ratio:.1%}")


if __name__ == '__main__':
    main()
