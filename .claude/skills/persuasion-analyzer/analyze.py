#!/usr/bin/env python3
"""
Persuasion Analyzer Skill - 說服力分析工具
分析文章的說服力結構，評估 AIDA、PAS、4Cs 等框架的應用程度

使用方式:
    python3 analyze.py input_article.md --output persuasion_report.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


# AIDA 框架模式
AIDA_PATTERNS = {
    "attention": [
        (r"^.{0,100}[?？]", "問句開頭"),
        (r"\d+%", "數據衝擊"),
        (r"(?:震驚|驚人|沒想到|不可思議)", "震撼性詞彙"),
        (r"(?:你知道嗎|想像一下|如果告訴你)", "引導開頭"),
    ],
    "interest": [
        (r"(?:好處|優勢|特點|能夠|可以幫助)", "好處展示"),
        (r"(?:接下來|讓我|今天要分享)", "內容預告"),
        (r"(?:為什麼|如何|怎麼)", "好奇引導"),
    ],
    "desire": [
        (r"(?:\d+\s*(?:人|位|個).*?(?:使用|驗證|選擇))", "社會證明"),
        (r"(?:節省|提升|增加|減少).*?\d+", "成果數據"),
        (r"(?:案例|實例|經驗|故事)", "案例展示"),
        (r"(?:從.*?變成|以前.*?現在)", "對比效果"),
    ],
    "action": [
        (r"(?:立即|馬上|現在就)", "行動詞彙"),
        (r"(?:下載|訂閱|點擊|開始)", "CTA 動詞"),
        (r"(?:免費|限時|獨家)", "緊迫感"),
        (r"(?:只需|簡單|輕鬆|快速)", "門檻降低"),
    ],
}

# PAS 框架模式
PAS_PATTERNS = {
    "problem": [
        (r"(?:困擾|問題|挑戰|難題|痛點)", "問題詞彙"),
        (r"(?:你是否|有沒有|是不是)", "問題提問"),
        (r"(?:花.*?時間|浪費|效率低)", "痛點描述"),
    ],
    "agitate": [
        (r"(?:如果繼續|越來越|更嚴重)", "問題惡化"),
        (r"(?:後果|代價|損失)", "後果展示"),
        (r"(?:焦慮|擔心|害怕|恐懼)", "情感激化"),
    ],
    "solution": [
        (r"(?:解決方案|方法|答案|秘訣)", "解決詞彙"),
        (r"(?:終於|直到|發現了)", "轉折詞彙"),
        (r"(?:步驟|流程|系統|框架)", "方案描述"),
    ],
}

# 4Cs 框架模式
FOUR_CS_PATTERNS = {
    "clear": [
        (r"(?:簡單來說|換句話說|也就是)", "簡化表達"),
        (r"(?:第[一二三四五]|步驟\s*\d)", "結構化"),
    ],
    "concise": [
        # 反向檢測：冗餘詞彙
        (r"(?:基本上|總的來說|在某種程度上)", "冗餘詞彙（負面）"),
    ],
    "compelling": [
        (r"(?:驚人|精彩|絕妙|厲害)", "吸引詞彙"),
        (r"(?:故事|經歷|旅程)", "故事元素"),
    ],
    "credible": [
        (r"(?:根據|研究|數據|調查)", "來源引用"),
        (r"(?:實測|驗證|證明)", "證據展示"),
    ],
}

# 心理觸發模式
PSYCHOLOGICAL_TRIGGERS = {
    "scarcity": [
        (r"(?:限時|獨家|僅剩|最後)", "稀缺性"),
    ],
    "social_proof": [
        (r"(?:\d+\s*(?:人|位|個))", "數量證明"),
        (r"(?:大家都|很多人|熱門)", "群眾認同"),
    ],
    "authority": [
        (r"(?:專家|專業|權威|經驗)", "權威性"),
        (r"(?:\d+\s*年)", "經驗年數"),
    ],
    "reciprocity": [
        (r"(?:免費|送給你|分享)", "互惠"),
    ],
    "consistency": [
        (r"(?:如果你同意|你可能也)", "一致性引導"),
    ],
    "liking": [
        (r"(?:我也|跟你一樣|我們都)", "相似性"),
    ],
}


class PersuasionAnalyzer:
    """說服力分析器"""

    def __init__(self, text: str):
        self.text = text
        self.paragraphs = self._split_paragraphs()

    def _split_paragraphs(self) -> List[str]:
        """分割段落"""
        return [p.strip() for p in self.text.split("\n\n") if p.strip()]

    def analyze_aida(self) -> Dict:
        """分析 AIDA 框架"""
        results = {}

        for stage, patterns in AIDA_PATTERNS.items():
            matches = []
            for pattern, description in patterns:
                found = re.findall(pattern, self.text)
                if found:
                    matches.append({"pattern": description, "count": len(found)})

            # 計算分數
            score = min(100, len(matches) * 25 + sum(m["count"] for m in matches) * 5)
            results[stage] = {"score": score, "matches": matches}

        return results

    def analyze_pas(self) -> Dict:
        """分析 PAS 框架"""
        results = {}

        for stage, patterns in PAS_PATTERNS.items():
            matches = []
            for pattern, description in patterns:
                found = re.findall(pattern, self.text)
                if found:
                    matches.append({"pattern": description, "count": len(found)})

            score = min(100, len(matches) * 30 + sum(m["count"] for m in matches) * 5)
            results[stage] = {"score": score, "matches": matches}

        return results

    def analyze_4cs(self) -> Dict:
        """分析 4Cs 框架"""
        results = {}

        for element, patterns in FOUR_CS_PATTERNS.items():
            matches = []
            negative_count = 0

            for pattern, description in patterns:
                found = re.findall(pattern, self.text)
                if found:
                    if "負面" in description:
                        negative_count += len(found)
                    else:
                        matches.append({"pattern": description, "count": len(found)})

            # 計算分數（冗餘詞彙扣分）
            base_score = len(matches) * 25 + sum(m.get("count", 0) for m in matches) * 5
            score = max(0, min(100, base_score - negative_count * 10))

            # 特殊處理：concise 需要評估文字簡潔度
            if element == "concise":
                avg_sentence_length = self._avg_sentence_length()
                if avg_sentence_length < 25:
                    score = min(100, score + 30)
                elif avg_sentence_length > 40:
                    score = max(0, score - 20)

            results[element] = {"score": score, "matches": matches}

        return results

    def analyze_psychological_triggers(self) -> Dict:
        """分析心理觸發"""
        results = {}

        for trigger, patterns in PSYCHOLOGICAL_TRIGGERS.items():
            matches = []
            for pattern, description in patterns:
                found = re.findall(pattern, self.text)
                if found:
                    matches.append({"pattern": description, "count": len(found)})

            results[trigger] = {
                "used": len(matches) > 0,
                "count": sum(m["count"] for m in matches),
                "matches": matches,
            }

        return results

    def _avg_sentence_length(self) -> float:
        """計算平均句子長度"""
        sentences = re.split(r"[。！？]", self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0
        total_chars = sum(len(s) for s in sentences)
        return total_chars / len(sentences)

    def calculate_overall_score(
        self, aida: Dict, pas: Dict, four_cs: Dict, triggers: Dict
    ) -> Tuple[int, str]:
        """計算總體分數"""
        # AIDA 權重分數
        aida_score = (
            aida["attention"]["score"] * 0.20
            + aida["interest"]["score"] * 0.25
            + aida["desire"]["score"] * 0.30
            + aida["action"]["score"] * 0.25
        )

        # PAS 權重分數
        pas_score = (
            pas["problem"]["score"] * 0.35
            + pas["agitate"]["score"] * 0.30
            + pas["solution"]["score"] * 0.35
        )

        # 4Cs 權重分數
        four_cs_score = sum(v["score"] for v in four_cs.values()) / 4

        # 心理觸發加分
        trigger_bonus = sum(5 for t in triggers.values() if t["used"])

        # 綜合分數（取 AIDA 和 PAS 的較高者）
        framework_score = max(aida_score, pas_score)
        total_score = int(framework_score * 0.5 + four_cs_score * 0.3 + trigger_bonus)
        total_score = min(100, total_score)

        # 評級
        if total_score >= 90:
            grade = "A+"
        elif total_score >= 80:
            grade = "A"
        elif total_score >= 70:
            grade = "B"
        elif total_score >= 60:
            grade = "C"
        else:
            grade = "D"

        return total_score, grade


class ReportGenerator:
    """報告生成器"""

    def __init__(
        self, aida: Dict, pas: Dict, four_cs: Dict, triggers: Dict, score: int, grade: str
    ):
        self.aida = aida
        self.pas = pas
        self.four_cs = four_cs
        self.triggers = triggers
        self.score = score
        self.grade = grade

    def generate_markdown(self) -> str:
        """生成 Markdown 報告"""
        report = f"""# 說服力分析報告

**生成時間**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 總體評估

| 指標 | 數值 |
|------|------|
| **說服力分數** | {self.score}/100 |
| **評級** | {self.grade} |

## AIDA 框架分析

| 階段 | 分數 | 狀態 |
|------|------|------|
| Attention (注意) | {self.aida['attention']['score']}/100 | {self._get_status(self.aida['attention']['score'])} |
| Interest (興趣) | {self.aida['interest']['score']}/100 | {self._get_status(self.aida['interest']['score'])} |
| Desire (慾望) | {self.aida['desire']['score']}/100 | {self._get_status(self.aida['desire']['score'])} |
| Action (行動) | {self.aida['action']['score']}/100 | {self._get_status(self.aida['action']['score'])} |

## PAS 框架分析

| 階段 | 分數 | 狀態 |
|------|------|------|
| Problem (問題) | {self.pas['problem']['score']}/100 | {self._get_status(self.pas['problem']['score'])} |
| Agitate (激化) | {self.pas['agitate']['score']}/100 | {self._get_status(self.pas['agitate']['score'])} |
| Solution (解決) | {self.pas['solution']['score']}/100 | {self._get_status(self.pas['solution']['score'])} |

## 4Cs 框架分析

| 元素 | 分數 | 狀態 |
|------|------|------|
| Clear (清晰) | {self.four_cs['clear']['score']}/100 | {self._get_status(self.four_cs['clear']['score'])} |
| Concise (簡潔) | {self.four_cs['concise']['score']}/100 | {self._get_status(self.four_cs['concise']['score'])} |
| Compelling (引人) | {self.four_cs['compelling']['score']}/100 | {self._get_status(self.four_cs['compelling']['score'])} |
| Credible (可信) | {self.four_cs['credible']['score']}/100 | {self._get_status(self.four_cs['credible']['score'])} |

## 心理觸發檢測

| 觸發 | 狀態 | 次數 |
|------|------|------|
| 稀缺性 (Scarcity) | {"✅" if self.triggers['scarcity']['used'] else "❌"} | {self.triggers['scarcity']['count']} |
| 社會證明 (Social Proof) | {"✅" if self.triggers['social_proof']['used'] else "❌"} | {self.triggers['social_proof']['count']} |
| 權威性 (Authority) | {"✅" if self.triggers['authority']['used'] else "❌"} | {self.triggers['authority']['count']} |
| 互惠 (Reciprocity) | {"✅" if self.triggers['reciprocity']['used'] else "❌"} | {self.triggers['reciprocity']['count']} |
| 一致性 (Consistency) | {"✅" if self.triggers['consistency']['used'] else "❌"} | {self.triggers['consistency']['count']} |
| 喜好 (Liking) | {"✅" if self.triggers['liking']['used'] else "❌"} | {self.triggers['liking']['count']} |

## 優化建議

"""
        # 生成優化建議
        suggestions = self._generate_suggestions()
        for priority, items in suggestions.items():
            if items:
                report += f"### {priority}\n\n"
                for item in items:
                    report += f"- {item}\n"
                report += "\n"

        return report

    def generate_json(self) -> str:
        """生成 JSON 報告"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "overall_score": self.score,
            "grade": self.grade,
            "aida": self.aida,
            "pas": self.pas,
            "four_cs": self.four_cs,
            "psychological_triggers": self.triggers,
            "suggestions": self._generate_suggestions(),
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _get_status(self, score: int) -> str:
        """獲取狀態標記"""
        if score >= 80:
            return "優秀"
        elif score >= 60:
            return "良好"
        elif score >= 40:
            return "需改進"
        else:
            return "不足"

    def _generate_suggestions(self) -> Dict[str, List[str]]:
        """生成優化建議"""
        suggestions = {"高優先級": [], "中優先級": [], "可選優化": []}

        # AIDA 建議
        if self.aida["attention"]["score"] < 60:
            suggestions["高優先級"].append("開頭需要更有衝擊力，考慮使用數據、問題或反直覺陳述")
        if self.aida["action"]["score"] < 60:
            suggestions["高優先級"].append("CTA 不夠明確，需要加強行動呼籲")

        if self.aida["desire"]["score"] < 70:
            suggestions["中優先級"].append("增加社會證明和成果展示，強化讀者慾望")
        if self.aida["interest"]["score"] < 70:
            suggestions["中優先級"].append("加強好處展示和好奇心製造")

        # 心理觸發建議
        unused_triggers = [t for t, v in self.triggers.items() if not v["used"]]
        if "social_proof" in unused_triggers:
            suggestions["中優先級"].append("考慮加入社會證明（使用者數據、案例等）")
        if "scarcity" in unused_triggers:
            suggestions["可選優化"].append("可考慮加入適當的稀缺性元素")

        # 4Cs 建議
        if self.four_cs["credible"]["score"] < 60:
            suggestions["高優先級"].append("加強可信度，補充數據來源和證據")

        return suggestions


def main():
    parser = argparse.ArgumentParser(description="說服力分析工具")
    parser.add_argument("input", help="待分析的文章路徑")
    parser.add_argument("--output", "-o", default="persuasion_report.md", help="輸出報告路徑")
    parser.add_argument(
        "--framework", "-f", choices=["AIDA", "PAS", "4Cs", "all"], default="all", help="分析框架"
    )
    parser.add_argument(
        "--format", choices=["markdown", "json"], default="markdown", help="輸出格式"
    )

    args = parser.parse_args()

    # 讀取輸入文章
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"錯誤: 找不到檔案 {args.input}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")

    # 執行分析
    analyzer = PersuasionAnalyzer(text)

    aida = analyzer.analyze_aida()
    pas = analyzer.analyze_pas()
    four_cs = analyzer.analyze_4cs()
    triggers = analyzer.analyze_psychological_triggers()

    score, grade = analyzer.calculate_overall_score(aida, pas, four_cs, triggers)

    # 生成報告
    generator = ReportGenerator(aida, pas, four_cs, triggers, score, grade)

    if args.format == "json":
        report = generator.generate_json()
        output_path = args.output if args.output.endswith(".json") else args.output + ".json"
    else:
        report = generator.generate_markdown()
        output_path = args.output

    # 寫入報告
    Path(output_path).write_text(report, encoding="utf-8")

    print(f"說服力分數: {score}/100 (評級: {grade})")
    print(f"報告已生成: {output_path}")


if __name__ == "__main__":
    main()
