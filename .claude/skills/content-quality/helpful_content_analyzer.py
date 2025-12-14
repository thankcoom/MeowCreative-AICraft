#!/usr/bin/env python3
"""
Helpful Content Analyzer - 有價值內容分析器
基於 Google Helpful Content System (2025)

Google Helpful Content System 核心原則：
- People-first content（用戶優先，而非搜尋引擎優先）
- 真實經驗和第一手知識
- 避免為排名而創作
- 提供實質價值

2025 年與核心更新、評論演算法整合為單一引擎
目標：減少 45% 低品質內容

Version: 1.0.0
Date: 2025-11-04
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class HelpfulnessScore:
    """有價值度評分結果"""
    overall_score: float  # 總分 (0-100)
    people_first_score: float  # 用戶優先分數
    value_density_score: float  # 價值密度分數
    actionability_score: float  # 可操作性分數
    authenticity_score: float  # 真實性分數
    red_flags: List[str]  # 紅旗警告
    green_signals: List[str]  # 正面信號
    quality_status: str  # excellent/good/acceptable/poor


class HelpfulContentAnalyzer:
    """有價值內容分析器"""

    def __init__(self):
        # SEO 過度優化的關鍵詞（負面信號）
        self.seo_spam_keywords = [
            '排名第一', '最好的', '最佳', '頂級', '冠軍',
            '絕對', '保證', '100%', '完美', '神器',
            '秒殺', '終極', '史上最強'
        ]

        # 有價值內容的正面信號
        self.value_signals = [
            '我的經驗', '實測', '親自試過', '實際使用',
            '舉例來說', '比如', '具體', '步驟', '方法',
            '優點是', '缺點是', '需要注意', '建議'
        ]

    def analyze(
        self,
        article_path: str,
        experience_profile_path: Optional[str] = None
    ) -> HelpfulnessScore:
        """
        分析文章的有價值度

        Args:
            article_path: 文章檔案路徑
            experience_profile_path: 經驗檔案路徑（可選）

        Returns:
            HelpfulnessScore: 有價值度評分
        """
        # 讀取文章
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 讀取經驗檔案（如果有）
        experience_data = None
        if experience_profile_path and Path(experience_profile_path).exists():
            with open(experience_profile_path, 'r', encoding='utf-8') as f:
                experience_data = f.read()

        # 清理內容
        clean_content = self._clean_content(content)

        # 分析 1: People-First vs SEO-First
        people_first_score, pf_flags, pf_signals = self._analyze_people_first(clean_content)

        # 分析 2: 價值密度（實質內容 vs 空話）
        value_density_score, vd_flags, vd_signals = self._analyze_value_density(clean_content)

        # 分析 3: 可操作性（讀者能否採取行動）
        actionability_score, act_flags, act_signals = self._analyze_actionability(clean_content)

        # 分析 4: 真實性（基於經驗檔案）
        authenticity_score, auth_flags, auth_signals = self._analyze_authenticity(
            clean_content,
            experience_data
        )

        # 合併所有紅旗和正面信號
        all_red_flags = pf_flags + vd_flags + act_flags + auth_flags
        all_green_signals = pf_signals + vd_signals + act_signals + auth_signals

        # 計算總分
        overall_score = self._calculate_overall_score(
            people_first_score,
            value_density_score,
            actionability_score,
            authenticity_score
        )

        # 判斷品質狀態
        quality_status = self._assess_quality(overall_score, len(all_red_flags))

        return HelpfulnessScore(
            overall_score=overall_score,
            people_first_score=people_first_score,
            value_density_score=value_density_score,
            actionability_score=actionability_score,
            authenticity_score=authenticity_score,
            red_flags=all_red_flags,
            green_signals=all_green_signals,
            quality_status=quality_status
        )

    def _clean_content(self, content: str) -> str:
        """清理內容"""
        # 移除 frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # 保留程式碼區塊（因為教學內容需要）但標記
        # content = re.sub(r'```.*?```', '[CODE_BLOCK]', content, flags=re.DOTALL)

        return content.strip()

    def _analyze_people_first(self, content: str) -> Tuple[float, List[str], List[str]]:
        """
        分析是否為用戶優先內容

        檢測：
        - 過度 SEO 優化（關鍵字堆砌）
        - 標題黨
        - 為排名而寫的跡象
        """
        red_flags = []
        green_signals = []
        score = 100.0

        # 檢測 1: SEO 垃圾關鍵詞
        spam_found = []
        for keyword in self.seo_spam_keywords:
            if keyword in content:
                spam_found.append(keyword)

        if len(spam_found) > 3:
            score -= 20
            red_flags.append(f"🚩 過度使用 SEO 誇大詞彙: {', '.join(spam_found[:5])}")
        elif len(spam_found) > 0:
            score -= 10
            red_flags.append(f"⚠️ 使用了部分誇大詞彙: {', '.join(spam_found)}")

        # 檢測 2: 關鍵字密度過高（可能是關鍵字堆砌）
        # 簡化：檢查某個詞彙的過度重複
        words = content.split()
        word_freq = {}
        for word in words:
            if len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1

        max_freq = max(word_freq.values()) if word_freq else 0
        if len(words) > 0 and max_freq / len(words) > 0.05:
            score -= 15
            most_common = max(word_freq, key=word_freq.get)
            red_flags.append(
                f"🚩 關鍵字過度重複: '{most_common}' 出現 {max_freq} 次 "
                f"({max_freq/len(words):.1%}，建議 < 5%)"
            )

        # 檢測 3: 標題黨模式
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            clickbait_patterns = ['你不知道', '震驚', '絕對', '必看', '必讀', '不看後悔']
            if any(pattern in title for pattern in clickbait_patterns):
                score -= 15
                red_flags.append(f"🚩 標題可能是標題黨: {title}")

        # 正面信號：使用用戶導向語言
        user_oriented = ['你可以', '幫助你', '讓你', '適合你', '如果你', '你需要']
        user_count = sum(1 for phrase in user_oriented if phrase in content)

        if user_count >= 5:
            green_signals.append(f"✅ 使用用戶導向語言 ({user_count} 處)")
        elif user_count >= 3:
            score += 5

        return max(0, min(100, score)), red_flags, green_signals

    def _analyze_value_density(self, content: str) -> Tuple[float, List[str], List[str]]:
        """
        分析價值密度

        檢測：
        - 空話比例（廢話、陳詞濫調）
        - 實質內容比例
        - 深度 vs 廣度
        """
        red_flags = []
        green_signals = []
        score = 100.0

        # 檢測 1: 常見空話
        fluff_phrases = [
            '眾所周知', '毋庸置疑', '不言而喻', '顯而易見',
            '在當今社會', '隨著科技的發展', '在這個時代',
            '總的來說', '綜上所述'  # 這些可以用，但過多就是空話
        ]

        fluff_count = sum(1 for phrase in fluff_phrases if phrase in content)
        total_sentences = len(re.split(r'[。！？.!?]', content))

        if total_sentences > 0 and fluff_count / total_sentences > 0.15:
            score -= 20
            red_flags.append(
                f"🚩 空話比例過高: {fluff_count} / {total_sentences} "
                f"({fluff_count/total_sentences:.1%}，建議 < 15%)"
            )

        # 檢測 2: 實質內容信號（數據、案例、步驟）
        value_signals_found = []

        # 數據
        numbers = len(re.findall(r'\d+[%％]|\d+\.\d+|\d+個|第\d+', content))
        if numbers >= 5:
            value_signals_found.append(f"數據 ({numbers} 處)")

        # 案例/例子
        examples = len(re.findall(r'例如|比如|舉例|案例|範例|實例', content))
        if examples >= 3:
            value_signals_found.append(f"案例 ({examples} 處)")

        # 步驟
        steps = len(re.findall(r'步驟|第[一二三四五六七八九十\d]+步|^\d+\.|^[-*]\s', content, re.MULTILINE))
        if steps >= 3:
            value_signals_found.append(f"步驟 ({steps} 處)")

        if len(value_signals_found) >= 2:
            green_signals.append(f"✅ 包含實質內容: {', '.join(value_signals_found)}")
            score += 10
        elif len(value_signals_found) == 0:
            score -= 15
            red_flags.append("🚩 缺乏實質內容（無數據、案例、步驟）")

        # 檢測 3: 深度（文章長度 + 細節）
        word_count = len(content)

        if word_count < 500:
            score -= 20
            red_flags.append(f"🚩 內容過短 ({word_count} 字，建議 >= 800 字)")
        elif word_count < 800:
            score -= 10
            red_flags.append(f"⚠️ 內容偏短 ({word_count} 字，建議 >= 800 字)")
        elif word_count >= 1500:
            green_signals.append(f"✅ 內容豐富 ({word_count} 字)")
            score += 5

        return max(0, min(100, score)), red_flags, green_signals

    def _analyze_actionability(self, content: str) -> Tuple[float, List[str], List[str]]:
        """
        分析可操作性

        檢測：
        - 是否提供可執行的建議
        - 是否有明確的步驟
        - 是否有實用的工具/資源
        """
        red_flags = []
        green_signals = []
        score = 100.0

        # 檢測 1: 行動導向語言
        action_verbs = [
            '可以', '建議', '試試', '嘗試', '使用', '執行',
            '開始', '設定', '配置', '安裝', '下載', '點擊'
        ]

        action_count = sum(1 for verb in action_verbs if verb in content)

        if action_count >= 10:
            green_signals.append(f"✅ 包含豐富的行動指引 ({action_count} 處)")
            score += 10
        elif action_count >= 5:
            green_signals.append(f"✅ 包含行動指引 ({action_count} 處)")
        elif action_count < 3:
            score -= 15
            red_flags.append("🚩 缺乏可操作的建議")

        # 檢測 2: 具體步驟
        steps = len(re.findall(
            r'步驟\s*\d+|第[一二三四五六七八九十\d]+步|^\d+\.',
            content,
            re.MULTILINE
        ))

        if steps >= 5:
            green_signals.append(f"✅ 提供清晰的步驟指引 ({steps} 個步驟)")
            score += 10
        elif steps >= 3:
            green_signals.append(f"✅ 包含步驟說明 ({steps} 個步驟)")

        # 檢測 3: 工具和資源
        resources = len(re.findall(r'工具|軟體|平台|網站|資源|下載|連結', content))

        if resources >= 5:
            green_signals.append(f"✅ 提供實用工具/資源 ({resources} 處)")
            score += 5

        # 檢測 4: 程式碼範例（技術文章的可操作性）
        code_blocks = len(re.findall(r'```', content))

        if code_blocks >= 2:
            green_signals.append(f"✅ 包含程式碼範例 ({code_blocks // 2} 個)")
            score += 10

        return max(0, min(100, score)), red_flags, green_signals

    def _analyze_authenticity(
        self,
        content: str,
        experience_data: Optional[str]
    ) -> Tuple[float, List[str], List[str]]:
        """
        分析真實性

        檢測：
        - 是否有第一手經驗
        - 是否有個人觀點
        - 是否有真實的優缺點評價
        """
        red_flags = []
        green_signals = []
        score = 100.0

        # 檢測 1: 第一人稱經驗
        first_person = len(re.findall(r'我[的在用試做]|我們[的在用試做]', content))

        if first_person >= 5:
            green_signals.append(f"✅ 包含第一手經驗 ({first_person} 處)")
            score += 15
        elif first_person >= 2:
            green_signals.append(f"✅ 有個人觀點 ({first_person} 處)")
            score += 5
        elif first_person == 0:
            score -= 20
            red_flags.append("🚩 缺乏第一手經驗（無第一人稱敘述）")

        # 檢測 2: 真實的優缺點評價
        pros_cons = (
            len(re.findall(r'優點|好處|優勢|益處', content)) > 0 and
            len(re.findall(r'缺點|不足|限制|缺陷|問題', content)) > 0
        )

        if pros_cons:
            green_signals.append("✅ 提供平衡的優缺點評價")
            score += 15
        else:
            score -= 15
            red_flags.append("🚩 缺乏平衡評價（只有優點或只有缺點）")

        # 檢測 3: 與經驗檔案的一致性
        if experience_data:
            # 檢查文章是否提到經驗檔案中的關鍵資訊
            # 簡化：檢查是否有時間參考
            has_time_ref = bool(re.search(r'\d{4}年|\d+個月|最近|上週|去年', content))

            if has_time_ref:
                green_signals.append("✅ 包含具體時間參考（真實性指標）")
                score += 10
        else:
            # 沒有經驗檔案，檢查文章本身的真實性信號
            if not re.search(r'實測|親自|實際|真實|體驗', content):
                score -= 10
                red_flags.append("⚠️ 缺乏真實性信號（建議加入實測、親身體驗）")

        # 檢測 4: 避免過度正面或過度負面
        positive_words = len(re.findall(r'很好|非常好|極佳|完美|優秀|推薦', content))
        negative_words = len(re.findall(r'很差|非常差|糟糕|不推薦|避免', content))
        total_sentences = len(re.split(r'[。！？.!?]', content))

        if total_sentences > 0:
            sentiment_ratio = abs(positive_words - negative_words) / total_sentences

            if sentiment_ratio > 0.3:
                score -= 10
                red_flags.append("⚠️ 情緒過於極端（過度正面或負面）")

        return max(0, min(100, score)), red_flags, green_signals

    def _calculate_overall_score(
        self,
        people_first: float,
        value_density: float,
        actionability: float,
        authenticity: float
    ) -> float:
        """
        計算總體有價值度分數

        權重：
        - People-First: 30%（最重要）
        - Authenticity: 30%（與 E-E-A-T 對應）
        - Value Density: 25%
        - Actionability: 15%
        """
        overall = (
            people_first * 0.30 +
            authenticity * 0.30 +
            value_density * 0.25 +
            actionability * 0.15
        )

        return round(overall, 1)

    def _assess_quality(self, score: float, red_flag_count: int) -> str:
        """評估品質等級"""
        # 如果有嚴重紅旗，降級
        if red_flag_count >= 5:
            return 'poor'
        elif red_flag_count >= 3:
            return 'acceptable' if score >= 60 else 'poor'

        # 基於分數評級
        if score >= 80:
            return 'excellent'
        elif score >= 65:
            return 'good'
        elif score >= 50:
            return 'acceptable'
        else:
            return 'poor'

    def generate_markdown_report(
        self,
        score: HelpfulnessScore,
        output_path: Optional[str] = None
    ) -> str:
        """
        生成 Markdown 格式的有價值度報告

        Args:
            score: 有價值度評分
            output_path: 輸出檔案路徑（可選）

        Returns:
            str: Markdown 格式報告
        """
        quality_emoji = {
            'excellent': '🟢',
            'good': '🟡',
            'acceptable': '🟠',
            'poor': '🔴'
        }

        report = f"""# Helpful Content 有價值度分析報告

## 📊 總體評分

**有價值度分數**: {score.overall_score}/100 {quality_emoji[score.quality_status]}

**品質等級**: {score.quality_status.upper()}

---

## 📈 四大維度分數

### 1. People-First (用戶優先) - 權重 30%
**{score.people_first_score:.1f}/100** {quality_emoji[self._score_to_quality(score.people_first_score)]}

檢測內容是否為用戶而寫，而非為 SEO 排名而寫

### 2. Authenticity (真實性) - 權重 30%
**{score.authenticity_score:.1f}/100** {quality_emoji[self._score_to_quality(score.authenticity_score)]}

檢測是否有第一手經驗和真實觀點

### 3. Value Density (價值密度) - 權重 25%
**{score.value_density_score:.1f}/100** {quality_emoji[self._score_to_quality(score.value_density_score)]}

檢測實質內容比例，避免空話

### 4. Actionability (可操作性) - 權重 15%
**{score.actionability_score:.1f}/100** {quality_emoji[self._score_to_quality(score.actionability_score)]}

檢測是否提供可執行的建議和步驟

---

## ✅ 正面信號 ({len(score.green_signals)} 個)

"""

        if score.green_signals:
            for signal in score.green_signals:
                report += f"{signal}\n"
        else:
            report += "*未檢測到顯著的正面信號*\n"

        report += "\n---\n\n## 🚩 需要改進的問題 ({} 個)\n\n".format(len(score.red_flags))

        if score.red_flags:
            for flag in score.red_flags:
                report += f"{flag}\n"
        else:
            report += "✅ *無明顯問題*\n"

        report += "\n---\n\n## 💡 改進建議\n\n"

        # 根據狀態提供建議
        if score.quality_status == 'excellent':
            report += "🎉 **內容品質優秀！** 完全符合 Google Helpful Content 標準。\n\n"
            report += "✅ 這是真正為用戶創作的有價值內容。\n\n"
            report += "**保持優勢**：\n"
            report += "- 繼續提供第一手經驗和實用建議\n"
            report += "- 保持內容的深度和可操作性\n"
            report += "- 定期更新以保持時效性\n\n"

        elif score.quality_status == 'good':
            report += "👍 **內容品質良好**，接近優秀標準：\n\n"
            report += "**快速提升建議**：\n"

            if score.people_first_score < 80:
                report += "- 減少 SEO 導向的詞彙，使用更自然的用戶語言\n"

            if score.authenticity_score < 80:
                report += "- 加入更多個人經驗和真實案例\n"

            if score.value_density_score < 80:
                report += "- 增加實質內容（數據、案例、步驟）\n"

            if score.actionability_score < 80:
                report += "- 提供更具體的行動步驟和工具\n"

            report += "\n"

        elif score.quality_status == 'acceptable':
            report += "⚠️ **內容可接受，但有明顯改進空間**：\n\n"
            report += "**優先改進項目**：\n\n"

            # 找出分數最低的維度
            dims = [
                ('People-First', score.people_first_score),
                ('Authenticity', score.authenticity_score),
                ('Value Density', score.value_density_score),
                ('Actionability', score.actionability_score)
            ]
            dims.sort(key=lambda x: x[1])

            lowest_dim = dims[0]
            report += f"1. **{lowest_dim[0]} ({lowest_dim[1]:.1f}分)** - 最需要改進\n"

            if lowest_dim[0] == 'People-First':
                report += "   - 檢查是否過度 SEO 優化\n"
                report += "   - 使用更自然的語言\n"
                report += "   - 避免關鍵字堆砌\n"

            elif lowest_dim[0] == 'Authenticity':
                report += "   - 加入第一手使用經驗\n"
                report += "   - 分享個人觀點和發現\n"
                report += "   - 提供平衡的優缺點評價\n"

            elif lowest_dim[0] == 'Value Density':
                report += "   - 減少空話和陳詞濫調\n"
                report += "   - 加入具體數據和案例\n"
                report += "   - 增加內容深度\n"

            elif lowest_dim[0] == 'Actionability':
                report += "   - 提供清晰的步驟說明\n"
                report += "   - 加入實用工具和資源\n"
                report += "   - 使用行動導向語言\n"

            report += "\n"

            if dims[1][1] < 65:
                report += f"2. **{dims[1][0]} ({dims[1][1]:.1f}分)** - 次要改進\n"

            report += "\n"

        else:  # poor
            report += "🔴 **內容品質不佳，強烈建議重寫**：\n\n"
            report += "**嚴重問題**：\n\n"

            if score.people_first_score < 50:
                report += "- 🔴 過度 SEO 優化，需要改為用戶導向寫作\n"

            if score.authenticity_score < 50:
                report += "- 🔴 缺乏第一手經驗，內容不夠真實\n"

            if score.value_density_score < 50:
                report += "- 🔴 實質內容不足，空話過多\n"

            if score.actionability_score < 50:
                report += "- 🔴 缺乏可操作的建議，對讀者幫助有限\n"

            report += "\n**重寫指引**：\n\n"
            report += "1. **確立用戶價值**：這篇文章能幫讀者解決什麼問題？\n"
            report += "2. **加入真實經驗**：分享你的親身使用經驗和發現\n"
            report += "3. **提供實用建議**：給出具體的步驟和可執行的方法\n"
            report += "4. **減少 SEO 痕跡**：用自然語言寫作，不要刻意堆砌關鍵字\n"
            report += "5. **增加深度和細節**：提供數據、案例、對比\n\n"

        report += "---\n\n## 📚 Google Helpful Content System 核心原則\n\n"

        report += """### ✅ People-First Content Checklist

**內容創作前問自己**：

1. ❓ 你的內容是否展示了第一手經驗和深入知識？
2. ❓ 你的網站是否有明確的主題或專業領域？
3. ❓ 讀者看完後，是否會覺得學到了東西？
4. ❓ 讀者是否會將你的網站加入書籤或推薦給朋友？

**避免的做法**：

1. ❌ 主要為了搜尋引擎排名而創作內容
2. ❌ 大量產生多主題內容，希望其中一些能排名
3. ❌ 使用 AI 大量生成內容，但未經人工審查和編輯
4. ❌ 總結其他人的內容，沒有加入實質價值
5. ❌ 只是為了湊字數而寫長文

### 🎯 2025 年 Helpful Content System 要點

- **與核心更新整合**：現在是單一系統，影響更大
- **減少 45% 低品質內容**：Google 的明確目標
- **AI 內容可以，但需要審查**：不是反對 AI，而是反對低品質
- **真實經驗比理論更重要**：E-E-A-T 的 Experience 維度

"""

        report += f"\n---\n\n*報告生成時間: {self._get_timestamp()}*\n"

        # 如果指定輸出路徑，寫入檔案
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Helpful Content 報告已生成: {output_path}")

        return report

    def _score_to_quality(self, score: float) -> str:
        """分數轉品質等級"""
        if score >= 80:
            return 'excellent'
        elif score >= 65:
            return 'good'
        elif score >= 50:
            return 'acceptable'
        else:
            return 'poor'

    def _get_timestamp(self) -> str:
        """取得當前時間戳記"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    """命令行介面"""
    parser = argparse.ArgumentParser(
        description='分析文章是否符合 Google Helpful Content 標準'
    )
    parser.add_argument(
        'article',
        help='待分析的文章檔案路徑'
    )
    parser.add_argument(
        '-e', '--experience',
        help='經驗檔案路徑（experience_profile.md）'
    )
    parser.add_argument(
        '-o', '--output',
        help='輸出報告路徑（可選）'
    )

    args = parser.parse_args()

    # 創建分析器
    analyzer = HelpfulContentAnalyzer()

    # 執行分析
    print(f"🔍 分析文章: {args.article}")

    if args.experience:
        print(f"📝 參考經驗檔案: {args.experience}")

    score = analyzer.analyze(args.article, args.experience)

    # 生成報告
    report = analyzer.generate_markdown_report(score, args.output)

    # 如果沒有指定輸出路徑，列印到終端
    if not args.output:
        print("\n" + report)

    # 顯示摘要
    quality_emoji = {'excellent': '🟢', 'good': '🟡', 'acceptable': '🟠', 'poor': '🔴'}

    print(f"\n{quality_emoji[score.quality_status]} 有價值度: {score.overall_score}/100 ({score.quality_status.upper()})")
    print(f"📊 維度分數:")
    print(f"  - People-First: {score.people_first_score:.1f}/100")
    print(f"  - Authenticity: {score.authenticity_score:.1f}/100")
    print(f"  - Value Density: {score.value_density_score:.1f}/100")
    print(f"  - Actionability: {score.actionability_score:.1f}/100")


if __name__ == '__main__':
    main()
