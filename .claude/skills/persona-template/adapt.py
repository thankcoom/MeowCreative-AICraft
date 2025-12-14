#!/usr/bin/env python3
"""
Persona Template Skill
管理和應用讀者 Persona 模板，支援內容適配和多版本生成

Usage:
    python3 adapt.py list
    python3 adapt.py show beginner
    python3 adapt.py adapt input.md --persona beginner --output adapted.md
    python3 adapt.py multi-adapt input.md --personas beginner,expert --output-dir versions/
    python3 adapt.py verify original.md adapted.md --persona beginner
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import yaml


# 預設 Persona 模板
DEFAULT_PERSONAS = {
    "beginner": {
        "id": "beginner",
        "name": "新手小白",
        "description": "剛接觸此領域的初學者",
        "icon": "🌱",
        "characteristics": {
            "knowledge_level": 1,
            "attention_span": "short",
            "preferred_format": "visual_heavy",
        },
        "adaptation": {
            "vocabulary": {
                "complexity": "simple",
                "explain_jargon": True,
            },
            "structure": {
                "paragraph_length": "short",
                "header_frequency": "dense",
                "list_usage": "high",
            },
            "content": {
                "include_basics": True,
                "example_frequency": "high",
            },
            "tone": {
                "formality": 0.3,
                "encouragement": 0.9,
            },
        },
    },
    "intermediate": {
        "id": "intermediate",
        "name": "進階使用者",
        "description": "有基礎知識，尋求深入理解",
        "icon": "📈",
        "characteristics": {
            "knowledge_level": 3,
            "attention_span": "medium",
            "preferred_format": "balanced",
        },
        "adaptation": {
            "vocabulary": {
                "complexity": "medium",
                "explain_jargon": "briefly",
            },
            "structure": {
                "paragraph_length": "medium",
                "header_frequency": "normal",
                "list_usage": "medium",
            },
            "content": {
                "skip_basics": True,
                "best_practices": True,
            },
            "tone": {
                "formality": 0.5,
                "directness": 0.7,
            },
        },
    },
    "expert": {
        "id": "expert",
        "name": "專家讀者",
        "description": "領域專家，尋求新知和深度",
        "icon": "🎓",
        "characteristics": {
            "knowledge_level": 5,
            "attention_span": "long",
            "preferred_format": "text_heavy",
        },
        "adaptation": {
            "vocabulary": {
                "complexity": "high",
                "no_explanations": True,
            },
            "structure": {
                "paragraph_length": "long",
                "header_frequency": "sparse",
                "list_usage": "low",
            },
            "content": {
                "deep_dive": True,
                "edge_cases": True,
            },
            "tone": {
                "formality": 0.8,
                "precision": 0.9,
            },
        },
    },
    "decision_maker": {
        "id": "decision_maker",
        "name": "決策者",
        "description": "需要做出決定的管理者",
        "icon": "💼",
        "characteristics": {
            "knowledge_level": "varies",
            "attention_span": "short",
            "preferred_format": "summary_first",
        },
        "adaptation": {
            "vocabulary": {
                "complexity": "medium",
                "business_focus": True,
            },
            "structure": {
                "executive_summary": True,
                "bullet_points": "high",
            },
            "content": {
                "roi_focus": True,
                "recommendations": True,
            },
            "tone": {
                "formality": 0.7,
                "confidence": 0.8,
            },
        },
    },
    "gen_z": {
        "id": "gen_z",
        "name": "Z 世代",
        "description": "1997-2012 年出生的年輕讀者",
        "icon": "⚡",
        "characteristics": {
            "knowledge_level": "varies",
            "attention_span": "very_short",
            "preferred_format": "snackable",
        },
        "adaptation": {
            "vocabulary": {
                "complexity": "simple",
                "slang_ok": True,
            },
            "structure": {
                "paragraph_length": "very_short",
                "visual_breaks": True,
            },
            "content": {
                "relevance_first": True,
                "social_proof": True,
            },
            "tone": {
                "formality": 0.1,
                "authenticity": 0.9,
            },
        },
    },
    "professional": {
        "id": "professional",
        "name": "專業人士",
        "description": "有工作經驗的職場人士",
        "icon": "👔",
        "characteristics": {
            "knowledge_level": 3,
            "attention_span": "medium",
            "preferred_format": "practical",
        },
        "adaptation": {
            "vocabulary": {
                "complexity": "medium",
                "industry_terms": True,
            },
            "structure": {
                "problem_solution": True,
                "checklists": True,
            },
            "content": {
                "practical_focus": True,
                "tool_recommendations": True,
            },
            "tone": {
                "formality": 0.6,
                "practical": 0.9,
            },
        },
    },
}

# 自定義 Persona 存儲路徑
CUSTOM_PERSONAS_PATH = Path(__file__).parent / "custom_personas"


class PersonaAdapter:
    """Persona 適配器"""

    def __init__(self):
        self.personas = self._load_personas()

    def _load_personas(self) -> Dict:
        """載入所有 Persona"""
        personas = DEFAULT_PERSONAS.copy()

        # 載入自定義 Persona
        if CUSTOM_PERSONAS_PATH.exists():
            for f in CUSTOM_PERSONAS_PATH.glob("*.yaml"):
                data = yaml.safe_load(f.read_text(encoding="utf-8"))
                if data and "id" in data:
                    personas[data["id"]] = data

        return personas

    def list_personas(self) -> List[Dict]:
        """列出所有 Persona"""
        return [
            {
                "id": p["id"],
                "name": p["name"],
                "icon": p.get("icon", "👤"),
                "description": p["description"],
                "knowledge_level": p["characteristics"].get("knowledge_level", "varies"),
            }
            for p in self.personas.values()
        ]

    def get_persona(self, persona_id: str) -> Optional[Dict]:
        """獲取特定 Persona"""
        return self.personas.get(persona_id)

    def adapt_content(self, content: str, persona_id: str) -> Dict:
        """適配內容"""
        persona = self.get_persona(persona_id)
        if not persona:
            return {"error": f"Persona 不存在: {persona_id}"}

        original_stats = self._analyze_content(content)
        adapted_content = self._apply_adaptation(content, persona)
        adapted_stats = self._analyze_content(adapted_content)

        return {
            "persona": persona_id,
            "persona_name": persona["name"],
            "original_content": content,
            "adapted_content": adapted_content,
            "original_stats": original_stats,
            "adapted_stats": adapted_stats,
            "changes": self._calculate_changes(original_stats, adapted_stats),
        }

    def _analyze_content(self, content: str) -> Dict:
        """分析內容統計"""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        sentences = re.split(r'[。！？.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = len(content)
        avg_sentence_len = words / max(1, len(sentences))
        avg_paragraph_len = words / max(1, len(paragraphs))

        # 統計專業術語 (簡化版)
        jargon_patterns = [
            r'API', r'SDK', r'框架', r'演算法', r'迭代',
            r'優化', r'效能', r'架構', r'模組', r'介面',
        ]
        jargon_count = sum(len(re.findall(p, content)) for p in jargon_patterns)

        # 統計列表項目
        list_items = len(re.findall(r'^[-*]\s', content, re.MULTILINE))

        # 統計標題
        headers = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))

        return {
            "word_count": words,
            "paragraph_count": len(paragraphs),
            "sentence_count": len(sentences),
            "avg_sentence_length": round(avg_sentence_len, 1),
            "avg_paragraph_length": round(avg_paragraph_len, 1),
            "jargon_count": jargon_count,
            "list_items": list_items,
            "header_count": headers,
        }

    def _apply_adaptation(self, content: str, persona: Dict) -> str:
        """應用適配規則"""
        adapted = content
        adaptation = persona.get("adaptation", {})

        # 詞彙適配
        vocab = adaptation.get("vocabulary", {})
        if vocab.get("explain_jargon"):
            adapted = self._add_jargon_explanations(adapted)
        if vocab.get("complexity") == "simple":
            adapted = self._simplify_vocabulary(adapted)

        # 結構適配
        structure = adaptation.get("structure", {})
        if structure.get("paragraph_length") in ["short", "very_short"]:
            adapted = self._shorten_paragraphs(adapted)
        if structure.get("list_usage") == "high":
            adapted = self._enhance_lists(adapted)
        if structure.get("header_frequency") == "dense":
            adapted = self._add_headers(adapted)

        # 內容適配
        content_rules = adaptation.get("content", {})
        if content_rules.get("include_basics"):
            adapted = self._add_basics(adapted)
        if content_rules.get("example_frequency") == "high":
            adapted = self._enhance_examples(adapted)

        return adapted

    def _add_jargon_explanations(self, content: str) -> str:
        """添加專業術語解釋"""
        explanations = {
            "API": "API（應用程式介面，讓不同軟體可以互相溝通）",
            "SDK": "SDK（軟體開發套件，幫助開發者更快建立應用）",
        }
        for term, explanation in explanations.items():
            # 只替換第一次出現
            if term in content and explanation not in content:
                content = content.replace(term, explanation, 1)
        return content

    def _simplify_vocabulary(self, content: str) -> str:
        """簡化詞彙"""
        replacements = {
            "優化": "改善",
            "迭代": "改進",
            "實現": "做到",
            "架構": "結構",
            "配置": "設定",
        }
        for old, new in replacements.items():
            content = content.replace(old, new)
        return content

    def _shorten_paragraphs(self, content: str) -> str:
        """縮短段落"""
        paragraphs = content.split('\n\n')
        shortened = []
        for para in paragraphs:
            if len(para) > 300:
                # 嘗試在中間點斷開
                mid = len(para) // 2
                # 找最近的句號
                break_point = para.rfind('。', 0, mid + 50)
                if break_point > mid - 100:
                    shortened.append(para[:break_point + 1])
                    shortened.append(para[break_point + 1:].strip())
                else:
                    shortened.append(para)
            else:
                shortened.append(para)
        return '\n\n'.join(shortened)

    def _enhance_lists(self, content: str) -> str:
        """增強列表使用"""
        # 簡化實現：在有「首先」「其次」等詞的地方建議使用列表
        # 這裡只是示意，實際實現會更複雜
        return content

    def _add_headers(self, content: str) -> str:
        """增加標題密度"""
        # 簡化實現
        return content

    def _add_basics(self, content: str) -> str:
        """添加基礎說明"""
        # 簡化實現
        return content

    def _enhance_examples(self, content: str) -> str:
        """增強範例"""
        # 簡化實現
        return content

    def _calculate_changes(self, original: Dict, adapted: Dict) -> Dict:
        """計算變化"""
        changes = {}
        for key in original:
            orig_val = original[key]
            adapt_val = adapted[key]
            if isinstance(orig_val, (int, float)) and orig_val > 0:
                change_pct = ((adapt_val - orig_val) / orig_val) * 100
                changes[key] = {
                    "original": orig_val,
                    "adapted": adapt_val,
                    "change_percent": round(change_pct, 1),
                }
        return changes

    def verify_adaptation(self, original: str, adapted: str, persona_id: str) -> Dict:
        """驗證適配品質"""
        persona = self.get_persona(persona_id)
        if not persona:
            return {"error": f"Persona 不存在: {persona_id}"}

        original_stats = self._analyze_content(original)
        adapted_stats = self._analyze_content(adapted)

        # 核心訊息保留檢查 (簡化版：比較關鍵詞)
        original_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,4}', original))
        adapted_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,4}', adapted))
        keyword_retention = len(original_keywords & adapted_keywords) / max(1, len(original_keywords))

        # 計算可讀性分數 (簡化版)
        readability = self._calculate_readability(adapted_stats)

        # 風格匹配度
        style_match = self._check_style_match(adapted_stats, persona)

        # 計算總分
        scores = {
            "core_message_retention": round(keyword_retention * 100, 1),
            "readability_score": readability,
            "style_match": style_match,
        }

        total_score = (
            scores["core_message_retention"] * 0.4 +
            scores["readability_score"] * 0.3 +
            scores["style_match"] * 0.3
        )

        return {
            "persona": persona_id,
            "scores": scores,
            "total_score": round(total_score, 1),
            "passed": total_score >= 80 and keyword_retention >= 0.95,
            "issues": self._identify_issues(scores, persona),
        }

    def _calculate_readability(self, stats: Dict) -> float:
        """計算可讀性分數"""
        # 簡化版：基於句子長度和段落長度
        sentence_score = max(0, 100 - (stats["avg_sentence_length"] - 15) * 2)
        paragraph_score = max(0, 100 - (stats["avg_paragraph_length"] - 200) * 0.1)
        return round((sentence_score + paragraph_score) / 2, 1)

    def _check_style_match(self, stats: Dict, persona: Dict) -> float:
        """檢查風格匹配度"""
        # 簡化版
        adaptation = persona.get("adaptation", {})
        structure = adaptation.get("structure", {})

        score = 70  # 基礎分

        # 段落長度檢查
        expected_para_length = structure.get("paragraph_length", "medium")
        if expected_para_length == "short" and stats["avg_paragraph_length"] < 200:
            score += 15
        elif expected_para_length == "medium" and 200 <= stats["avg_paragraph_length"] <= 400:
            score += 15
        elif expected_para_length == "long" and stats["avg_paragraph_length"] > 400:
            score += 15

        # 列表使用檢查
        list_usage = structure.get("list_usage", "medium")
        if list_usage == "high" and stats["list_items"] > 5:
            score += 15

        return min(100, score)

    def _identify_issues(self, scores: Dict, persona: Dict) -> List[str]:
        """識別問題"""
        issues = []
        if scores["core_message_retention"] < 95:
            issues.append("核心訊息保留不足，建議檢查關鍵內容")
        if scores["readability_score"] < 70:
            issues.append("可讀性偏低，建議縮短句子或段落")
        if scores["style_match"] < 70:
            issues.append("風格匹配度不足，建議調整結構")
        return issues

    def create_persona(self, persona_id: str, name: str, config_file: Path) -> Dict:
        """創建自定義 Persona"""
        if not config_file.exists():
            return {"error": f"配置檔案不存在: {config_file}"}

        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        config["id"] = persona_id
        config["name"] = name

        # 確保目錄存在
        CUSTOM_PERSONAS_PATH.mkdir(parents=True, exist_ok=True)

        # 保存
        output_file = CUSTOM_PERSONAS_PATH / f"{persona_id}.yaml"
        output_file.write_text(
            yaml.dump(config, allow_unicode=True, default_flow_style=False),
            encoding="utf-8"
        )

        return {
            "status": "success",
            "persona_id": persona_id,
            "file": str(output_file),
            "message": f"Persona '{name}' 已創建",
        }


def generate_report(result: Dict) -> str:
    """生成適配報告"""
    lines = [
        "# Persona 適配報告",
        "",
        f"**目標 Persona**: {result['persona_name']} ({result['persona']})",
        f"**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 適配統計",
        "",
        "| 指標 | 原始 | 適配後 | 變化 |",
        "|------|------|--------|------|",
    ]

    changes = result.get("changes", {})
    for key, data in changes.items():
        change_str = f"+{data['change_percent']}%" if data['change_percent'] > 0 else f"{data['change_percent']}%"
        lines.append(f"| {key} | {data['original']} | {data['adapted']} | {change_str} |")

    lines.extend([
        "",
        "---",
        "",
        "*自動生成 by Persona Template Skill*",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Persona Template Skill - 讀者適配")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list
    subparsers.add_parser("list", help="列出所有 Persona")

    # show
    show_parser = subparsers.add_parser("show", help="顯示 Persona 詳情")
    show_parser.add_argument("persona_id", help="Persona ID")

    # adapt
    adapt_parser = subparsers.add_parser("adapt", help="適配內容")
    adapt_parser.add_argument("input", help="輸入檔案")
    adapt_parser.add_argument("--persona", required=True, help="目標 Persona")
    adapt_parser.add_argument("--output", default="adapted.md", help="輸出檔案")

    # multi-adapt
    multi_parser = subparsers.add_parser("multi-adapt", help="多版本生成")
    multi_parser.add_argument("input", help="輸入檔案")
    multi_parser.add_argument("--personas", required=True, help="Persona 列表 (逗號分隔)")
    multi_parser.add_argument("--output-dir", default="adapted_versions", help="輸出目錄")

    # verify
    verify_parser = subparsers.add_parser("verify", help="驗證適配品質")
    verify_parser.add_argument("original", help="原始檔案")
    verify_parser.add_argument("adapted", help="適配後檔案")
    verify_parser.add_argument("--persona", required=True, help="目標 Persona")

    # create
    create_parser = subparsers.add_parser("create", help="創建自定義 Persona")
    create_parser.add_argument("--id", required=True, help="Persona ID")
    create_parser.add_argument("--name", required=True, help="Persona 名稱")
    create_parser.add_argument("--config", required=True, help="配置檔案路徑")

    args = parser.parse_args()
    adapter = PersonaAdapter()

    if args.command == "list":
        personas = adapter.list_personas()
        print("可用的 Persona 模板:\n")
        for p in personas:
            print(f"  {p['icon']} {p['id']}: {p['name']}")
            print(f"     {p['description']}")
            print(f"     知識程度: {p['knowledge_level']}")
            print()

    elif args.command == "show":
        persona = adapter.get_persona(args.persona_id)
        if persona:
            print(f"{persona.get('icon', '👤')} {persona['name']} ({persona['id']})")
            print(f"\n{persona['description']}\n")
            print("特徵:")
            for key, value in persona.get("characteristics", {}).items():
                print(f"  - {key}: {value}")
            print("\n適配規則:")
            print(yaml.dump(persona.get("adaptation", {}), allow_unicode=True, default_flow_style=False))
        else:
            print(f"❌ Persona 不存在: {args.persona_id}")

    elif args.command == "adapt":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ 檔案不存在: {args.input}")
            sys.exit(1)

        content = input_path.read_text(encoding="utf-8")
        result = adapter.adapt_content(content, args.persona)

        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result["adapted_content"], encoding="utf-8")

        print(f"✅ 已適配到 {result['persona_name']}")
        print(f"   輸出: {output_path}")
        print(f"   字數變化: {result['original_stats']['word_count']} → {result['adapted_stats']['word_count']}")

    elif args.command == "multi-adapt":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ 檔案不存在: {args.input}")
            sys.exit(1)

        content = input_path.read_text(encoding="utf-8")
        personas = [p.strip() for p in args.personas.split(",")]
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"正在生成 {len(personas)} 個版本...\n")
        for persona_id in personas:
            result = adapter.adapt_content(content, persona_id)
            if "error" in result:
                print(f"  ❌ {persona_id}: {result['error']}")
                continue

            output_file = output_dir / f"{persona_id}_version.md"
            output_file.write_text(result["adapted_content"], encoding="utf-8")
            print(f"  ✅ {result['persona_name']} → {output_file.name}")

        print(f"\n✅ 完成！輸出目錄: {output_dir}")

    elif args.command == "verify":
        original_path = Path(args.original)
        adapted_path = Path(args.adapted)

        if not original_path.exists() or not adapted_path.exists():
            print("❌ 檔案不存在")
            sys.exit(1)

        original = original_path.read_text(encoding="utf-8")
        adapted = adapted_path.read_text(encoding="utf-8")

        result = adapter.verify_adaptation(original, adapted, args.persona)

        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)

        print(f"適配品質驗證 ({args.persona})")
        print(f"\n總分: {result['total_score']}/100 {'✅ 通過' if result['passed'] else '❌ 未通過'}")
        print(f"\n各項分數:")
        for key, score in result["scores"].items():
            print(f"  - {key}: {score}")

        if result["issues"]:
            print("\n問題:")
            for issue in result["issues"]:
                print(f"  ⚠️ {issue}")

    elif args.command == "create":
        result = adapter.create_persona(
            args.id,
            args.name,
            Path(args.config)
        )
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print(f"✅ {result['message']}")
        print(f"   檔案: {result['file']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
