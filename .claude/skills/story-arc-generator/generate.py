#!/usr/bin/env python3
"""
Story Arc Generator Skill
生成故事弧線和情感曲線，為文章提供敘事結構建議

Usage:
    python3 generate.py input.md --mode analyze --output story_analysis.md
    python3 generate.py input.md --mode generate --structure hero_journey --output story_arc.md
    python3 generate.py input.md --mode emotion --pattern man_in_hole --output emotion_curve.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


# 故事結構模板
STORY_STRUCTURES = {
    "hero_journey": {
        "name": "Hero's Journey (英雄之旅)",
        "stages": [
            ("平凡世界", "描述讀者現狀和日常", 0.08),
            ("冒險召喚", "問題或機會出現", 0.08),
            ("拒絕召喚", "常見顧慮和阻力", 0.05),
            ("遇見導師", "解決方案/工具介紹", 0.10),
            ("跨越門檻", "開始行動的決定", 0.08),
            ("試煉盟友敵人", "執行過程中的挑戰", 0.15),
            ("逼近洞穴", "最困難的部分", 0.10),
            ("苦難折磨", "關鍵突破點", 0.10),
            ("獲得寶物", "掌握核心技能/成果", 0.10),
            ("歸途", "整合應用", 0.06),
            ("復活", "持續精進", 0.05),
            ("帶著寶物歸來", "最終成果和價值", 0.05),
        ],
        "best_for": ["轉型故事", "學習歷程", "個人成長", "產品導入"],
    },
    "three_act": {
        "name": "Three-Act Structure (三幕劇)",
        "stages": [
            ("第一幕：設定", "現狀、問題、利害關係", 0.25),
            ("第二幕：對抗", "嘗試、失敗、學習、突破", 0.50),
            ("第三幕：解決", "解決方案、成果、未來展望", 0.25),
        ],
        "best_for": ["問題解決", "教學文章", "how-to 指南"],
    },
    "story_spine": {
        "name": "Story Spine (Pixar 故事骨架)",
        "stages": [
            ("從前有...", "背景設定", 0.10),
            ("每天...", "日常狀態", 0.10),
            ("直到有一天...", "觸發事件", 0.10),
            ("因為這樣...(1)", "後果連鎖 1", 0.15),
            ("因為這樣...(2)", "後果連鎖 2", 0.15),
            ("因為這樣...(3)", "後果連鎖 3", 0.15),
            ("直到最後...", "高潮", 0.15),
            ("從那之後...", "新常態", 0.10),
        ],
        "best_for": ["案例分享", "經驗談", "故事型內容"],
    },
    "freytag": {
        "name": "Freytag's Pyramid (弗萊塔格金字塔)",
        "stages": [
            ("引入", "背景和角色設定", 0.15),
            ("上升動作", "衝突發展", 0.25),
            ("高潮", "最戲劇性的轉折點", 0.20),
            ("下降動作", "高潮後的影響", 0.25),
            ("結局", "新的平衡", 0.15),
        ],
        "best_for": ["戲劇性內容", "懸念文章", "衝突導向敘事"],
    },
}

# 情感曲線模式
EMOTION_PATTERNS = {
    "rags_to_riches": {
        "name": "Rags to Riches (鹹魚翻身)",
        "curve": [(-0.3, "低起點"), (0.0, "轉機"), (0.5, "上升"), (0.9, "成功")],
        "description": "從低谷開始，持續上升到高點",
        "best_for": ["成功故事", "逆襲敘事", "勵志內容"],
    },
    "man_in_hole": {
        "name": "Man in a Hole (穴中人)",
        "curve": [(0.5, "正常"), (0.0, "遇到問題"), (-0.5, "最低點"), (0.0, "開始解決"), (0.7, "解決成功")],
        "description": "從正常狀態掉入問題，然後爬出來變得更好",
        "best_for": ["問題解決", "學習經歷", "教學文章"],
    },
    "cinderella": {
        "name": "Cinderella (灰姑娘)",
        "curve": [(0.0, "普通"), (0.6, "第一次成功"), (0.2, "挫折"), (-0.3, "最低點"), (0.9, "最終成功")],
        "description": "起伏較大，有反覆但最終成功",
        "best_for": ["有反覆的成長故事", "真實經歷分享"],
    },
    "icarus": {
        "name": "Icarus (伊卡洛斯)",
        "curve": [(0.0, "起點"), (0.5, "上升"), (0.9, "高峰"), (0.3, "開始下降"), (-0.5, "墜落")],
        "description": "上升到高點後下墜",
        "best_for": ["警世故事", "失敗教訓", "風險提醒"],
    },
    "oedipus": {
        "name": "Oedipus (俄狄浦斯)",
        "curve": [(0.5, "高起點"), (0.2, "發現問題"), (-0.2, "真相揭露"), (-0.6, "最低點")],
        "description": "從高點持續下降",
        "best_for": ["悲劇", "深刻反思", "批判性內容"],
    },
}

# 敘事元素檢測模式
NARRATIVE_PATTERNS = {
    "hook": [
        (r"^.{0,50}[?？]", "問句開頭"),
        (r"^(?:你|妳)(?:有沒有|是否|曾經)", "第二人稱開頭"),
        (r"^(?:想像|假設|如果)", "假設情境"),
        (r"^\d+(?:%|萬|億)", "數據開頭"),
        (r"^[「『\"']", "引言開頭"),
    ],
    "conflict": [
        (r"(?:但是|然而|不過|可是|卻)", "轉折詞"),
        (r"(?:問題|挑戰|困難|障礙|瓶頸)", "問題詞彙"),
        (r"(?:失敗|錯誤|踩坑|血淚)", "失敗經驗"),
        (r"(?:矛盾|衝突|對立|掙扎)", "衝突詞彙"),
    ],
    "turning_point": [
        (r"(?:直到|終於|後來|最終)", "轉折標記"),
        (r"(?:發現|意識到|突然|恍然)", "領悟時刻"),
        (r"(?:原來|其實|真正的)", "真相揭示"),
        (r"(?:改變|轉變|突破)", "改變標記"),
    ],
    "climax": [
        (r"(?:最(?:重要|關鍵|核心))", "最高級修飾"),
        (r"(?:成功|達成|實現|完成)", "成就詞彙"),
        (r"(?:驚人|震撼|驚訝)", "情感高峰詞"),
    ],
    "resolution": [
        (r"(?:總結|總的來說|最後)", "總結標記"),
        (r"(?:從此|從那之後|之後)", "結局標記"),
        (r"(?:建議|希望|期待)", "展望詞彙"),
        (r"(?:行動|開始|嘗試)", "行動呼籲"),
    ],
}


class StoryArcGenerator:
    """故事弧線生成器"""

    def __init__(self, content: str):
        self.content = content
        self.paragraphs = self._split_paragraphs()
        self.total_chars = len(content)

    def _split_paragraphs(self) -> List[str]:
        """分割段落"""
        paragraphs = re.split(r'\n\s*\n', self.content)
        return [p.strip() for p in paragraphs if p.strip()]

    def analyze(self) -> Dict:
        """分析現有文章的故事結構"""
        results = {
            "elements": self._detect_narrative_elements(),
            "structure_match": self._match_structure(),
            "emotion_curve": self._detect_emotion_curve(),
            "scores": self._calculate_scores(),
            "recommendations": [],
        }

        results["recommendations"] = self._generate_recommendations(results)
        return results

    def _detect_narrative_elements(self) -> Dict:
        """檢測敘事元素"""
        elements = {}

        for element_type, patterns in NARRATIVE_PATTERNS.items():
            found = []
            for i, para in enumerate(self.paragraphs):
                for pattern, desc in patterns:
                    if re.search(pattern, para):
                        position = (i + 1) / len(self.paragraphs) * 100
                        found.append({
                            "paragraph": i + 1,
                            "position": f"{position:.0f}%",
                            "type": desc,
                            "text_preview": para[:50] + "..." if len(para) > 50 else para,
                        })
                        break

            elements[element_type] = {
                "found": len(found) > 0,
                "count": len(found),
                "instances": found[:3],  # 最多顯示3個
            }

        return elements

    def _match_structure(self) -> Dict:
        """匹配最適合的故事結構"""
        matches = {}

        for struct_id, struct_info in STORY_STRUCTURES.items():
            score = self._calculate_structure_match(struct_id)
            matches[struct_id] = {
                "name": struct_info["name"],
                "score": score,
                "best_for": struct_info["best_for"],
            }

        # 找出最佳匹配
        best_match = max(matches.items(), key=lambda x: x[1]["score"])
        return {
            "best_structure": best_match[0],
            "best_name": best_match[1]["name"],
            "confidence": best_match[1]["score"],
            "all_matches": matches,
        }

    def _calculate_structure_match(self, structure_id: str) -> int:
        """計算結構匹配度"""
        structure = STORY_STRUCTURES[structure_id]
        total_stages = len(structure["stages"])
        matched_stages = 0

        # 簡化的匹配邏輯：根據段落數和內容特徵
        para_count = len(self.paragraphs)

        # 檢查是否有足夠的段落來支持這個結構
        if para_count >= total_stages * 0.5:
            matched_stages += 2

        # 檢查敘事元素
        elements = self._detect_narrative_elements()
        if elements.get("hook", {}).get("found"):
            matched_stages += 2
        if elements.get("conflict", {}).get("found"):
            matched_stages += 2
        if elements.get("turning_point", {}).get("found"):
            matched_stages += 2
        if elements.get("resolution", {}).get("found"):
            matched_stages += 2

        # 特定結構加分
        if structure_id == "hero_journey" and para_count >= 8:
            matched_stages += 1
        elif structure_id == "three_act" and para_count >= 5:
            matched_stages += 1
        elif structure_id == "story_spine" and elements.get("turning_point", {}).get("count", 0) >= 2:
            matched_stages += 1

        max_score = 12
        return min(100, int(matched_stages / max_score * 100))

    def _detect_emotion_curve(self) -> Dict:
        """檢測情感曲線"""
        # 簡化的情感分析
        positive_words = r"(?:成功|開心|興奮|驚喜|感謝|喜歡|愛|棒|優秀|完美|滿意)"
        negative_words = r"(?:失敗|困難|痛苦|糟糕|問題|挑戰|困擾|擔心|焦慮|挫折)"

        curve_points = []
        for i, para in enumerate(self.paragraphs):
            pos_count = len(re.findall(positive_words, para))
            neg_count = len(re.findall(negative_words, para))
            sentiment = (pos_count - neg_count) / max(1, pos_count + neg_count)
            curve_points.append({
                "position": (i + 1) / len(self.paragraphs),
                "sentiment": sentiment,
                "paragraph": i + 1,
            })

        # 匹配情感模式
        best_pattern = self._match_emotion_pattern(curve_points)

        return {
            "curve_points": curve_points,
            "pattern_match": best_pattern,
            "has_variation": self._check_emotion_variation(curve_points),
        }

    def _match_emotion_pattern(self, curve_points: List[Dict]) -> Dict:
        """匹配情感模式"""
        if len(curve_points) < 3:
            return {"pattern": "unknown", "confidence": 0}

        # 計算整體趨勢
        start_sentiment = curve_points[0]["sentiment"]
        mid_sentiment = curve_points[len(curve_points)//2]["sentiment"]
        end_sentiment = curve_points[-1]["sentiment"]

        # 簡化的模式匹配
        if start_sentiment < 0 and end_sentiment > 0.3:
            return {"pattern": "rags_to_riches", "name": "鹹魚翻身", "confidence": 75}
        elif start_sentiment > 0 and mid_sentiment < 0 and end_sentiment > 0:
            return {"pattern": "man_in_hole", "name": "穴中人", "confidence": 80}
        elif start_sentiment > 0.3 and end_sentiment < 0:
            return {"pattern": "icarus", "name": "伊卡洛斯", "confidence": 70}
        else:
            return {"pattern": "neutral", "name": "平淡", "confidence": 50}

    def _check_emotion_variation(self, curve_points: List[Dict]) -> bool:
        """檢查是否有足夠的情感起伏"""
        if len(curve_points) < 3:
            return False

        sentiments = [p["sentiment"] for p in curve_points]
        variation = max(sentiments) - min(sentiments)
        return variation > 0.3

    def _calculate_scores(self) -> Dict:
        """計算各項分數"""
        elements = self._detect_narrative_elements()
        emotion = self._detect_emotion_curve()

        # 開頭吸引力
        hook_score = 80 if elements.get("hook", {}).get("found") else 40
        if elements.get("hook", {}).get("count", 0) > 1:
            hook_score = min(100, hook_score + 10)

        # 中段張力
        conflict_score = 50
        if elements.get("conflict", {}).get("found"):
            conflict_score += 20
        if elements.get("turning_point", {}).get("found"):
            conflict_score += 20
        if emotion.get("has_variation"):
            conflict_score += 10

        # 結尾收束
        resolution_score = 60 if elements.get("resolution", {}).get("found") else 30
        if elements.get("climax", {}).get("found"):
            resolution_score += 20

        # 整體分數
        overall = int(hook_score * 0.3 + conflict_score * 0.4 + resolution_score * 0.3)

        return {
            "overall": overall,
            "hook_attraction": hook_score,
            "mid_tension": conflict_score,
            "ending_closure": resolution_score,
            "grade": self._get_grade(overall),
        }

    def _get_grade(self, score: int) -> str:
        """獲取等級"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"

    def _generate_recommendations(self, results: Dict) -> List[Dict]:
        """生成改進建議"""
        recommendations = []
        elements = results["elements"]
        scores = results["scores"]

        if not elements.get("hook", {}).get("found"):
            recommendations.append({
                "priority": "high",
                "area": "開頭",
                "issue": "缺乏吸引人的開場鉤子",
                "suggestion": "考慮使用問句、驚人數據或情境描述作為開頭",
            })

        if not elements.get("conflict", {}).get("found"):
            recommendations.append({
                "priority": "high",
                "area": "衝突",
                "issue": "缺少明確的衝突或問題設定",
                "suggestion": "加入讀者可能面臨的挑戰或痛點描述",
            })

        if not elements.get("turning_point", {}).get("found"):
            recommendations.append({
                "priority": "medium",
                "area": "轉折",
                "issue": "缺乏明確的轉折點",
                "suggestion": "加入「直到...」「發現...」等轉折敘述",
            })

        if not results["emotion_curve"].get("has_variation"):
            recommendations.append({
                "priority": "medium",
                "area": "情感曲線",
                "issue": "情感起伏不足，敘事較平淡",
                "suggestion": "加入更多情感詞彙和高低起伏的情節",
            })

        if scores["ending_closure"] < 70:
            recommendations.append({
                "priority": "medium",
                "area": "結尾",
                "issue": "結尾收束力度不足",
                "suggestion": "加強總結和行動呼籲，給讀者明確的下一步",
            })

        return recommendations

    def generate_arc(self, structure: str = "hero_journey") -> Dict:
        """生成故事弧線建議"""
        if structure not in STORY_STRUCTURES:
            structure = "hero_journey"

        struct_info = STORY_STRUCTURES[structure]
        total_chars = self.total_chars or 2000  # 預設2000字

        stages_plan = []
        for stage_name, description, ratio in struct_info["stages"]:
            char_count = int(total_chars * ratio)
            stages_plan.append({
                "stage": stage_name,
                "description": description,
                "ratio": f"{ratio*100:.0f}%",
                "suggested_chars": char_count,
                "content_tips": self._get_stage_tips(stage_name),
            })

        turning_points = self._suggest_turning_points(structure)

        return {
            "structure": structure,
            "structure_name": struct_info["name"],
            "best_for": struct_info["best_for"],
            "stages": stages_plan,
            "turning_points": turning_points,
            "total_stages": len(stages_plan),
        }

    def _get_stage_tips(self, stage_name: str) -> List[str]:
        """獲取階段寫作提示"""
        tips_map = {
            "平凡世界": ["描述讀者目前的處境", "建立共鳴和認同感", "使用「你是否也...」句式"],
            "冒險召喚": ["提出改變的機會", "暗示可能的好處", "製造好奇心"],
            "遇見導師": ["介紹解決方案", "建立信任和權威", "展示專業知識"],
            "試煉盟友敵人": ["分享具體步驟", "預告可能的困難", "提供實用技巧"],
            "獲得寶物": ["展示成果", "分享成功經驗", "證明方法有效"],
            "第一幕：設定": ["建立背景", "介紹問題", "設定利害關係"],
            "第二幕：對抗": ["展示嘗試過程", "描述失敗經歷", "呈現突破時刻"],
            "第三幕：解決": ["總結解決方案", "展示成果", "提供行動呼籲"],
        }
        return tips_map.get(stage_name, ["根據主題發揮"])

    def _suggest_turning_points(self, structure: str) -> List[Dict]:
        """建議轉折點位置"""
        if structure == "hero_journey":
            return [
                {"position": "20%", "name": "第一轉折", "description": "從問題認知到尋找解決方案"},
                {"position": "50%", "name": "中點", "description": "最大挑戰出現，決定性時刻"},
                {"position": "80%", "name": "第二轉折", "description": "突破達成，準備收尾"},
            ]
        elif structure == "three_act":
            return [
                {"position": "25%", "name": "情節點1", "description": "從設定進入衝突"},
                {"position": "75%", "name": "情節點2", "description": "從衝突進入解決"},
            ]
        else:
            return [
                {"position": "33%", "name": "第一轉折", "description": "故事開始升溫"},
                {"position": "66%", "name": "第二轉折", "description": "故事走向結局"},
            ]

    def generate_emotion_curve(self, pattern: str = "man_in_hole") -> Dict:
        """生成情感曲線設計"""
        if pattern not in EMOTION_PATTERNS:
            pattern = "man_in_hole"

        pattern_info = EMOTION_PATTERNS[pattern]
        para_count = max(5, len(self.paragraphs))

        curve_design = []
        for i, (value, label) in enumerate(pattern_info["curve"]):
            position = i / (len(pattern_info["curve"]) - 1)
            para_index = int(position * (para_count - 1)) + 1
            curve_design.append({
                "position": f"{position*100:.0f}%",
                "paragraph": para_index,
                "emotion_value": value,
                "label": label,
                "writing_tips": self._get_emotion_tips(value),
            })

        return {
            "pattern": pattern,
            "pattern_name": pattern_info["name"],
            "description": pattern_info["description"],
            "best_for": pattern_info["best_for"],
            "curve_points": curve_design,
            "ascii_visualization": self._generate_ascii_curve(pattern_info["curve"]),
        }

    def _get_emotion_tips(self, value: float) -> str:
        """根據情感值獲取寫作提示"""
        if value >= 0.7:
            return "使用積極詞彙，展示成功和喜悅"
        elif value >= 0.3:
            return "保持正面但務實的語調"
        elif value >= -0.3:
            return "中性描述，客觀陳述"
        elif value >= -0.7:
            return "描述困難和挑戰，引發共鳴"
        else:
            return "深入痛點，製造最低谷的情感衝擊"

    def _generate_ascii_curve(self, curve: List[Tuple]) -> str:
        """生成 ASCII 情感曲線圖"""
        height = 7
        width = 40
        canvas = [[" " for _ in range(width)] for _ in range(height)]

        # 繪製座標軸
        for i in range(height):
            canvas[i][0] = "|"
        for i in range(width):
            canvas[height-1][i] = "-"
        canvas[height-1][0] = "+"

        # 繪製曲線點
        for i, (value, _) in enumerate(curve):
            x = int(i / (len(curve) - 1) * (width - 2)) + 1
            y = int((1 - (value + 1) / 2) * (height - 2))
            y = max(0, min(height - 2, y))
            canvas[y][x] = "*"

        # 連接點
        for i in range(len(curve) - 1):
            x1 = int(i / (len(curve) - 1) * (width - 2)) + 1
            x2 = int((i + 1) / (len(curve) - 1) * (width - 2)) + 1
            for x in range(x1 + 1, x2):
                y1 = int((1 - (curve[i][0] + 1) / 2) * (height - 2))
                y2 = int((1 - (curve[i + 1][0] + 1) / 2) * (height - 2))
                y = int(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
                y = max(0, min(height - 2, y))
                if canvas[y][x] == " ":
                    canvas[y][x] = "."

        return "\n".join(["".join(row) for row in canvas])


def generate_markdown_report(results: Dict, mode: str) -> str:
    """生成 Markdown 格式報告"""
    report = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if mode == "analyze":
        report.append("# 故事結構分析報告")
        report.append(f"\n**生成時間**: {timestamp}")

        # 敘事強度評分
        scores = results.get("scores", {})
        report.append("\n## 敘事強度評分")
        report.append(f"\n- **整體分數**: {scores.get('overall', 0)}/100")
        report.append(f"- **評級**: {scores.get('grade', 'N/A')}")
        report.append(f"- **開頭吸引力**: {scores.get('hook_attraction', 0)}/100")
        report.append(f"- **中段張力**: {scores.get('mid_tension', 0)}/100")
        report.append(f"- **結尾收束**: {scores.get('ending_closure', 0)}/100")

        # 現有結構檢測
        report.append("\n## 現有結構檢測")
        report.append("\n| 元素 | 狀態 | 數量 | 說明 |")
        report.append("|------|------|------|------|")

        element_names = {
            "hook": "開場鉤子",
            "conflict": "衝突設定",
            "turning_point": "轉折點",
            "climax": "高潮",
            "resolution": "結局",
        }

        elements = results.get("elements", {})
        for key, name in element_names.items():
            elem = elements.get(key, {})
            status = "✅" if elem.get("found") else "❌"
            count = elem.get("count", 0)
            instances = elem.get("instances", [])
            desc = instances[0].get("type", "未檢測到") if instances else "未檢測到"
            report.append(f"| {name} | {status} | {count} | {desc} |")

        # 結構匹配
        structure_match = results.get("structure_match", {})
        report.append("\n## 建議結構")
        report.append(f"\n- **最佳匹配**: {structure_match.get('best_name', 'N/A')}")
        report.append(f"- **匹配度**: {structure_match.get('confidence', 0)}%")

        # 情感曲線
        emotion = results.get("emotion_curve", {})
        pattern = emotion.get("pattern_match", {})
        report.append("\n## 情感曲線分析")
        report.append(f"\n- **檢測到的模式**: {pattern.get('name', '未知')}")
        report.append(f"- **信心度**: {pattern.get('confidence', 0)}%")
        report.append(f"- **有足夠起伏**: {'是' if emotion.get('has_variation') else '否'}")

        # 改進建議
        recommendations = results.get("recommendations", [])
        if recommendations:
            report.append("\n## 改進建議")
            for rec in recommendations:
                priority_icon = "🔴" if rec["priority"] == "high" else "🟡"
                report.append(f"\n### {priority_icon} {rec['area']}")
                report.append(f"- **問題**: {rec['issue']}")
                report.append(f"- **建議**: {rec['suggestion']}")

    elif mode == "generate":
        report.append("# 故事弧線設計")
        report.append(f"\n**生成時間**: {timestamp}")
        report.append(f"\n## 推薦結構：{results.get('structure_name', 'N/A')}")
        report.append(f"\n**適用於**: {', '.join(results.get('best_for', []))}")

        # 段落規劃
        report.append("\n## 段落規劃")
        report.append("\n| 階段 | 描述 | 比例 | 建議字數 |")
        report.append("|------|------|------|----------|")

        for stage in results.get("stages", []):
            report.append(f"| {stage['stage']} | {stage['description']} | {stage['ratio']} | {stage['suggested_chars']} |")

        # 轉折點設計
        report.append("\n## 轉折點設計")
        for tp in results.get("turning_points", []):
            report.append(f"\n### {tp['name']} (約 {tp['position']} 處)")
            report.append(f"- {tp['description']}")

        # 各階段寫作提示
        report.append("\n## 各階段寫作提示")
        for stage in results.get("stages", []):
            report.append(f"\n### {stage['stage']}")
            for tip in stage.get("content_tips", []):
                report.append(f"- {tip}")

    elif mode == "emotion":
        report.append("# 情感曲線設計")
        report.append(f"\n**生成時間**: {timestamp}")
        report.append(f"\n## 採用模式：{results.get('pattern_name', 'N/A')}")
        report.append(f"\n**描述**: {results.get('description', '')}")
        report.append(f"\n**適用於**: {', '.join(results.get('best_for', []))}")

        # 視覺化
        report.append("\n## 情感曲線視覺化")
        report.append("\n```")
        report.append(results.get("ascii_visualization", ""))
        report.append("```")

        # 曲線設計點
        report.append("\n## 情感節點設計")
        report.append("\n| 位置 | 段落 | 情感值 | 標籤 | 寫作提示 |")
        report.append("|------|------|--------|------|----------|")

        for point in results.get("curve_points", []):
            report.append(f"| {point['position']} | {point['paragraph']} | {point['emotion_value']:.1f} | {point['label']} | {point['writing_tips']} |")

    report.append("\n---")
    report.append("\n**Story Arc Generator Skill v1.0.0**")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Story Arc Generator - 生成故事弧線和情感曲線"
    )
    parser.add_argument("input", help="輸入文章路徑")
    parser.add_argument("-m", "--mode", choices=["analyze", "generate", "emotion"],
                       default="analyze", help="運行模式")
    parser.add_argument("-s", "--structure", choices=list(STORY_STRUCTURES.keys()),
                       default="hero_journey", help="故事結構類型")
    parser.add_argument("-p", "--pattern", choices=list(EMOTION_PATTERNS.keys()),
                       default="man_in_hole", help="情感曲線模式")
    parser.add_argument("-o", "--output", default="story_arc.md", help="輸出檔案路徑")
    parser.add_argument("--format", choices=["markdown", "json"],
                       default="markdown", help="輸出格式")

    args = parser.parse_args()

    # 讀取輸入檔案
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"錯誤：找不到輸入檔案 {args.input}")
        sys.exit(1)

    content = input_path.read_text(encoding="utf-8")

    # 創建生成器
    generator = StoryArcGenerator(content)

    # 根據模式執行
    if args.mode == "analyze":
        results = generator.analyze()
    elif args.mode == "generate":
        results = generator.generate_arc(args.structure)
    elif args.mode == "emotion":
        results = generator.generate_emotion_curve(args.pattern)

    # 輸出結果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "json":
        output_path.write_text(
            json.dumps(results, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    else:
        report = generate_markdown_report(results, args.mode)
        output_path.write_text(report, encoding="utf-8")

    print(f"✅ 報告已生成: {output_path}")

    # 根據結果返回適當的退出碼
    if args.mode == "analyze":
        score = results.get("scores", {}).get("overall", 0)
        if score < 60:
            print(f"⚠️ 敘事強度分數 ({score}/100) 低於閾值 (60)")
            sys.exit(1)
        else:
            print(f"✅ 敘事強度分數: {score}/100")

    sys.exit(0)


if __name__ == "__main__":
    main()
