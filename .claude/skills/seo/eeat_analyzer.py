#!/usr/bin/env python3
"""
E-E-A-T 分析器 (Experience, Expertise, Authoritativeness, Trustworthiness)

這個工具評估文章內容的 E-E-A-T 品質，這是 Google 2025 年最重視的排名因素。

版本: 1.0.0
建立日期: 2025-11-04
作者: 喵哩文創 AI 寫手系統團隊
"""

import re
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class EEATScore:
    """E-E-A-T 評分結果"""
    experience: float  # 經驗分數 (0-100)
    expertise: float   # 專業知識分數 (0-100)
    authoritativeness: float  # 權威性分數 (0-100)
    trustworthiness: float    # 可信度分數 (0-100)
    overall: float     # 總分 (0-100)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EEATAnalysisResult:
    """E-E-A-T 分析結果"""
    scores: EEATScore
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    details: Dict
    analyzed_at: str


class EEATAnalyzer:
    """E-E-A-T 內容品質分析器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化分析器

        Args:
            config_path: 配置文件路徑，如果為 None 則使用預設配置
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """載入配置文件"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 使用預設配置
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """取得預設配置"""
        return {
            'weights': {
                'experience': 0.30,
                'expertise': 0.25,
                'authoritativeness': 0.20,
                'trustworthiness': 0.25
            },
            'thresholds': {
                'excellent': 85,
                'good': 70,
                'fair': 55,
                'poor': 40
            }
        }

    def analyze(self, content: str, experience_profile_path: Optional[str] = None) -> EEATAnalysisResult:
        """
        分析文章的 E-E-A-T 品質

        Args:
            content: 文章內容（Markdown 格式）
            experience_profile_path: 用戶經驗檔案路徑（可選，但強烈建議提供）

        Returns:
            E-E-A-T 分析結果
        """
        # 讀取用戶經驗檔案
        experience_data = None
        if experience_profile_path and Path(experience_profile_path).exists():
            with open(experience_profile_path, 'r', encoding='utf-8') as f:
                experience_data = f.read()

        # 分析各項指標
        experience_score, exp_details = self._analyze_experience(content, experience_data)
        expertise_score, exp_details_2 = self._analyze_expertise(content)
        authority_score, auth_details = self._analyze_authoritativeness(content)
        trust_score, trust_details = self._analyze_trustworthiness(content)

        # 計算總分
        weights = self.config['weights']
        overall = (
            experience_score * weights['experience'] +
            expertise_score * weights['expertise'] +
            authority_score * weights['authoritativeness'] +
            trust_score * weights['trustworthiness']
        )

        scores = EEATScore(
            experience=round(experience_score, 2),
            expertise=round(expertise_score, 2),
            authoritativeness=round(authority_score, 2),
            trustworthiness=round(trust_score, 2),
            overall=round(overall, 2)
        )

        # 彙整優缺點和建議
        strengths, weaknesses, recommendations = self._generate_insights(
            scores, exp_details, exp_details_2, auth_details, trust_details
        )

        # 彙整詳細資訊
        details = {
            'experience': exp_details,
            'expertise': exp_details_2,
            'authoritativeness': auth_details,
            'trustworthiness': trust_details
        }

        return EEATAnalysisResult(
            scores=scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            details=details,
            analyzed_at=datetime.now().isoformat()
        )

    def _analyze_experience(self, content: str, experience_data: Optional[str]) -> Tuple[float, Dict]:
        """
        分析「經驗」維度

        檢查項目：
        - 是否有第一人稱的真實經驗敘述
        - 是否有具體的時間、地點、情境
        - 是否有個人見解和反思
        - 是否與 experience_profile.md 一致
        """
        score = 0.0
        details = {
            'has_first_person': False,
            'has_specific_details': False,
            'has_personal_insights': False,
            'consistent_with_profile': None,
            'experience_indicators': []
        }

        # 1. 檢查第一人稱敘述 (30分)
        first_person_patterns = [
            r'我[使用過|試過|發現|注意到|經歷|遇到]',
            r'當我[開始|嘗試|使用]',
            r'我的[經驗|心得|觀察|發現]',
            r'根據我的[實際|親身]'
        ]

        first_person_count = 0
        for pattern in first_person_patterns:
            matches = re.findall(pattern, content)
            first_person_count += len(matches)
            if matches:
                details['experience_indicators'].extend(matches[:2])  # 記錄前2個範例

        if first_person_count >= 5:
            score += 30
            details['has_first_person'] = True
        elif first_person_count >= 3:
            score += 20
            details['has_first_person'] = True
        elif first_person_count >= 1:
            score += 10
            details['has_first_person'] = True

        # 2. 檢查具體細節 (30分)
        # 時間參考
        time_patterns = [
            r'\d+[年個天週月]前',
            r'上[個週月年]',
            r'去年|今年',
            r'20\d{2}年',
            r'最近|近期'
        ]
        time_count = sum(len(re.findall(p, content)) for p in time_patterns)

        # 具體數字和數據
        specific_numbers = re.findall(r'\d+%|\d+倍|\d+小時|\d+天|\d+個', content)

        # 情境描述
        context_patterns = [
            r'在[使用|開發|測試|部署].*時',
            r'當[遇到|面對|處理]',
            r'[專案|系統|工具]中'
        ]
        context_count = sum(len(re.findall(p, content)) for p in context_patterns)

        specificity_score = min(30, (time_count * 5 + len(specific_numbers) * 3 + context_count * 5))
        score += specificity_score
        details['has_specific_details'] = specificity_score > 15

        # 3. 檢查個人見解 (20分)
        insight_patterns = [
            r'我[認為|覺得|建議|推薦]',
            r'個人[看法|觀點|建議]',
            r'值得注意的是',
            r'關鍵[在於|是]'
        ]
        insight_count = sum(len(re.findall(p, content)) for p in insight_patterns)

        if insight_count >= 3:
            score += 20
            details['has_personal_insights'] = True
        elif insight_count >= 2:
            score += 15
            details['has_personal_insights'] = True
        elif insight_count >= 1:
            score += 10
            details['has_personal_insights'] = True

        # 4. 與 experience_profile 一致性 (20分)
        if experience_data:
            # 簡單檢查：是否有經驗檔案中提到的主題
            consistency_score = self._check_experience_consistency(content, experience_data)
            score += consistency_score
            details['consistent_with_profile'] = consistency_score > 10
        else:
            # 沒有經驗檔案，無法驗證，給予基礎分
            score += 10
            details['consistent_with_profile'] = None

        return min(100, score), details

    def _check_experience_consistency(self, content: str, experience_data: str) -> float:
        """檢查內容與經驗檔案的一致性"""
        # 提取經驗檔案中的「可寫內容」
        can_write_section = re.search(r'## 可寫內容清單(.*?)##', experience_data, re.DOTALL)
        if not can_write_section:
            return 10  # 無法判斷，給予基礎分

        can_write_topics = can_write_section.group(1)

        # 提取「不可寫內容」
        cannot_write_section = re.search(r'## 不可寫內容清單(.*?)(?:##|$)', experience_data, re.DOTALL)

        # 簡單一致性檢查：內容中是否提到可寫主題
        # 這裡簡化處理，實際應該更複雜
        if any(topic in content for topic in ['實際', '經驗', '使用過', '試過']):
            return 20
        return 10

    def _analyze_expertise(self, content: str) -> Tuple[float, Dict]:
        """
        分析「專業知識」維度

        檢查項目：
        - 內容深度（是否深入技術細節）
        - 專業術語使用正確性
        - 理論與實踐結合
        - 程式碼範例品質
        """
        score = 0.0
        details = {
            'has_code_examples': False,
            'code_quality': 0,
            'technical_depth': 0,
            'theory_practice_balance': False,
            'professional_terms': []
        }

        # 1. 程式碼範例 (30分)
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        code_count = len(code_blocks)

        if code_count >= 3:
            score += 20
            details['has_code_examples'] = True

            # 檢查程式碼品質（有註解、有說明）
            good_code = sum(1 for block in code_blocks if '#' in block or '"""' in block or '//' in block)
            if good_code >= code_count * 0.7:
                score += 10
                details['code_quality'] = 90
            elif good_code >= code_count * 0.5:
                score += 5
                details['code_quality'] = 70
            else:
                details['code_quality'] = 50
        elif code_count >= 1:
            score += 10
            details['has_code_examples'] = True
            details['code_quality'] = 50

        # 2. 技術深度 (30分)
        # 檢查是否有深入的技術說明
        technical_indicators = [
            r'原理|機制|架構|設計模式',
            r'實作|實現|實施',
            r'優化|改進|最佳實踐',
            r'限制|注意事項|陷阱',
            r'比較|對比|差異'
        ]

        depth_score = 0
        for indicator in technical_indicators:
            if re.search(indicator, content):
                depth_score += 6

        score += min(30, depth_score)
        details['technical_depth'] = min(100, depth_score * 3.3)

        # 3. 理論與實踐平衡 (20分)
        # 檢查是否既有理論說明又有實際範例
        theory_keywords = ['原理', '概念', '定義', '為什麼', '理論']
        practice_keywords = ['如何', '步驟', '範例', '實際', '具體']

        has_theory = any(keyword in content for keyword in theory_keywords)
        has_practice = any(keyword in content for keyword in practice_keywords)

        if has_theory and has_practice:
            score += 20
            details['theory_practice_balance'] = True
        elif has_theory or has_practice:
            score += 10

        # 4. 專業術語 (20分)
        # 檢查是否使用並解釋專業術語
        # 簡化處理：檢查是否有術語並提供說明
        term_explanation_pattern = r'([A-Z]{2,}|[\u4e00-\u9fa5]{2,})\s*[（(].*?[）)]'
        explanations = re.findall(term_explanation_pattern, content)

        if len(explanations) >= 5:
            score += 20
            details['professional_terms'] = explanations[:3]
        elif len(explanations) >= 3:
            score += 15
            details['professional_terms'] = explanations[:2]
        elif len(explanations) >= 1:
            score += 10
            details['professional_terms'] = explanations[:1]

        return min(100, score), details

    def _analyze_authoritativeness(self, content: str) -> Tuple[float, Dict]:
        """
        分析「權威性」維度

        檢查項目：
        - 引用可靠來源
        - 數據支持
        - 引用最新資訊
        - 作者資歷說明
        """
        score = 0.0
        details = {
            'has_citations': False,
            'citation_count': 0,
            'has_data': False,
            'data_count': 0,
            'citations': [],
            'has_author_bio': False
        }

        # 1. 引用來源 (40分)
        # 檢查外部連結和引用
        url_pattern = r'https?://[^\s\)】」]+'
        urls = re.findall(url_pattern, content)

        # 權威來源域名
        authoritative_domains = [
            'github.com', 'docs.', 'arxiv.org', 'wikipedia.org',
            'stackoverflow.com', 'medium.com', 'dev.to',
            'anthropic.com', 'openai.com', 'google.com',
            '\.edu', '\.gov', '\.org'
        ]

        authoritative_count = sum(
            1 for url in urls
            if any(domain in url.lower() for domain in authoritative_domains)
        )

        details['citation_count'] = len(urls)
        details['citations'] = urls[:5]

        if authoritative_count >= 5:
            score += 40
            details['has_citations'] = True
        elif authoritative_count >= 3:
            score += 30
            details['has_citations'] = True
        elif authoritative_count >= 1:
            score += 20
            details['has_citations'] = True
        elif len(urls) >= 3:
            score += 15
            details['has_citations'] = True

        # 2. 數據支持 (30分)
        # 檢查統計數據、百分比、具體數字
        data_patterns = [
            r'\d+%',
            r'\d+倍',
            r'根據.*調查|研究|報告',
            r'數據顯示|統計|指出'
        ]

        data_mentions = sum(len(re.findall(p, content)) for p in data_patterns)
        details['data_count'] = data_mentions

        if data_mentions >= 5:
            score += 30
            details['has_data'] = True
        elif data_mentions >= 3:
            score += 20
            details['has_data'] = True
        elif data_mentions >= 1:
            score += 10
            details['has_data'] = True

        # 3. 時效性 (20分)
        # 檢查是否提到最新年份、版本
        current_year = 2025
        recent_years = [str(year) for year in range(current_year - 2, current_year + 1)]

        has_recent_info = any(year in content for year in recent_years)

        version_pattern = r'v?\d+\.\d+(?:\.\d+)?'
        has_version = bool(re.search(version_pattern, content))

        if has_recent_info and has_version:
            score += 20
        elif has_recent_info or has_version:
            score += 10

        # 4. 作者資歷 (10分)
        # 檢查是否有「關於作者」或作者介紹
        author_patterns = [
            r'關於作者|作者簡介|Author',
            r'我是.*工程師|開發者|專家',
            r'\d+年[經驗|資歷]'
        ]

        if any(re.search(p, content) for p in author_patterns):
            score += 10
            details['has_author_bio'] = True

        return min(100, score), details

    def _analyze_trustworthiness(self, content: str) -> Tuple[float, Dict]:
        """
        分析「可信度」維度

        檢查項目：
        - 資訊透明度（說明限制、不確定性）
        - 避免誇大宣稱
        - 提供多方觀點
        - 更新日期標註
        """
        score = 0.0
        details = {
            'has_limitations': False,
            'avoids_exaggeration': True,
            'has_multiple_perspectives': False,
            'has_update_date': False,
            'warning_phrases': [],
            'exaggeration_phrases': []
        }

        # 1. 透明度 - 說明限制和不確定性 (30分)
        limitation_patterns = [
            r'限制|侷限|不足',
            r'注意|小心|謹慎',
            r'可能|也許|或許',
            r'不一定|未必',
            r'需要.*驗證|確認'
        ]

        limitation_count = sum(len(re.findall(p, content)) for p in limitation_patterns)
        details['warning_phrases'] = re.findall(limitation_patterns[1], content)[:3]

        if limitation_count >= 5:
            score += 30
            details['has_limitations'] = True
        elif limitation_count >= 3:
            score += 20
            details['has_limitations'] = True
        elif limitation_count >= 1:
            score += 10
            details['has_limitations'] = True

        # 2. 避免誇大 (30分)
        exaggeration_patterns = [
            r'最[好|佳|優|強]',
            r'第一|No\.?\s*1',
            r'100%|絕對|一定',
            r'保證|必定|肯定',
            r'完美|無敵|神級'
        ]

        exaggeration_count = sum(len(re.findall(p, content)) for p in exaggeration_patterns)
        details['exaggeration_phrases'] = re.findall('|'.join(exaggeration_patterns), content)[:3]

        if exaggeration_count == 0:
            score += 30
        elif exaggeration_count <= 2:
            score += 20
            details['avoids_exaggeration'] = True
        elif exaggeration_count <= 5:
            score += 10
            details['avoids_exaggeration'] = False
        else:
            details['avoids_exaggeration'] = False

        # 3. 多方觀點 (20分)
        perspective_patterns = [
            r'另一方面|然而|但是',
            r'有人認為|部分.*認為',
            r'優點.*缺點|優勢.*劣勢',
            r'支持者|反對者'
        ]

        perspective_count = sum(len(re.findall(p, content)) for p in perspective_patterns)

        if perspective_count >= 3:
            score += 20
            details['has_multiple_perspectives'] = True
        elif perspective_count >= 1:
            score += 10
            details['has_multiple_perspectives'] = True

        # 4. 更新日期 (20分)
        date_patterns = [
            r'更新.*20\d{2}',
            r'最後更新|Last Updated',
            r'20\d{2}[年-]\d{1,2}[月-]\d{1,2}'
        ]

        if any(re.search(p, content) for p in date_patterns):
            score += 20
            details['has_update_date'] = True

        return min(100, score), details

    def _generate_insights(
        self,
        scores: EEATScore,
        exp_details: Dict,
        exp_details_2: Dict,
        auth_details: Dict,
        trust_details: Dict
    ) -> Tuple[List[str], List[str], List[str]]:
        """生成優點、缺點和建議"""
        strengths = []
        weaknesses = []
        recommendations = []

        # 分析經驗 (Experience)
        if scores.experience >= 75:
            strengths.append(f"✅ 經驗分數優秀 ({scores.experience}/100)：包含豐富的第一人稱真實經驗")
        elif scores.experience < 50:
            weaknesses.append(f"❌ 經驗分數偏低 ({scores.experience}/100)：缺乏真實的個人經驗敘述")
            recommendations.append("💡 增加第一人稱敘述，分享真實使用經驗和具體情境")

        if not exp_details['has_specific_details']:
            recommendations.append("💡 補充具體細節：時間參考、數據、使用情境")

        # 分析專業知識 (Expertise)
        if scores.expertise >= 75:
            strengths.append(f"✅ 專業知識分數優秀 ({scores.expertise}/100)：展現深厚的技術理解")
        elif scores.expertise < 50:
            weaknesses.append(f"❌ 專業知識分數不足 ({scores.expertise}/100)：技術深度有待加強")
            recommendations.append("💡 增加技術深度：原理說明、架構分析、最佳實踐")

        if not exp_details_2['has_code_examples']:
            recommendations.append("💡 添加程式碼範例並附上註解和說明")

        # 分析權威性 (Authoritativeness)
        if scores.authoritativeness >= 75:
            strengths.append(f"✅ 權威性分數優秀 ({scores.authoritativeness}/100)：充分引用可靠來源")
        elif scores.authoritativeness < 50:
            weaknesses.append(f"❌ 權威性分數不足 ({scores.authoritativeness}/100)：缺乏權威來源支持")
            recommendations.append("💡 引用權威來源：官方文件、研究報告、統計數據")

        if auth_details['citation_count'] < 3:
            recommendations.append("💡 增加外部引用連結（建議 3-5 個權威來源）")

        # 分析可信度 (Trustworthiness)
        if scores.trustworthiness >= 75:
            strengths.append(f"✅ 可信度分數優秀 ({scores.trustworthiness}/100)：資訊透明且客觀")
        elif scores.trustworthiness < 50:
            weaknesses.append(f"❌ 可信度分數偏低 ({scores.trustworthiness}/100)：資訊透明度不足")
            recommendations.append("💡 增加透明度：說明限制、標註不確定性、避免絕對化表述")

        if not trust_details['avoids_exaggeration']:
            recommendations.append("⚠️ 避免誇大用詞：移除「最好」「絕對」「保證」等詞彙")

        if not trust_details['has_update_date']:
            recommendations.append("💡 添加更新日期，讓讀者知道資訊時效性")

        # 總分評估
        if scores.overall >= 85:
            strengths.append(f"🎉 E-E-A-T 總分優秀 ({scores.overall}/100)：符合 Google 高品質內容標準")
        elif scores.overall >= 70:
            strengths.append(f"👍 E-E-A-T 總分良好 ({scores.overall}/100)：內容品質達標，仍有提升空間")
        elif scores.overall < 55:
            weaknesses.append(f"⚠️ E-E-A-T 總分需改進 ({scores.overall}/100)：建議優先提升低分項目")

        return strengths, weaknesses, recommendations

    def generate_report(self, result: EEATAnalysisResult, output_path: Optional[str] = None) -> str:
        """
        生成 Markdown 格式的分析報告

        Args:
            result: 分析結果
            output_path: 輸出檔案路徑（可選）

        Returns:
            Markdown 格式的報告內容
        """
        report_lines = []

        # 標題
        report_lines.append("# E-E-A-T 品質分析報告")
        report_lines.append("")
        report_lines.append(f"**分析時間**: {result.analyzed_at}")
        report_lines.append(f"**系統版本**: v1.0.0")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # E-E-A-T 說明
        report_lines.append("## 📖 關於 E-E-A-T")
        report_lines.append("")
        report_lines.append("E-E-A-T 是 Google 評估內容品質的核心標準：")
        report_lines.append("")
        report_lines.append("- **Experience (經驗)**: 作者是否有第一手經驗？")
        report_lines.append("- **Expertise (專業知識)**: 內容是否展現專業深度？")
        report_lines.append("- **Authoritativeness (權威性)**: 作者和來源是否可靠？")
        report_lines.append("- **Trustworthiness (可信度)**: 資訊是否透明且誠實？")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 總分
        report_lines.append("## 📊 E-E-A-T 總分")
        report_lines.append("")
        report_lines.append(f"### {result.scores.overall}/100")
        report_lines.append("")
        report_lines.append(self._get_progress_bar(result.scores.overall))
        report_lines.append("")
        report_lines.append(self._get_score_level(result.scores.overall))
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 各項分數
        report_lines.append("## 📈 各項分數明細")
        report_lines.append("")
        report_lines.append("| 評估項目 | 分數 | 進度 | 狀態 |")
        report_lines.append("|---------|------|------|------|")

        items = [
            ("Experience (經驗)", result.scores.experience),
            ("Expertise (專業知識)", result.scores.expertise),
            ("Authoritativeness (權威性)", result.scores.authoritativeness),
            ("Trustworthiness (可信度)", result.scores.trustworthiness)
        ]

        for name, score in items:
            bar = self._get_mini_progress_bar(score)
            status = self._get_score_emoji(score)
            report_lines.append(f"| {name} | {score}/100 | {bar} | {status} |")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 優點
        if result.strengths:
            report_lines.append("## ✅ 優點")
            report_lines.append("")
            for strength in result.strengths:
                report_lines.append(f"- {strength}")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # 缺點
        if result.weaknesses:
            report_lines.append("## ⚠️ 需要改進")
            report_lines.append("")
            for weakness in result.weaknesses:
                report_lines.append(f"- {weakness}")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # 建議
        if result.recommendations:
            report_lines.append("## 💡 優化建議")
            report_lines.append("")
            for i, rec in enumerate(result.recommendations, 1):
                report_lines.append(f"{i}. {rec}")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # 詳細分析
        report_lines.append("## 🔍 詳細分析")
        report_lines.append("")

        # Experience 詳情
        report_lines.append(f"### Experience (經驗) - {result.scores.experience}/100")
        report_lines.append("")
        exp_d = result.details['experience']
        report_lines.append(f"- 第一人稱敘述: {'✅ 充足' if exp_d['has_first_person'] else '❌ 不足'}")
        report_lines.append(f"- 具體細節: {'✅ 充足' if exp_d['has_specific_details'] else '❌ 不足'}")
        report_lines.append(f"- 個人見解: {'✅ 有' if exp_d['has_personal_insights'] else '❌ 缺乏'}")

        if exp_d['consistent_with_profile'] is not None:
            status = '✅ 一致' if exp_d['consistent_with_profile'] else '⚠️ 需檢查'
            report_lines.append(f"- 與經驗檔案一致性: {status}")

        report_lines.append("")

        # Expertise 詳情
        report_lines.append(f"### Expertise (專業知識) - {result.scores.expertise}/100")
        report_lines.append("")
        exp_d2 = result.details['expertise']
        report_lines.append(f"- 程式碼範例: {'✅ 有' if exp_d2['has_code_examples'] else '❌ 無'}")
        report_lines.append(f"- 程式碼品質: {exp_d2['code_quality']}/100")
        report_lines.append(f"- 技術深度: {exp_d2['technical_depth']}/100")
        report_lines.append(f"- 理論實踐平衡: {'✅ 平衡' if exp_d2['theory_practice_balance'] else '⚠️ 失衡'}")
        report_lines.append("")

        # Authoritativeness 詳情
        report_lines.append(f"### Authoritativeness (權威性) - {result.scores.authoritativeness}/100")
        report_lines.append("")
        auth_d = result.details['authoritativeness']
        report_lines.append(f"- 引用來源: {'✅ 有 (' + str(auth_d['citation_count']) + ' 個)' if auth_d['has_citations'] else '❌ 無'}")
        report_lines.append(f"- 數據支持: {'✅ 有 (' + str(auth_d['data_count']) + ' 處)' if auth_d['has_data'] else '❌ 無'}")
        report_lines.append(f"- 作者簡介: {'✅ 有' if auth_d['has_author_bio'] else '⚠️ 建議補充'}")
        report_lines.append("")

        # Trustworthiness 詳情
        report_lines.append(f"### Trustworthiness (可信度) - {result.scores.trustworthiness}/100")
        report_lines.append("")
        trust_d = result.details['trustworthiness']
        report_lines.append(f"- 說明限制: {'✅ 有' if trust_d['has_limitations'] else '⚠️ 建議補充'}")
        report_lines.append(f"- 避免誇大: {'✅ 良好' if trust_d['avoids_exaggeration'] else '❌ 有誇大用詞'}")
        report_lines.append(f"- 多方觀點: {'✅ 有' if trust_d['has_multiple_perspectives'] else '⚠️ 建議補充'}")
        report_lines.append(f"- 更新日期: {'✅ 有' if trust_d['has_update_date'] else '⚠️ 建議添加'}")
        report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

        # 總結建議
        report_lines.append("## 📋 行動清單")
        report_lines.append("")
        report_lines.append("根據分析結果，建議優先處理：")
        report_lines.append("")

        # 找出得分最低的項目
        scores_dict = {
            'Experience': result.scores.experience,
            'Expertise': result.scores.expertise,
            'Authoritativeness': result.scores.authoritativeness,
            'Trustworthiness': result.scores.trustworthiness
        }
        sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1])

        for i, (name, score) in enumerate(sorted_scores[:2], 1):
            report_lines.append(f"{i}. **提升 {name}** (當前: {score}/100)")

        report_lines.append("")
        report_lines.append("完成這些改進後，預期 E-E-A-T 總分可提升 10-20 分。")
        report_lines.append("")

        # 底部資訊
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("**工具**: E-E-A-T 分析器 v1.0.0")
        report_lines.append("**位置**: `.claude/skills/seo/eeat_analyzer.py`")
        report_lines.append("")

        report = "\n".join(report_lines)

        # 儲存檔案
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 報告已儲存至: {output_path}")

        return report

    def _get_progress_bar(self, score: float, width: int = 40) -> str:
        """生成進度條"""
        filled = int(score / 100 * width)
        bar = '█' * filled + '░' * (width - filled)
        return f"```\n{bar} {score}%\n```"

    def _get_mini_progress_bar(self, score: float, width: int = 10) -> str:
        """生成小型進度條"""
        filled = int(score / 100 * width)
        return '█' * filled + '░' * (width - filled)

    def _get_score_emoji(self, score: float) -> str:
        """根據分數返回表情符號"""
        if score >= 85:
            return "🌟 優秀"
        elif score >= 70:
            return "✅ 良好"
        elif score >= 55:
            return "⚠️ 尚可"
        else:
            return "❌ 需改進"

    def _get_score_level(self, score: float) -> str:
        """根據分數返回評級描述"""
        if score >= 85:
            return "**評級**: 🌟 優秀 - 符合 Google 高品質內容標準，有望獲得較好排名"
        elif score >= 70:
            return "**評級**: ✅ 良好 - 內容品質達標，持續優化可進一步提升"
        elif score >= 55:
            return "**評級**: ⚠️ 尚可 - 基本要素具備，但需要顯著改進"
        else:
            return "**評級**: ❌ 需改進 - E-E-A-T 品質不足，建議重新檢視內容"


def main():
    """命令列介面"""
    parser = argparse.ArgumentParser(
        description='E-E-A-T 內容品質分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 分析文章（顯示於終端）
  python eeat_analyzer.py --article draft_final.md

  # 分析並產生報告
  python eeat_analyzer.py --article draft_final.md --output eeat_report.md

  # 提供經驗檔案以獲得更準確的分析
  python eeat_analyzer.py --article draft_final.md \\
      --experience experience_profile.md --output eeat_report.md

  # JSON 格式輸出
  python eeat_analyzer.py --article draft_final.md --json
        """
    )

    parser.add_argument(
        '--article', '-a',
        required=True,
        help='要分析的文章檔案路徑'
    )

    parser.add_argument(
        '--experience', '-e',
        help='用戶經驗檔案路徑 (experience_profile.md)'
    )

    parser.add_argument(
        '--output', '-o',
        help='輸出報告檔案路徑'
    )

    parser.add_argument(
        '--config', '-c',
        help='配置檔案路徑'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='以 JSON 格式輸出結果'
    )

    args = parser.parse_args()

    # 讀取文章
    try:
        with open(args.article, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 錯誤：找不到文章檔案 {args.article}")
        return 1

    # 初始化分析器
    analyzer = EEATAnalyzer(config_path=args.config)

    # 執行分析
    result = analyzer.analyze(content, experience_profile_path=args.experience)

    # 輸出結果
    if args.json:
        # JSON 格式
        output_data = {
            'scores': result.scores.to_dict(),
            'strengths': result.strengths,
            'weaknesses': result.weaknesses,
            'recommendations': result.recommendations,
            'analyzed_at': result.analyzed_at
        }
        print(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        # Markdown 報告
        report = analyzer.generate_report(result, output_path=args.output)
        if not args.output:
            print(report)

    return 0


if __name__ == '__main__':
    exit(main())
