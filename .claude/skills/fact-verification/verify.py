#!/usr/bin/env python3
"""
Fact Verification Skill - 事實驗證工具
用於檢測和驗證文章中的事實陳述、數據來源和專業聲明

使用方式:
    python3 verify.py input_article.md --output fact_check_report.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


# 事實類型識別模式
FACT_PATTERNS = {
    "data": [
        (r"\d+(?:\.\d+)?%", "百分比數據"),
        (r"\$[\d,]+(?:\.\d+)?", "金額數據"),
        (r"\d{4}年", "年份"),
        (r"(?:約|超過|近|達到)?\d+(?:萬|億|千)?(?:個|人|次|篇|項)?", "數量數據"),
        (r"(?:節省|提升|增加|減少|降低).*?\d+", "效果數據"),
    ],
    "claim": [
        (r"(?:導致|因為|所以|因此|由於)", "因果關係"),
        (r"(?:比|優於|勝過|超越|領先)", "比較性陳述"),
        (r"(?:最|唯一|第一|絕對|完全|100%)", "絕對性陳述"),
        (r"(?:可以|能夠|支援|兼容)", "能力聲明"),
    ],
    "citation": [
        (r"根據.*?(?:研究|調查|報告|數據)", "研究引用"),
        (r"(?:專家|學者|分析師)(?:表示|指出|認為)", "專家引用"),
        (r"(?:官方|政府|機構)(?:數據|資料|報告)", "官方來源"),
    ],
    "technical": [
        (r"(?:API|SDK|MCP|REST|GraphQL)", "技術術語"),
        (r"(?:Python|JavaScript|TypeScript)\s*\d+(?:\.\d+)?", "版本號"),
        (r"(?:支援|兼容|整合).*?(?:所有|全部|多種)", "相容性聲明"),
    ],
}

# 高風險特徵模式
HIGH_RISK_PATTERNS = [
    (r"\d+(?:\.\d+)?%.*?(?:用戶|開發者|人)", "無來源的用戶統計"),
    (r"(?:研究|調查)(?:顯示|發現|表明)", "可能虛構的研究引用"),
    (r"(?:絕對|肯定|一定|無疑|毫無疑問)", "過度自信語言"),
    (r"(?:最好|最佳|最強|最快|最)", "最高級形容詞"),
]

# 情感和主觀詞彙（這些不需要驗證）
SUBJECTIVE_PATTERNS = [
    r"我(?:認為|覺得|想|相信)",
    r"(?:可能|也許|或許|大概)",
    r"(?:個人|主觀)(?:經驗|看法|意見)",
]


class FactExtractor:
    """事實陳述提取器"""

    def __init__(self, text: str):
        self.text = text
        self.paragraphs = self._split_paragraphs()

    def _split_paragraphs(self) -> List[str]:
        """分割段落"""
        return [p.strip() for p in self.text.split("\n\n") if p.strip()]

    def extract_facts(self) -> List[Dict]:
        """提取所有事實陳述"""
        facts = []
        fact_id = 1

        for para_idx, paragraph in enumerate(self.paragraphs):
            # 按句子分割
            sentences = re.split(r"[。！？]", paragraph)

            for sentence in sentences:
                if not sentence.strip():
                    continue

                # 檢查是否包含主觀表達
                if self._is_subjective(sentence):
                    continue

                # 檢查各類事實模式
                for fact_type, patterns in FACT_PATTERNS.items():
                    for pattern, description in patterns:
                        if re.search(pattern, sentence):
                            facts.append(
                                {
                                    "id": f"F{fact_id}",
                                    "type": fact_type,
                                    "description": description,
                                    "text": sentence.strip(),
                                    "paragraph": para_idx + 1,
                                    "priority": self._calculate_priority(
                                        sentence, fact_type
                                    ),
                                }
                            )
                            fact_id += 1
                            break  # 每個句子只標記一次
                    else:
                        continue
                    break

        return facts

    def _is_subjective(self, text: str) -> bool:
        """檢查是否為主觀表達"""
        for pattern in SUBJECTIVE_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    def _calculate_priority(self, text: str, fact_type: str) -> str:
        """計算驗證優先級"""
        # 高優先級：數據型且無來源、絕對性陳述
        if fact_type == "data" and not re.search(r"根據|來源|調查", text):
            return "high"
        if re.search(r"(?:最|唯一|第一|絕對|100%)", text):
            return "high"
        if fact_type == "citation":
            return "high"

        # 中優先級：一般聲明
        if fact_type == "claim":
            return "medium"

        # 低優先級：技術術語、一般數據
        return "low"


class RiskCalculator:
    """幻覺風險計算器"""

    def __init__(self, experience_text: Optional[str] = None):
        self.experience_text = experience_text or ""
        self.experience_facts = self._extract_experience_facts()

    def _extract_experience_facts(self) -> set:
        """從經驗檔案提取可信事實"""
        facts = set()
        for line in self.experience_text.split("\n"):
            # 提取經驗檔案中的關鍵數據
            numbers = re.findall(r"\d+(?:\.\d+)?%?", line)
            facts.update(numbers)
        return facts

    def calculate_risk(self, fact: Dict) -> Tuple[int, List[str]]:
        """計算單個事實的幻覺風險"""
        risk_score = 50  # 基礎分數
        risk_factors = []

        text = fact["text"]

        # 檢查是否有來源標註
        if not re.search(r"根據|來源|調查|研究|官方", text):
            risk_score += 20
            risk_factors.append("缺少來源標註")

        # 檢查是否包含具體數據但無來源
        if re.search(r"\d+(?:\.\d+)?%", text) and not re.search(r"根據|調查", text):
            risk_score += 25
            risk_factors.append("具體數據無來源")

        # 檢查高風險模式
        for pattern, reason in HIGH_RISK_PATTERNS:
            if re.search(pattern, text):
                risk_score += 15
                risk_factors.append(reason)

        # 檢查是否在經驗檔案中
        if self._is_in_experience(text):
            risk_score -= 30
            risk_factors.append("來自真實經驗（降低風險）")

        # 檢查過度自信語言
        if re.search(r"(?:絕對|肯定|一定|無疑)", text):
            risk_score += 15
            risk_factors.append("過度自信語言")

        return min(100, max(0, risk_score)), risk_factors

    def _is_in_experience(self, text: str) -> bool:
        """檢查是否來自經驗檔案"""
        # 提取數據
        numbers = re.findall(r"\d+(?:\.\d+)?%?", text)
        for num in numbers:
            if num in self.experience_facts:
                return True
        return False


class VerificationReportGenerator:
    """驗證報告生成器"""

    def __init__(self, facts: List[Dict], risks: Dict[str, Tuple[int, List[str]]]):
        self.facts = facts
        self.risks = risks

    def generate_markdown(self) -> str:
        """生成 Markdown 格式報告"""
        # 計算統計
        total = len(self.facts)
        high_risk = sum(1 for f in self.facts if self.risks[f["id"]][0] > 70)
        medium_risk = sum(1 for f in self.facts if 40 < self.risks[f["id"]][0] <= 70)
        low_risk = total - high_risk - medium_risk

        # 計算可信度評分
        avg_risk = sum(self.risks[f["id"]][0] for f in self.facts) / max(total, 1)
        credibility_score = round(100 - avg_risk)

        report = f"""# 事實驗證報告

**生成時間**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**總體可信度評分**: {credibility_score}/100

## 驗證摘要

| 指標 | 數值 |
|------|------|
| 總事實陳述數 | {total} |
| 高風險項目 | {high_risk} ({round(high_risk/max(total,1)*100)}%) |
| 中風險項目 | {medium_risk} ({round(medium_risk/max(total,1)*100)}%) |
| 低風險項目 | {low_risk} ({round(low_risk/max(total,1)*100)}%) |

## 評級

"""
        # 評級
        if credibility_score >= 85:
            report += "**A** - 優秀：可直接進入下一階段\n\n"
        elif credibility_score >= 70:
            report += "**B** - 良好：建議修改高風險項目後繼續\n\n"
        elif credibility_score >= 50:
            report += "**C** - 可接受：需要修改多個項目\n\n"
        else:
            report += "**D** - 需改進：建議大幅修改或重寫\n\n"

        # 高風險項目
        report += "## 高風險項目 (必須處理)\n\n"
        high_risk_facts = [f for f in self.facts if self.risks[f["id"]][0] > 70]
        if high_risk_facts:
            for fact in high_risk_facts:
                risk_score, factors = self.risks[fact["id"]]
                report += f"""### {fact['id']}: {fact['description']}

- **原文**: "{fact['text']}"
- **位置**: 第{fact['paragraph']}段
- **風險等級**: {risk_score}/100
- **風險因素**: {', '.join(factors)}
- **建議**: 補充可靠來源或修改措辭

---

"""
        else:
            report += "無高風險項目。\n\n"

        # 中風險項目
        report += "## 中風險項目 (建議處理)\n\n"
        medium_risk_facts = [
            f for f in self.facts if 40 < self.risks[f["id"]][0] <= 70
        ]
        if medium_risk_facts:
            for fact in medium_risk_facts:
                risk_score, factors = self.risks[fact["id"]]
                report += f"- **{fact['id']}** (風險:{risk_score}): {fact['text'][:50]}... - {', '.join(factors)}\n"
        else:
            report += "無中風險項目。\n\n"

        # 低風險項目
        report += "\n## 低風險項目\n\n"
        low_risk_facts = [f for f in self.facts if self.risks[f["id"]][0] <= 40]
        if low_risk_facts:
            report += "| ID | 類型 | 摘要 | 風險 |\n"
            report += "|----|----|------|------|\n"
            for fact in low_risk_facts:
                risk_score = self.risks[fact["id"]][0]
                report += f"| {fact['id']} | {fact['description']} | {fact['text'][:30]}... | {risk_score} |\n"
        else:
            report += "無低風險項目。\n"

        # 建議
        report += f"""

## 給 Writer Agent 的修改建議

1. **必須修改** (高優先級):
"""
        for fact in high_risk_facts[:3]:
            report += f"   - {fact['id']}: 補充來源或修改 \"{fact['text'][:30]}...\"\n"

        report += f"""
2. **建議修改** (中優先級):
"""
        for fact in medium_risk_facts[:3]:
            report += f"   - {fact['id']}: 考慮補充說明\n"

        report += f"""

## 給 Blog Manager 的決策建議

- **可信度評分**: {credibility_score}/100
- **建議行動**: {"可直接進入下一階段" if credibility_score >= 85 else "建議修改後重新驗證" if credibility_score >= 70 else "需要大幅修改"}
"""

        return report

    def generate_json(self) -> str:
        """生成 JSON 格式報告"""
        total = len(self.facts)
        avg_risk = sum(self.risks[f["id"]][0] for f in self.facts) / max(total, 1)
        credibility_score = round(100 - avg_risk)

        data = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_statements": total,
                "high_risk": sum(1 for f in self.facts if self.risks[f["id"]][0] > 70),
                "medium_risk": sum(
                    1 for f in self.facts if 40 < self.risks[f["id"]][0] <= 70
                ),
                "low_risk": sum(1 for f in self.facts if self.risks[f["id"]][0] <= 40),
                "credibility_score": credibility_score,
            },
            "facts": [
                {
                    **fact,
                    "risk_score": self.risks[fact["id"]][0],
                    "risk_factors": self.risks[fact["id"]][1],
                }
                for fact in self.facts
            ],
        }

        return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="事實驗證工具")
    parser.add_argument("input", help="待驗證的文章路徑")
    parser.add_argument("--output", "-o", default="fact_check_report.md", help="輸出報告路徑")
    parser.add_argument(
        "--level",
        choices=["basic", "standard", "strict"],
        default="standard",
        help="驗證級別",
    )
    parser.add_argument("--experience", "-e", help="經驗檔案路徑")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="輸出格式"
    )

    args = parser.parse_args()

    # 讀取輸入文章
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"錯誤: 找不到檔案 {args.input}")
        sys.exit(1)

    article_text = input_path.read_text(encoding="utf-8")

    # 讀取經驗檔案（如果有）
    experience_text = ""
    if args.experience:
        exp_path = Path(args.experience)
        if exp_path.exists():
            experience_text = exp_path.read_text(encoding="utf-8")

    # 提取事實
    extractor = FactExtractor(article_text)
    facts = extractor.extract_facts()

    print(f"找到 {len(facts)} 個事實陳述")

    # 計算風險
    risk_calculator = RiskCalculator(experience_text)
    risks = {}
    for fact in facts:
        risk_score, factors = risk_calculator.calculate_risk(fact)
        risks[fact["id"]] = (risk_score, factors)

    # 生成報告
    generator = VerificationReportGenerator(facts, risks)

    if args.format == "json":
        report = generator.generate_json()
        output_path = (
            args.output if args.output.endswith(".json") else args.output + ".json"
        )
    else:
        report = generator.generate_markdown()
        output_path = args.output

    # 寫入報告
    Path(output_path).write_text(report, encoding="utf-8")
    print(f"驗證報告已生成: {output_path}")

    # 計算可信度評分
    avg_risk = sum(r[0] for r in risks.values()) / max(len(risks), 1)
    credibility_score = round(100 - avg_risk)
    print(f"可信度評分: {credibility_score}/100")


if __name__ == "__main__":
    main()
