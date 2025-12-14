#!/usr/bin/env python3
"""
行銷素材生成器 v2.5.0
====================

從文章自動生成行銷素材。

功能：
- 標題變體生成 (20+ 變體)
- Hook 開場白生成
- CTA 按鈕文案
- 縮圖設計建議
- Email 主旨行
- A/B 測試組合

使用方式：
---------
# 生成所有素材
python3 generate.py all --input article.md --output-dir marketing/

# 只生成標題
python3 generate.py headlines --input article.md --count 20

# 生成 A/B 測試組合
python3 generate.py ab-test --input article.md --variants 3
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import random

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from base import BaseSkill, ValidationError
except ImportError:
    class BaseSkill:
        def __init__(self, *args, **kwargs):
            pass
        def read_file(self, path):
            return Path(path).read_text(encoding='utf-8')
        def write_file(self, path, content):
            Path(path).write_text(content, encoding='utf-8')
    class ValidationError(Exception):
        pass


class MarketingAssetsGenerator(BaseSkill):
    """行銷素材生成器"""

    SKILL_NAME = "marketing-assets"
    VERSION = "1.0.0"

    # 標題模板
    HEADLINE_TEMPLATES = {
        'how_to': [
            "如何{action}：{benefit}完整指南",
            "{number}個方法教你{action}",
            "{topic}新手必看：如何{action}",
        ],
        'list': [
            "{number}個{topic}的{type}",
            "{year}年必知的{number}個{topic}趨勢",
            "你不知道的{number}個{topic}秘訣",
        ],
        'question': [
            "為什麼{topic}如此重要？",
            "{topic}真的有效嗎？實測告訴你",
            "你還在為{pain_point}煩惱嗎？",
        ],
        'benefit': [
            "{action}後，我的{metric}提升了{percentage}%",
            "這樣做{topic}，效率翻倍",
            "{benefit}的秘密：{topic}實戰分享",
        ],
        'curiosity': [
            "大多數人不知道的{topic}真相",
            "{topic}：你可能一直做錯了",
            "震驚！{topic}原來要這樣做",
        ],
        'social_proof': [
            "{number}萬人都在用的{topic}方法",
            "專家推薦：{topic}最佳實踐",
            "為什麼{percentage}%的成功者都{action}",
        ]
    }

    # Hook 開場模板
    HOOK_TEMPLATES = [
        "你有沒有想過，{question}",
        "很多人都在問：{question}",
        "我曾經{pain_point}，直到我發現{solution}",
        "如果你正在為{pain_point}煩惱，這篇文章就是為你寫的",
        "想像一下，{desired_outcome}，是什麼感覺？",
        "{statistic}。這個數字可能讓你驚訝",
        "停！在你繼續之前，先問自己：{question}",
    ]

    # CTA 模板
    CTA_TEMPLATES = {
        'soft': [
            "了解更多",
            "繼續閱讀",
            "看看這個",
        ],
        'medium': [
            "立即開始",
            "免費試用",
            "獲取指南",
            "下載資源",
        ],
        'strong': [
            "立即行動",
            "馬上加入",
            "限時免費",
            "不要錯過",
        ],
        'personal': [
            "我要參加",
            "算我一個",
            "帶我去",
            "我準備好了",
        ]
    }

    def _execute(self, input_file: str, asset_type: str = 'all',
                 output_dir: str = None, **kwargs) -> dict:
        """執行素材生成"""
        content = self.read_file(input_file)
        results = {}

        # 提取文章資訊
        article_info = self._analyze_article(content)

        if asset_type in ['all', 'headlines']:
            count = kwargs.get('count', 20)
            results['headlines'] = self._generate_headlines(article_info, count)

        if asset_type in ['all', 'hooks']:
            results['hooks'] = self._generate_hooks(article_info)

        if asset_type in ['all', 'ctas']:
            results['ctas'] = self._generate_ctas(article_info)

        if asset_type in ['all', 'thumbnails']:
            results['thumbnails'] = self._generate_thumbnail_ideas(article_info)

        if asset_type in ['all', 'emails']:
            results['emails'] = self._generate_email_subjects(article_info)

        if asset_type in ['all', 'ab-test']:
            variants = kwargs.get('variants', 3)
            results['ab_tests'] = self._generate_ab_tests(article_info, variants)

        if output_dir:
            self._save_results(results, output_dir, article_info)

        return results

    def _analyze_article(self, content: str) -> dict:
        """分析文章提取關鍵資訊"""
        # 提取標題
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "未知標題"

        # 提取關鍵詞
        words = re.findall(r'[\u4e00-\u9fff]+', content)
        word_freq = {}
        for word in words:
            if len(word) >= 2:
                word_freq[word] = word_freq.get(word, 0) + 1

        keywords = sorted(word_freq.items(), key=lambda x: -x[1])[:10]
        topic = keywords[0][0] if keywords else "主題"

        # 提取數字
        numbers = re.findall(r'\d+', content)
        stats = [n for n in numbers if len(n) >= 2][:5]

        # 識別痛點和好處
        pain_patterns = ['煩惱', '困難', '問題', '挑戰', '不知道', '難以']
        benefit_patterns = ['成功', '提升', '增長', '改善', '優化', '效率']

        pains = []
        benefits = []
        sentences = re.split(r'[。！？]', content)
        for sent in sentences:
            if any(p in sent for p in pain_patterns):
                pains.append(sent.strip()[:50])
            if any(b in sent for b in benefit_patterns):
                benefits.append(sent.strip()[:50])

        return {
            'title': title,
            'topic': topic,
            'keywords': [k[0] for k in keywords],
            'stats': stats,
            'pains': pains[:3],
            'benefits': benefits[:3],
            'word_count': len(content)
        }

    def _generate_headlines(self, info: dict, count: int = 20) -> List[dict]:
        """生成標題變體"""
        headlines = []
        topic = info['topic']
        keywords = info['keywords']

        for category, templates in self.HEADLINE_TEMPLATES.items():
            for template in templates:
                try:
                    headline = template.format(
                        topic=topic,
                        action=f"掌握{topic}",
                        benefit=info['benefits'][0] if info['benefits'] else f"{topic}的好處",
                        number=random.choice(['5', '7', '10', '21']),
                        type=random.choice(['技巧', '方法', '秘訣', '策略']),
                        year='2025',
                        pain_point=info['pains'][0] if info['pains'] else f"{topic}的困擾",
                        metric=random.choice(['效率', '收入', '流量', '轉換率']),
                        percentage=random.choice(['50', '100', '200', '300']),
                        question=f"{topic}為什麼這麼重要",
                        desired_outcome=f"輕鬆掌握{topic}",
                        statistic=f"{random.choice(info['stats'])}%" if info['stats'] else "80%",
                        solution=f"{topic}的解決方案"
                    )
                    headlines.append({
                        'headline': headline,
                        'category': category,
                        'char_count': len(headline)
                    })
                except (KeyError, IndexError):
                    continue

        # 去重並限制數量
        seen = set()
        unique = []
        for h in headlines:
            if h['headline'] not in seen:
                seen.add(h['headline'])
                unique.append(h)

        return unique[:count]

    def _generate_hooks(self, info: dict) -> List[dict]:
        """生成 Hook 開場白"""
        hooks = []
        topic = info['topic']

        for template in self.HOOK_TEMPLATES:
            try:
                hook = template.format(
                    topic=topic,
                    question=f"{topic}到底重不重要",
                    pain_point=info['pains'][0] if info['pains'] else f"不知道如何處理{topic}",
                    solution=f"{topic}的正確方法",
                    desired_outcome=f"完全掌握{topic}",
                    statistic=f"{random.choice(info['stats'])}%" if info['stats'] else "78%的人"
                )
                hooks.append({
                    'hook': hook,
                    'type': 'question' if '?' in template or '？' in template else 'statement',
                    'char_count': len(hook)
                })
            except (KeyError, IndexError):
                continue

        return hooks

    def _generate_ctas(self, info: dict) -> dict:
        """生成 CTA 按鈕文案"""
        result = {}
        for strength, templates in self.CTA_TEMPLATES.items():
            result[strength] = [
                {'text': cta, 'char_count': len(cta)}
                for cta in templates
            ]
        return result

    def _generate_thumbnail_ideas(self, info: dict) -> List[dict]:
        """生成縮圖設計建議"""
        topic = info['topic']
        keywords = info['keywords'][:3]

        ideas = [
            {
                'style': 'text_focused',
                'main_text': info['title'][:20],
                'sub_text': f"完整{topic}指南",
                'colors': ['#FF6B6B', '#4ECDC4'],
                'elements': ['大標題', '漸層背景', '品牌 logo']
            },
            {
                'style': 'number_highlight',
                'main_text': random.choice(['5', '7', '10']),
                'sub_text': f"個{topic}技巧",
                'colors': ['#667EEA', '#764BA2'],
                'elements': ['大數字', '小標題', '圖示']
            },
            {
                'style': 'face_thumbnail',
                'main_text': f"{topic}",
                'sub_text': "你不知道的秘密",
                'colors': ['#F093FB', '#F5576C'],
                'elements': ['人物表情', '驚訝表情', '箭頭指向']
            },
            {
                'style': 'before_after',
                'main_text': "前後對比",
                'sub_text': f"{topic}效果",
                'colors': ['#4CAF50', '#FF5722'],
                'elements': ['分割畫面', '對比圖', '箭頭']
            },
            {
                'style': 'minimal',
                'main_text': info['title'][:15],
                'sub_text': "",
                'colors': ['#000000', '#FFFFFF'],
                'elements': ['純文字', '大量留白', '簡潔設計']
            }
        ]

        return ideas

    def _generate_email_subjects(self, info: dict) -> List[dict]:
        """生成 Email 主旨行"""
        topic = info['topic']

        subjects = [
            f"💡 {topic}完整攻略（免費下載）",
            f"你真的了解{topic}嗎？",
            f"[限時] {topic}速成班開放報名",
            f"關於{topic}，我想說幾句...",
            f"這個{topic}方法改變了一切",
            f"🔥 {topic}最新趨勢報告",
            f"別再犯這個{topic}的錯誤",
            f"3分鐘學會{topic}",
            f"為什麼{topic}這麼重要？",
            f"[獨家] {topic}內部資料首度公開"
        ]

        return [
            {
                'subject': s,
                'char_count': len(s),
                'has_emoji': any(ord(c) > 127 for c in s),
                'type': 'curiosity' if '?' in s else 'benefit'
            }
            for s in subjects
        ]

    def _generate_ab_tests(self, info: dict, variants: int = 3) -> List[dict]:
        """生成 A/B 測試組合"""
        headlines = self._generate_headlines(info, variants * 2)
        hooks = self._generate_hooks(info)[:variants]
        ctas = list(self.CTA_TEMPLATES['medium'])[:variants]

        tests = []
        for i in range(variants):
            tests.append({
                'variant': chr(65 + i),  # A, B, C...
                'headline': headlines[i * 2]['headline'] if i * 2 < len(headlines) else info['title'],
                'hook': hooks[i]['hook'] if i < len(hooks) else hooks[0]['hook'],
                'cta': ctas[i] if i < len(ctas) else ctas[0],
                'test_id': f"test_{datetime.now().strftime('%Y%m%d')}_{i+1}"
            })

        return tests

    def _save_results(self, results: dict, output_dir: str, info: dict) -> None:
        """儲存結果"""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        # 生成 Markdown 報告
        md_content = f"""# 行銷素材報告

**文章**: {info['title']}
**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**主題關鍵詞**: {', '.join(info['keywords'][:5])}

---

## 標題變體 ({len(results.get('headlines', []))} 個)

| # | 標題 | 類型 | 字數 |
|---|------|------|------|
"""
        for i, h in enumerate(results.get('headlines', [])[:20], 1):
            md_content += f"| {i} | {h['headline']} | {h['category']} | {h['char_count']} |\n"

        md_content += "\n## Hook 開場白\n\n"
        for h in results.get('hooks', []):
            md_content += f"- {h['hook']}\n"

        md_content += "\n## CTA 按鈕文案\n\n"
        for strength, ctas in results.get('ctas', {}).items():
            md_content += f"### {strength.upper()}\n"
            for cta in ctas:
                md_content += f"- {cta['text']}\n"

        md_content += "\n## 縮圖設計建議\n\n"
        for idea in results.get('thumbnails', []):
            md_content += f"""
### {idea['style']}
- 主文字: {idea['main_text']}
- 副文字: {idea['sub_text']}
- 配色: {', '.join(idea['colors'])}
- 元素: {', '.join(idea['elements'])}
"""

        md_content += "\n## Email 主旨行\n\n"
        for s in results.get('emails', []):
            emoji = "✅" if s['has_emoji'] else "⬜"
            md_content += f"- {emoji} {s['subject']} ({s['char_count']}字)\n"

        md_content += "\n## A/B 測試組合\n\n"
        for test in results.get('ab_tests', []):
            md_content += f"""
### 變體 {test['variant']}
- 標題: {test['headline']}
- Hook: {test['hook']}
- CTA: {test['cta']}
"""

        self.write_file(str(out_path / "marketing_assets.md"), md_content)

        # 儲存 JSON
        self.write_file(
            str(out_path / "marketing_assets.json"),
            json.dumps(results, ensure_ascii=False, indent=2)
        )


def main():
    parser = argparse.ArgumentParser(description="行銷素材生成器 v2.5.0")

    parser.add_argument('type', nargs='?', default='all',
                        choices=['all', 'headlines', 'hooks', 'ctas',
                                 'thumbnails', 'emails', 'ab-test'],
                        help='素材類型')
    parser.add_argument('--input', '-i', required=True, help='輸入文章路徑')
    parser.add_argument('--output-dir', '-d', help='輸出目錄')
    parser.add_argument('--count', '-c', type=int, default=20, help='標題數量')
    parser.add_argument('--variants', '-v', type=int, default=3, help='A/B 測試變體數')

    args = parser.parse_args()

    generator = MarketingAssetsGenerator()
    results = generator._execute(
        args.input, args.type, args.output_dir,
        count=args.count, variants=args.variants
    )

    if not args.output_dir:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"行銷素材已儲存至: {args.output_dir}")


if __name__ == '__main__':
    main()
