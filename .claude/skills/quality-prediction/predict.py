#!/usr/bin/env python3
"""
Quality Prediction Skill
預測文章品質分數和評估風險
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class QualityPredictor:
    """品質預測器"""

    def __init__(self):
        self.weights = {
            'eeat': 0.30,
            'seo': 0.25,
            'persuasion': 0.25,
            'engagement': 0.20,
        }

    def extract_features(self, content: str) -> Dict:
        """提取文本特徵"""
        lines = content.split('\n')
        words = content.split()
        sentences = re.split(r'[。！？.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = [p for p in content.split('\n\n') if p.strip()]

        # 標題統計
        h1_count = len(re.findall(r'^# [^#]', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## [^#]', content, re.MULTILINE))
        h3_count = len(re.findall(r'^### [^#]', content, re.MULTILINE))

        # 列表統計
        list_items = len(re.findall(r'^[-*\d]+[.)] ', content, re.MULTILINE))

        # 第一人稱
        first_person = len(re.findall(r'我|我們|我的', content))

        # 問句
        questions = len(re.findall(r'[？?]', content))

        # 數據點
        data_points = len(re.findall(r'\d+[%％]|\d+\s*(個|次|年|天|元|萬|億)', content))

        # 引用來源
        citations = len(re.findall(r'\[.*?\]\(.*?\)|根據|研究顯示|報告指出', content))

        # CTA 檢測
        cta_patterns = r'點擊|立即|馬上|現在|免費|了解更多|開始|試試|加入|訂閱'
        cta_count = len(re.findall(cta_patterns, content))

        # 心理觸發詞
        trigger_words = r'限時|獨家|僅限|最後|立即|緊急|免費|保證|證明|專家'
        trigger_count = len(re.findall(trigger_words, content))

        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'avg_paragraph_length': len(words) / max(len(paragraphs), 1),
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'total_headings': h1_count + h2_count + h3_count,
            'list_items': list_items,
            'first_person_usage': first_person,
            'question_count': questions,
            'data_points': data_points,
            'citations': citations,
            'cta_count': cta_count,
            'trigger_words': trigger_count,
        }

    def predict_eeat(self, features: Dict) -> Dict:
        """預測 E-E-A-T 分數"""
        # Experience - 基於第一人稱和具體細節
        experience = min(100, 50 + features['first_person_usage'] * 3 + features['data_points'] * 2)

        # Expertise - 基於深度和結構
        expertise = min(100, 50 + features['total_headings'] * 5 + features['word_count'] // 100)

        # Authoritativeness - 基於引用和數據
        authority = min(100, 40 + features['citations'] * 8 + features['data_points'] * 3)

        # Trustworthiness - 綜合考量
        trust = min(100, 50 + features['citations'] * 5 + features['question_count'] * 2)

        overall = (experience + expertise + authority + trust) / 4

        return {
            'score': int(overall),
            'confidence': 0.85,
            'components': {
                'experience': int(experience),
                'expertise': int(expertise),
                'authoritativeness': int(authority),
                'trustworthiness': int(trust),
            }
        }

    def predict_seo(self, features: Dict) -> Dict:
        """預測 SEO 分數"""
        score = 50

        # 標題結構
        if features['h1_count'] == 1:
            score += 10
        if features['h2_count'] >= 3:
            score += 10
        if features['h3_count'] >= 2:
            score += 5

        # 內容長度
        if features['word_count'] >= 1500:
            score += 10
        elif features['word_count'] >= 1000:
            score += 5

        # 列表使用
        if features['list_items'] >= 3:
            score += 5

        # 段落長度適中
        if 50 <= features['avg_paragraph_length'] <= 150:
            score += 5

        # 句子長度適中
        if 10 <= features['avg_sentence_length'] <= 25:
            score += 5

        return {
            'score': min(100, score),
            'confidence': 0.88,
        }

    def predict_persuasion(self, features: Dict) -> Dict:
        """預測說服力分數"""
        score = 40

        # CTA
        if features['cta_count'] >= 3:
            score += 20
        elif features['cta_count'] >= 2:
            score += 15
        elif features['cta_count'] >= 1:
            score += 10

        # 心理觸發
        if features['trigger_words'] >= 5:
            score += 20
        elif features['trigger_words'] >= 3:
            score += 15
        elif features['trigger_words'] >= 1:
            score += 10

        # 問句（引發思考）
        if features['question_count'] >= 3:
            score += 10
        elif features['question_count'] >= 1:
            score += 5

        # 數據支持
        if features['data_points'] >= 3:
            score += 10

        return {
            'score': min(100, score),
            'confidence': 0.82,
        }

    def predict_engagement(self, features: Dict) -> Dict:
        """預測參與度分數"""
        score = 50

        # 開頭問句 (假設問句在前面表示好的開頭)
        if features['question_count'] >= 1:
            score += 10

        # 第一人稱（連結感）
        if features['first_person_usage'] >= 5:
            score += 10
        elif features['first_person_usage'] >= 2:
            score += 5

        # 結構清晰
        if features['total_headings'] >= 5:
            score += 10

        # 列表（易讀性）
        if features['list_items'] >= 5:
            score += 10
        elif features['list_items'] >= 2:
            score += 5

        # 適當長度
        if 1500 <= features['word_count'] <= 3000:
            score += 10

        return {
            'score': min(100, score),
            'confidence': 0.80,
        }

    def assess_risks(self, features: Dict) -> List[Dict]:
        """評估風險"""
        risks = []

        # 說服力風險
        if features['cta_count'] < 2 or features['trigger_words'] < 3:
            probability = 0.65 if features['cta_count'] < 1 else 0.45
            risks.append({
                'type': 'persuasion_risk',
                'severity': 'high',
                'probability': probability,
                'description': '說服力元素不足',
                'indicators': [
                    f"CTA 僅出現 {features['cta_count']} 次",
                    f"心理觸發詞 {features['trigger_words']} 個",
                ],
                'recommendation': '強化執行 Phase 3.8'
            })

        # 參與度風險
        if features['question_count'] < 1 or features['first_person_usage'] < 2:
            risks.append({
                'type': 'engagement_risk',
                'severity': 'medium',
                'probability': 0.45,
                'description': '開頭吸引力可能不足',
                'indicators': [
                    f"問句數量: {features['question_count']}",
                    f"第一人稱使用: {features['first_person_usage']}",
                ],
                'recommendation': '添加開場問句和個人化語氣'
            })

        # AI 偵測風險 - 基於變異度
        if features['avg_sentence_length'] > 20 and features['first_person_usage'] < 3:
            risks.append({
                'type': 'ai_detection_risk',
                'severity': 'medium',
                'probability': 0.35,
                'description': 'AI 痕跡風險',
                'indicators': [
                    '句子長度較一致',
                    '個人化語氣不足',
                ],
                'recommendation': '執行 Phase 3.7 Humanizer'
            })

        # SEO 風險
        if features['h1_count'] != 1 or features['h2_count'] < 3:
            risks.append({
                'type': 'seo_risk',
                'severity': 'medium',
                'probability': 0.40,
                'description': 'SEO 結構風險',
                'indicators': [
                    f"H1 數量: {features['h1_count']}",
                    f"H2 數量: {features['h2_count']}",
                ],
                'recommendation': '優化標題結構'
            })

        # 可信度風險
        if features['citations'] < 2:
            risks.append({
                'type': 'credibility_risk',
                'severity': 'medium',
                'probability': 0.50,
                'description': '可信度支撐不足',
                'indicators': [
                    f"引用來源: {features['citations']} 處",
                ],
                'recommendation': '增加引用和數據支持'
            })

        return risks

    def predict(self, content: str) -> Dict:
        """完整預測"""
        features = self.extract_features(content)

        eeat = self.predict_eeat(features)
        seo = self.predict_seo(features)
        persuasion = self.predict_persuasion(features)
        engagement = self.predict_engagement(features)

        # 計算綜合分數
        overall_score = (
            eeat['score'] * self.weights['eeat'] +
            seo['score'] * self.weights['seo'] +
            persuasion['score'] * self.weights['persuasion'] +
            engagement['score'] * self.weights['engagement']
        )

        overall_confidence = (
            eeat['confidence'] * self.weights['eeat'] +
            seo['confidence'] * self.weights['seo'] +
            persuasion['confidence'] * self.weights['persuasion'] +
            engagement['confidence'] * self.weights['engagement']
        )

        # 決定評級
        if overall_score >= 90:
            grade = 'A+'
        elif overall_score >= 85:
            grade = 'A'
        elif overall_score >= 80:
            grade = 'B+'
        elif overall_score >= 75:
            grade = 'B'
        elif overall_score >= 70:
            grade = 'C+'
        elif overall_score >= 65:
            grade = 'C'
        else:
            grade = 'D'

        # 決定執行路徑
        if overall_score >= 85:
            recommendation = 'high_quality_path'
        elif overall_score >= 70:
            recommendation = 'standard_path'
        else:
            recommendation = 'improvement_needed'

        # 評估風險
        risks = self.assess_risks(features)

        return {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'predictions': {
                'eeat': eeat,
                'seo': seo,
                'persuasion': persuasion,
                'engagement': engagement,
                'overall': {
                    'score': int(overall_score),
                    'confidence': round(overall_confidence, 2),
                    'grade': grade,
                }
            },
            'risks': risks,
            'execution_recommendation': recommendation,
        }

    def generate_report(self, prediction: Dict, file_path: str) -> str:
        """生成預測報告"""
        pred = prediction['predictions']
        risks = prediction['risks']

        report = f"""# 品質預測報告

**文章**: {file_path}
**預測時間**: {prediction['timestamp'][:19]}
**預測信心度**: {pred['overall']['confidence']*100:.0f}%

## 分數預測

| 維度 | 預測分數 | 信心度 | 狀態 |
|------|----------|--------|------|
| E-E-A-T | {pred['eeat']['score']}/100 | {pred['eeat']['confidence']*100:.0f}% | {'✅' if pred['eeat']['score'] >= 75 else '⚠️'} |
| SEO | {pred['seo']['score']}/100 | {pred['seo']['confidence']*100:.0f}% | {'✅' if pred['seo']['score'] >= 75 else '⚠️'} |
| 說服力 | {pred['persuasion']['score']}/100 | {pred['persuasion']['confidence']*100:.0f}% | {'✅' if pred['persuasion']['score'] >= 75 else '⚠️'} |
| 參與度 | {pred['engagement']['score']}/100 | {pred['engagement']['confidence']*100:.0f}% | {'✅' if pred['engagement']['score'] >= 75 else '⚠️'} |
| **綜合** | **{pred['overall']['score']}/100** | **{pred['overall']['confidence']*100:.0f}%** | **{pred['overall']['grade']}** |

## E-E-A-T 細項

| 維度 | 分數 |
|------|------|
| Experience (經驗) | {pred['eeat']['components']['experience']}/100 |
| Expertise (專業) | {pred['eeat']['components']['expertise']}/100 |
| Authoritativeness (權威) | {pred['eeat']['components']['authoritativeness']}/100 |
| Trustworthiness (可信) | {pred['eeat']['components']['trustworthiness']}/100 |

## 風險評估

"""
        if risks:
            report += "| 風險類型 | 嚴重度 | 機率 | 狀態 |\n"
            report += "|----------|--------|------|------|\n"
            for risk in risks:
                status = "⚠️ 需處理" if risk['severity'] == 'high' else "⚠️ 建議改善"
                report += f"| {risk['description']} | {risk['severity']} | {risk['probability']*100:.0f}% | {status} |\n"

            report += "\n### 風險詳情\n\n"
            for risk in risks:
                report += f"**{risk['type'].replace('_', ' ').title()}**\n"
                report += f"- 嚴重度: {risk['severity']}\n"
                report += f"- 指標: {', '.join(risk['indicators'])}\n"
                report += f"- 建議: {risk['recommendation']}\n\n"
        else:
            report += "✅ 未發現顯著風險\n"

        # 執行建議
        rec = prediction['execution_recommendation']
        if rec == 'high_quality_path':
            rec_text = "高品質路徑 - 可跳過部分強化 Phase"
        elif rec == 'standard_path':
            rec_text = "標準路徑 - 執行完整流程"
        else:
            rec_text = "改進路徑 - 需要額外強化"

        report += f"""
## 執行建議

**推薦路徑**: {rec_text}

"""
        if rec == 'high_quality_path':
            report += "- ⏭️ 可跳過 Phase 3.9 (如非故事型文章)\n"
            report += "- ✅ 正常執行其他 Phase\n"
        elif rec == 'standard_path':
            # 根據風險決定重點
            high_risks = [r for r in risks if r['severity'] == 'high']
            if high_risks:
                report += f"- ⭐ 重點執行: {high_risks[0]['recommendation']}\n"
            report += "- ✅ 執行完整強化流程\n"
        else:
            report += "- ⚠️ 建議返回 Writer Agent 修改\n"
            report += "- 或增加額外強化 Phase\n"

        report += f"""
---
*預測模型版本: 1.0.0*
*報告生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report

    def suggest_improvements(self, prediction: Dict, target_score: int) -> List[Dict]:
        """生成改進建議"""
        current = prediction['predictions']['overall']['score']
        gap = target_score - current
        suggestions = []

        if gap <= 0:
            return [{
                'type': 'none',
                'description': f'當前預測分數 ({current}) 已達到或超過目標 ({target_score})',
                'priority': 'low'
            }]

        pred = prediction['predictions']

        # 找出最弱的維度
        scores = {
            'eeat': pred['eeat']['score'],
            'seo': pred['seo']['score'],
            'persuasion': pred['persuasion']['score'],
            'engagement': pred['engagement']['score'],
        }

        sorted_scores = sorted(scores.items(), key=lambda x: x[1])

        for dim, score in sorted_scores[:2]:
            if dim == 'persuasion':
                suggestions.append({
                    'type': 'persuasion_enhancement',
                    'description': '強化說服力元素',
                    'actions': [
                        '增加 2-3 個明確的 CTA',
                        '添加心理觸發詞（限時、獨家、免費等）',
                        '增加社會證明和數據支持'
                    ],
                    'expected_gain': 10,
                    'priority': 'high'
                })
            elif dim == 'engagement':
                suggestions.append({
                    'type': 'engagement_enhancement',
                    'description': '提升讀者參與度',
                    'actions': [
                        '添加開場問句引發共鳴',
                        '增加第一人稱使用，建立連結',
                        '添加互動元素或行動清單'
                    ],
                    'expected_gain': 8,
                    'priority': 'high'
                })
            elif dim == 'eeat':
                suggestions.append({
                    'type': 'eeat_enhancement',
                    'description': '提升 E-E-A-T 分數',
                    'actions': [
                        '增加引用來源和數據支持',
                        '添加更多個人經驗描述',
                        '補充專家觀點或研究引用'
                    ],
                    'expected_gain': 8,
                    'priority': 'medium'
                })
            elif dim == 'seo':
                suggestions.append({
                    'type': 'seo_enhancement',
                    'description': '優化 SEO 結構',
                    'actions': [
                        '確保只有一個 H1 標題',
                        '增加 H2/H3 子標題結構',
                        '優化段落長度和列表使用'
                    ],
                    'expected_gain': 7,
                    'priority': 'medium'
                })

        return suggestions


def main():
    parser = argparse.ArgumentParser(description='Quality Prediction Skill')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # score
    score_parser = subparsers.add_parser('score', help='預測品質分數')
    score_parser.add_argument('file', help='文章檔案路徑')
    score_parser.add_argument('--output', help='輸出 JSON 路徑')

    # risk
    risk_parser = subparsers.add_parser('risk', help='評估風險')
    risk_parser.add_argument('file', help='文章檔案路徑')
    risk_parser.add_argument('--output', help='輸出報告路徑')

    # suggest
    suggest_parser = subparsers.add_parser('suggest', help='獲取改進建議')
    suggest_parser.add_argument('file', help='文章檔案路徑')
    suggest_parser.add_argument('--target-score', type=int, default=85, help='目標分數')

    # trend
    trend_parser = subparsers.add_parser('trend', help='歷史趨勢分析')
    trend_parser.add_argument('--sessions', type=int, default=10, help='分析的 session 數量')
    trend_parser.add_argument('--output', help='輸出報告路徑')

    # full
    full_parser = subparsers.add_parser('full', help='完整預測報告')
    full_parser.add_argument('file', help='文章檔案路徑')
    full_parser.add_argument('--output', help='輸出報告路徑')

    args = parser.parse_args()
    predictor = QualityPredictor()

    if args.command in ['score', 'risk', 'suggest', 'full']:
        # 讀取文章
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ 檔案不存在: {args.file}")
            sys.exit(1)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        prediction = predictor.predict(content)

    if args.command == 'score':
        pred = prediction['predictions']
        print(f"品質預測結果 ({args.file}):\n")
        print(f"  E-E-A-T:   {pred['eeat']['score']}/100")
        print(f"  SEO:       {pred['seo']['score']}/100")
        print(f"  說服力:    {pred['persuasion']['score']}/100")
        print(f"  參與度:    {pred['engagement']['score']}/100")
        print(f"  ─────────────────")
        print(f"  綜合分數:  {pred['overall']['score']}/100 ({pred['overall']['grade']})")
        print(f"  信心度:    {pred['overall']['confidence']*100:.0f}%")
        print(f"\n執行建議: {prediction['execution_recommendation']}")

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(prediction, f, indent=2, ensure_ascii=False)
            print(f"\n已保存至: {args.output}")

    elif args.command == 'risk':
        risks = prediction['risks']
        print(f"風險評估 ({args.file}):\n")

        if risks:
            for risk in risks:
                severity_icon = "🔴" if risk['severity'] == 'high' else "🟡"
                print(f"{severity_icon} {risk['description']}")
                print(f"   嚴重度: {risk['severity']}, 機率: {risk['probability']*100:.0f}%")
                print(f"   建議: {risk['recommendation']}\n")
        else:
            print("✅ 未發現顯著風險")

        if args.output:
            report = predictor.generate_report(prediction, args.file)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n報告已保存至: {args.output}")

    elif args.command == 'suggest':
        suggestions = predictor.suggest_improvements(prediction, args.target_score)

        current = prediction['predictions']['overall']['score']
        print(f"改進建議 (當前: {current}, 目標: {args.target_score}):\n")

        for i, sug in enumerate(suggestions, 1):
            print(f"{i}. {sug['description']} (預期提升: +{sug.get('expected_gain', 'N/A')})")
            if 'actions' in sug:
                for action in sug['actions']:
                    print(f"   - {action}")
            print()

    elif args.command == 'trend':
        print(f"歷史趨勢分析 (最近 {args.sessions} 個 sessions):")
        print("\n⚠️ 此功能需要累積歷史數據後才能提供分析")
        print("建議: 執行更多 sessions 後再查看趨勢")

    elif args.command == 'full':
        report = predictor.generate_report(prediction, args.file)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 完整報告已保存至: {args.output}")
        else:
            print(report)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
