#!/usr/bin/env python3
"""
AI Detection Skill - AI 內容偵測工具
分析文章的 AI 生成特徵並提供人類化改進建議

使用方式:
    python3 detect.py input_article.md --output ai_detection_report.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter
import statistics


# AI 特徵模式
AI_PATTERNS = {
    "sequential_markers": [
        (r"^首先[，,]", "序號開頭: 首先"),
        (r"^其次[，,]", "序號開頭: 其次"),
        (r"^最後[，,]", "序號開頭: 最後"),
        (r"^第[一二三四五六七八九十]", "數字序號開頭"),
        (r"^接下來[，,]", "過渡詞開頭: 接下來"),
        (r"^此外[，,]", "過渡詞開頭: 此外"),
    ],
    "formal_patterns": [
        (r"本文將", "過度正式: 本文將"),
        (r"綜上所述", "過度正式: 綜上所述"),
        (r"值得注意的是", "過度正式: 值得注意的是"),
        (r"不言而喻", "過度正式: 不言而喻"),
        (r"顯而易見", "過度正式: 顯而易見"),
    ],
    "overused_transitions": [
        (r"因此[，,]", "過度使用: 因此"),
        (r"然而[，,]", "過度使用: 然而"),
        (r"總之[，,]", "過度使用: 總之"),
        (r"換句話說", "過度使用: 換句話說"),
    ],
    "lack_personality": [
        (r"這(?:個|種|些)(?:方法|工具|技術)", "缺乏個性: 泛泛而談"),
        (r"可以幫助(?:你|我們|用戶)", "缺乏個性: 標準句式"),
    ],
}

# 情感詞彙
EMOTION_WORDS = [
    "驚訝", "開心", "興奮", "沮喪", "困惑", "好奇", "期待", "失望",
    "感動", "生氣", "害怕", "放心", "滿意", "後悔", "尷尬", "緊張",
    "輕鬆", "煩惱", "無奈", "欣慰", "佩服", "羨慕", "嫉妒", "同情",
    "愛", "恨", "喜歡", "討厭", "擔心", "安心", "焦慮", "平靜",
    # 口語化情感表達
    "天啊", "哇", "太棒了", "糟糕", "可惡", "真的假的", "沒想到",
    "老實說", "說實話", "坦白講", "不騙你", "真心覺得",
]

# 人類化特徵詞彙
HUMAN_MARKERS = [
    r"我(?:認為|覺得|想|相信|發現|試過|用過)",
    r"說(?:實話|真的|老實)",
    r"(?:其實|事實上|坦白說)",
    r"(?:你|妳)(?:可能|應該|會不會)",
    r"(?:有沒有|是不是|對不對)",
    r"(?:吧|啦|呢|嘛|喔|耶)$",
    r"\.{3}",  # 省略號
    r"[!?！？]{2,}",  # 連續標點
    r"—{1,2}",  # 破折號
]


class AIDetector:
    """AI 內容偵測器"""

    def __init__(self, text: str):
        self.text = text
        self.paragraphs = self._split_paragraphs()
        self.sentences = self._split_sentences()

    def _split_paragraphs(self) -> List[str]:
        """分割段落"""
        return [p.strip() for p in self.text.split('\n\n') if p.strip()]

    def _split_sentences(self) -> List[str]:
        """分割句子"""
        sentences = []
        for para in self.paragraphs:
            # 使用中文標點分割
            sents = re.split(r'[。！？]', para)
            sentences.extend([s.strip() for s in sents if s.strip()])
        return sentences

    def analyze(self) -> Dict:
        """執行完整分析"""
        return {
            "repetition_rate": self._calculate_repetition_rate(),
            "paragraph_variance": self._calculate_paragraph_variance(),
            "emotion_density": self._calculate_emotion_density(),
            "perplexity_estimate": self._estimate_perplexity(),
            "burstiness": self._calculate_burstiness(),
            "ai_patterns_found": self._find_ai_patterns(),
            "human_markers_found": self._find_human_markers(),
        }

    def _calculate_repetition_rate(self) -> Tuple[float, List[str]]:
        """計算句式重複率"""
        if not self.sentences:
            return 0.0, []

        # 提取句子開頭（前10個字）
        sentence_starts = []
        for sent in self.sentences:
            if len(sent) >= 5:
                sentence_starts.append(sent[:10])

        if not sentence_starts:
            return 0.0, []

        # 計算重複
        counter = Counter(sentence_starts)
        repeated = [start for start, count in counter.items() if count > 1]
        repetition_count = sum(count - 1 for count in counter.values() if count > 1)

        rate = repetition_count / len(sentence_starts)
        return rate, repeated

    def _calculate_paragraph_variance(self) -> float:
        """計算段落長度變異度"""
        if len(self.paragraphs) < 2:
            return 0.0

        # 計算每段的中文字數
        lengths = []
        for para in self.paragraphs:
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', para))
            lengths.append(chinese_chars)

        if len(lengths) < 2:
            return 0.0

        return statistics.stdev(lengths)

    def _calculate_emotion_density(self) -> float:
        """計算情感詞彙密度"""
        # 計算總字數
        total_chars = len(re.findall(r'[\u4e00-\u9fff]', self.text))
        if total_chars == 0:
            return 0.0

        # 計算情感詞出現次數
        emotion_count = 0
        for word in EMOTION_WORDS:
            emotion_count += len(re.findall(word, self.text))

        # 假設平均每個情感詞 2 個字
        return (emotion_count * 2) / total_chars

    def _estimate_perplexity(self) -> str:
        """估算困惑度（簡化版）"""
        # 檢查是否有意外的用詞
        unusual_patterns = [
            r'(?:其實|事實上).*?(?:但是|不過)',  # 轉折
            r'說(?:實話|真的)',  # 口語
            r'\.{3}',  # 省略號
        ]

        unusual_count = sum(
            len(re.findall(pattern, self.text))
            for pattern in unusual_patterns
        )

        # 基於意外用詞判斷
        if unusual_count > 5:
            return "high"  # 高困惑度 = 像人類
        elif unusual_count > 2:
            return "medium"
        else:
            return "low"  # 低困惑度 = 像 AI

    def _calculate_burstiness(self) -> str:
        """計算爆發度（句子長度變化）"""
        if len(self.sentences) < 3:
            return "low"

        # 計算句子長度
        lengths = [len(s) for s in self.sentences]

        # 計算變異係數
        mean_len = statistics.mean(lengths)
        if mean_len == 0:
            return "low"

        std_len = statistics.stdev(lengths)
        cv = std_len / mean_len

        # 判斷爆發度
        if cv > 0.6:
            return "high"  # 高爆發度 = 像人類
        elif cv > 0.4:
            return "medium"
        else:
            return "low"  # 低爆發度 = 像 AI

    def _find_ai_patterns(self) -> List[Dict]:
        """找出 AI 特徵模式"""
        found = []

        for category, patterns in AI_PATTERNS.items():
            for pattern, description in patterns:
                matches = re.findall(pattern, self.text, re.MULTILINE)
                if matches:
                    found.append({
                        "category": category,
                        "description": description,
                        "count": len(matches),
                        "examples": matches[:3]  # 只取前3個範例
                    })

        return found

    def _find_human_markers(self) -> List[Dict]:
        """找出人類化特徵"""
        found = []

        for pattern in HUMAN_MARKERS:
            matches = re.findall(pattern, self.text)
            if matches:
                found.append({
                    "pattern": pattern,
                    "count": len(matches),
                    "examples": matches[:3]
                })

        return found


class AIScoreCalculator:
    """AI 分數計算器"""

    @staticmethod
    def calculate(analysis: Dict) -> Tuple[int, str]:
        """
        計算 AI 偵測分數

        分數越低越像人類 (0-100)
        """
        score = 50  # 基礎分數

        # 句式重複率 (影響 ±20)
        repetition_rate = analysis["repetition_rate"][0]
        if repetition_rate < 0.1:
            score -= 10
        elif repetition_rate > 0.3:
            score += 20
        elif repetition_rate > 0.2:
            score += 10

        # 段落變異度 (影響 ±15)
        variance = analysis["paragraph_variance"]
        if variance > 40:
            score -= 15
        elif variance < 20:
            score += 15
        elif variance < 30:
            score += 5

        # 情感詞密度 (影響 ±15)
        emotion = analysis["emotion_density"]
        if emotion > 0.03:
            score -= 15
        elif emotion < 0.01:
            score += 15
        elif emotion < 0.02:
            score += 5

        # 困惑度 (影響 ±10)
        perplexity = analysis["perplexity_estimate"]
        if perplexity == "high":
            score -= 10
        elif perplexity == "low":
            score += 10

        # 爆發度 (影響 ±10)
        burstiness = analysis["burstiness"]
        if burstiness == "high":
            score -= 10
        elif burstiness == "low":
            score += 10

        # AI 特徵模式 (每個 +5，最多 +20)
        ai_patterns = len(analysis["ai_patterns_found"])
        score += min(ai_patterns * 5, 20)

        # 人類化特徵 (每個 -5，最多 -20)
        human_markers = len(analysis["human_markers_found"])
        score -= min(human_markers * 5, 20)

        # 確保分數在 0-100 範圍
        score = max(0, min(100, score))

        # 評級
        if score <= 20:
            grade = "A"
        elif score <= 40:
            grade = "B"
        elif score <= 60:
            grade = "C"
        elif score <= 80:
            grade = "D"
        else:
            grade = "F"

        return score, grade


class ReportGenerator:
    """報告生成器"""

    def __init__(self, analysis: Dict, score: int, grade: str):
        self.analysis = analysis
        self.score = score
        self.grade = grade

    def generate_markdown(self, verbose: bool = False) -> str:
        """生成 Markdown 報告"""
        report = f"""# AI 偵測報告

**生成時間**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 整體評估

| 指標 | 數值 |
|------|------|
| **AI 偵測分數** | {self.score}/100 (越低越像人類) |
| **評級** | {self.grade} |
| **結論** | {self._get_conclusion()} |

## 各維度分析

| 維度 | 數值 | 狀態 | 說明 |
|------|------|------|------|
| 句式重複率 | {self.analysis['repetition_rate'][0]:.1%} | {self._get_status('repetition', self.analysis['repetition_rate'][0])} | <10% 為佳 |
| 段落變異度 | {self.analysis['paragraph_variance']:.1f} | {self._get_status('variance', self.analysis['paragraph_variance'])} | >40 為佳 |
| 情感詞密度 | {self.analysis['emotion_density']:.1%} | {self._get_status('emotion', self.analysis['emotion_density'])} | >3% 為佳 |
| 困惑度 | {self.analysis['perplexity_estimate']} | {self._perplexity_status()} | high 為佳 |
| 爆發度 | {self.analysis['burstiness']} | {self._burstiness_status()} | high 為佳 |

"""

        # AI 特徵
        ai_patterns = self.analysis['ai_patterns_found']
        if ai_patterns:
            report += "## 發現的 AI 特徵\n\n"
            for pattern in ai_patterns:
                report += f"- **{pattern['description']}** (出現 {pattern['count']} 次)\n"
                if verbose and pattern.get('examples'):
                    report += f"  - 範例: {', '.join(str(e) for e in pattern['examples'][:2])}\n"
            report += "\n"
        else:
            report += "## 發現的 AI 特徵\n\n無明顯 AI 特徵。\n\n"

        # 人類化特徵
        human_markers = self.analysis['human_markers_found']
        if human_markers:
            report += "## 發現的人類化特徵\n\n"
            for marker in human_markers:
                report += f"- 模式匹配 (出現 {marker['count']} 次)\n"
            report += "\n"

        # 建議
        report += self._generate_suggestions()

        return report

    def generate_json(self) -> str:
        """生成 JSON 報告"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "ai_score": self.score,
            "grade": self.grade,
            "conclusion": self._get_conclusion(),
            "dimensions": {
                "repetition_rate": self.analysis['repetition_rate'][0],
                "paragraph_variance": self.analysis['paragraph_variance'],
                "emotion_density": self.analysis['emotion_density'],
                "perplexity": self.analysis['perplexity_estimate'],
                "burstiness": self.analysis['burstiness'],
            },
            "ai_patterns_found": self.analysis['ai_patterns_found'],
            "human_markers_found": len(self.analysis['human_markers_found']),
            "suggestions": self._get_suggestions_list(),
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _get_conclusion(self) -> str:
        """獲取結論"""
        if self.score <= 20:
            return "非常像人類寫的，無需修改"
        elif self.score <= 40:
            return "偏向人類風格，可選擇性優化"
        elif self.score <= 60:
            return "難以判斷，建議進行人類化處理"
        elif self.score <= 80:
            return "偏向 AI 風格，需要修改"
        else:
            return "明顯的 AI 特徵，必須大幅修改"

    def _get_status(self, metric: str, value: float) -> str:
        """獲取狀態標記"""
        if metric == 'repetition':
            if value < 0.1:
                return "優秀"
            elif value < 0.2:
                return "良好"
            elif value < 0.3:
                return "需改進"
            else:
                return "AI 特徵"
        elif metric == 'variance':
            if value > 40:
                return "優秀"
            elif value > 30:
                return "良好"
            elif value > 20:
                return "需改進"
            else:
                return "AI 特徵"
        elif metric == 'emotion':
            if value > 0.03:
                return "優秀"
            elif value > 0.02:
                return "良好"
            elif value > 0.01:
                return "需改進"
            else:
                return "AI 特徵"
        return "未知"

    def _perplexity_status(self) -> str:
        """困惑度狀態"""
        p = self.analysis['perplexity_estimate']
        if p == "high":
            return "優秀"
        elif p == "medium":
            return "可接受"
        else:
            return "AI 特徵"

    def _burstiness_status(self) -> str:
        """爆發度狀態"""
        b = self.analysis['burstiness']
        if b == "high":
            return "優秀"
        elif b == "medium":
            return "可接受"
        else:
            return "AI 特徵"

    def _generate_suggestions(self) -> str:
        """生成改進建議"""
        suggestions = self._get_suggestions_list()

        if not suggestions:
            return "## 人類化建議\n\n文章已具備良好的人類化特徵，無需特別修改。\n"

        report = "## 人類化建議\n\n"

        # 高優先級建議
        high_priority = [s for s in suggestions if s.get('priority') == 'high']
        if high_priority:
            report += "### 高優先級 (建議修改)\n\n"
            for s in high_priority:
                report += f"- {s['suggestion']}\n"
            report += "\n"

        # 中優先級建議
        medium_priority = [s for s in suggestions if s.get('priority') == 'medium']
        if medium_priority:
            report += "### 中優先級 (可選優化)\n\n"
            for s in medium_priority:
                report += f"- {s['suggestion']}\n"
            report += "\n"

        return report

    def _get_suggestions_list(self) -> List[Dict]:
        """獲取建議列表"""
        suggestions = []

        # 基於句式重複率
        if self.analysis['repetition_rate'][0] > 0.2:
            suggestions.append({
                "priority": "high",
                "dimension": "repetition",
                "suggestion": "減少重複的句子開頭，嘗試使用不同的表達方式"
            })

        # 基於段落變異度
        if self.analysis['paragraph_variance'] < 30:
            suggestions.append({
                "priority": "high",
                "dimension": "variance",
                "suggestion": "調整段落長度，製造長短交替的「呼吸感」"
            })

        # 基於情感詞密度
        if self.analysis['emotion_density'] < 0.02:
            suggestions.append({
                "priority": "high",
                "dimension": "emotion",
                "suggestion": "增加情感表達，如個人反應、感受描述"
            })

        # 基於困惑度
        if self.analysis['perplexity_estimate'] == "low":
            suggestions.append({
                "priority": "medium",
                "dimension": "perplexity",
                "suggestion": "加入一些意外的用詞或轉折，避免文字過於「順暢」"
            })

        # 基於爆發度
        if self.analysis['burstiness'] == "low":
            suggestions.append({
                "priority": "medium",
                "dimension": "burstiness",
                "suggestion": "混合使用長短句，重點用短句強調"
            })

        # 基於 AI 特徵
        ai_patterns = self.analysis['ai_patterns_found']
        if ai_patterns:
            for pattern in ai_patterns[:3]:  # 最多3個建議
                if 'sequential' in pattern['category']:
                    suggestions.append({
                        "priority": "high",
                        "dimension": "ai_pattern",
                        "suggestion": f"避免使用 \"{pattern['description'].split(': ')[1]}\" 這類序號標記"
                    })
                elif 'formal' in pattern['category']:
                    suggestions.append({
                        "priority": "medium",
                        "dimension": "ai_pattern",
                        "suggestion": f"將 \"{pattern['description'].split(': ')[1]}\" 改為更口語化的表達"
                    })

        return suggestions


def main():
    parser = argparse.ArgumentParser(description='AI 內容偵測工具')
    parser.add_argument('input', help='待分析的文章路徑')
    parser.add_argument('--output', '-o', default='ai_detection_report.md', help='輸出報告路徑')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'], default='markdown', help='輸出格式')
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細模式')
    parser.add_argument('--threshold', type=int, default=40, help='AI 偵測閾值')

    args = parser.parse_args()

    # 讀取輸入文章
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"錯誤: 找不到檔案 {args.input}")
        sys.exit(1)

    text = input_path.read_text(encoding='utf-8')

    # 執行分析
    detector = AIDetector(text)
    analysis = detector.analyze()

    # 計算分數
    score, grade = AIScoreCalculator.calculate(analysis)

    # 生成報告
    generator = ReportGenerator(analysis, score, grade)

    if args.format == 'json':
        report = generator.generate_json()
        output_path = args.output if args.output.endswith('.json') else args.output + '.json'
    else:
        report = generator.generate_markdown(verbose=args.verbose)
        output_path = args.output

    # 寫入報告
    Path(output_path).write_text(report, encoding='utf-8')

    # 輸出摘要
    print(f"AI 偵測分數: {score}/100 (評級: {grade})")
    print(f"報告已生成: {output_path}")

    # 檢查是否通過閾值
    if score <= args.threshold:
        print(f"✅ 通過閾值 ({args.threshold})")
        sys.exit(0)
    else:
        print(f"⚠️ 超過閾值 ({args.threshold})，建議進行人類化處理")
        sys.exit(1)


if __name__ == "__main__":
    main()
