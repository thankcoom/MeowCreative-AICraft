#!/usr/bin/env python3
"""
SEO Analyzer Helper Script
實作 0-100 分的 SEO 評分系統
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
import math


class SEOAnalyzer:
    """SEO 分析器"""

    def __init__(self):
        self.stop_words = {
            '的', '了', '是', '在', '我', '有', '和', '就', '不', '人',
            '都', '一', '一個', '上', '也', '很', '到', '說', '要', '去',
            '你', '會', '著', '沒有', '看', '好', '自己', '這', '那', '個'
        }

    def analyze_article(self, content: str, title: str = None, meta_description: str = None,
                       focus_keyword: str = None) -> Dict:
        """
        完整 SEO 分析

        Args:
            content: 文章內容 (Markdown)
            title: 文章標題
            meta_description: Meta description
            focus_keyword: 目標關鍵字

        Returns:
            完整分析報告
        """
        # 1. 關鍵字優化分析 (25分)
        keyword_score, keyword_details = self._analyze_keywords(content, title, focus_keyword)

        # 2. 內容質量分析 (25分)
        quality_score, quality_details = self._analyze_content_quality(content)

        # 3. 技術 SEO 分析 (25分)
        technical_score, technical_details = self._analyze_technical_seo(
            content, title, meta_description
        )

        # 4. 使用者體驗分析 (25分)
        ux_score, ux_details = self._analyze_user_experience(content)

        # 計算總分
        total_score = keyword_score + quality_score + technical_score + ux_score

        # 生成建議
        recommendations = self._generate_recommendations(
            keyword_details, quality_details, technical_details, ux_details
        )

        return {
            'total_score': round(total_score, 1),
            'breakdown': {
                'keyword_optimization': {
                    'score': round(keyword_score, 1),
                    'max_score': 25,
                    'details': keyword_details
                },
                'content_quality': {
                    'score': round(quality_score, 1),
                    'max_score': 25,
                    'details': quality_details
                },
                'technical_seo': {
                    'score': round(technical_score, 1),
                    'max_score': 25,
                    'details': technical_details
                },
                'user_experience': {
                    'score': round(ux_score, 1),
                    'max_score': 25,
                    'details': ux_details
                }
            },
            'recommendations': recommendations,
            'grade': self._get_grade(total_score)
        }

    def _analyze_keywords(self, content: str, title: str, focus_keyword: str) -> Tuple[float, Dict]:
        """分析關鍵字優化 (25分)"""
        score = 0
        details = {}

        # 提取關鍵字
        if focus_keyword:
            keywords = [focus_keyword.lower()]
        else:
            keywords = self._extract_keywords(content, top_n=5)
            focus_keyword = keywords[0] if keywords else ""

        details['focus_keyword'] = focus_keyword
        details['extracted_keywords'] = keywords[:5]

        # 1. 關鍵字密度 (8分)
        density = self._calculate_keyword_density(content, focus_keyword)
        details['keyword_density'] = f"{density:.2f}%"

        if 1.0 <= density <= 2.0:
            score += 8
            details['density_status'] = 'optimal'
        elif 0.5 <= density < 1.0 or 2.0 < density <= 3.0:
            score += 5
            details['density_status'] = 'acceptable'
        else:
            score += 2
            details['density_status'] = 'needs_improvement'

        # 2. 標題中的關鍵字 (7分)
        if title and focus_keyword.lower() in title.lower():
            score += 7
            details['keyword_in_title'] = True
        else:
            details['keyword_in_title'] = False

        # 3. 首段中的關鍵字 (5分)
        first_para = self._get_first_paragraph(content)
        if focus_keyword.lower() in first_para.lower():
            score += 5
            details['keyword_in_first_para'] = True
        else:
            details['keyword_in_first_para'] = False

        # 4. 小標題中的關鍵字 (5分)
        headings = self._extract_headings(content)
        keywords_in_headings = sum(
            1 for h in headings if focus_keyword.lower() in h.lower()
        )
        details['keyword_in_headings'] = keywords_in_headings

        if keywords_in_headings >= 2:
            score += 5
        elif keywords_in_headings == 1:
            score += 3

        return score, details

    def _analyze_content_quality(self, content: str) -> Tuple[float, Dict]:
        """分析內容質量 (25分)"""
        score = 0
        details = {}

        # 1. 字數 (8分)
        word_count = self._count_chinese_chars(content)
        details['word_count'] = word_count

        if 1500 <= word_count <= 3000:
            score += 8
            details['word_count_status'] = 'optimal'
        elif 1000 <= word_count < 1500 or 3000 < word_count <= 4000:
            score += 5
            details['word_count_status'] = 'acceptable'
        else:
            score += 2
            details['word_count_status'] = 'needs_improvement'

        # 2. 可讀性 (8分)
        readability = self._calculate_readability(content)
        details['readability_score'] = round(readability, 1)

        if readability >= 70:
            score += 8
            details['readability_status'] = 'easy'
        elif readability >= 50:
            score += 5
            details['readability_status'] = 'moderate'
        else:
            score += 3
            details['readability_status'] = 'difficult'

        # 3. 段落結構 (5分)
        paragraphs = self._split_paragraphs(content)
        avg_para_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        details['paragraph_count'] = len(paragraphs)
        details['avg_paragraph_length'] = round(avg_para_length, 1)

        if 30 <= avg_para_length <= 80:
            score += 5
            details['paragraph_structure'] = 'optimal'
        elif 20 <= avg_para_length < 30 or 80 < avg_para_length <= 120:
            score += 3
            details['paragraph_structure'] = 'acceptable'
        else:
            score += 1
            details['paragraph_structure'] = 'needs_improvement'

        # 4. 句子長度 (4分)
        sentences = self._split_sentences(content)
        avg_sentence_length = sum(self._count_chinese_chars(s) for s in sentences) / len(sentences) if sentences else 0
        details['sentence_count'] = len(sentences)
        details['avg_sentence_length'] = round(avg_sentence_length, 1)

        if 15 <= avg_sentence_length <= 25:
            score += 4
            details['sentence_length'] = 'optimal'
        elif 10 <= avg_sentence_length < 15 or 25 < avg_sentence_length <= 35:
            score += 2
            details['sentence_length'] = 'acceptable'
        else:
            details['sentence_length'] = 'needs_improvement'

        return score, details

    def _analyze_technical_seo(self, content: str, title: str, meta_description: str) -> Tuple[float, Dict]:
        """分析技術 SEO (25分)"""
        score = 0
        details = {}

        # 1. 標題標籤 (7分)
        if title:
            title_length = len(title)
            details['title_length'] = title_length

            if 30 <= title_length <= 60:
                score += 7
                details['title_status'] = 'optimal'
            elif 20 <= title_length < 30 or 60 < title_length <= 70:
                score += 4
                details['title_status'] = 'acceptable'
            else:
                score += 1
                details['title_status'] = 'needs_improvement'
        else:
            details['title_status'] = 'missing'

        # 2. Meta Description (6分)
        if meta_description:
            meta_length = len(meta_description)
            details['meta_description_length'] = meta_length

            if 120 <= meta_length <= 160:
                score += 6
                details['meta_description_status'] = 'optimal'
            elif 100 <= meta_length < 120 or 160 < meta_length <= 180:
                score += 3
                details['meta_description_status'] = 'acceptable'
            else:
                score += 1
                details['meta_description_status'] = 'needs_improvement'
        else:
            details['meta_description_status'] = 'missing'

        # 3. 標題階層 (6分)
        headings = self._extract_all_headings(content)
        h1_count = sum(1 for h in headings if h['level'] == 1)
        details['heading_structure'] = {
            'h1_count': h1_count,
            'h2_count': sum(1 for h in headings if h['level'] == 2),
            'h3_count': sum(1 for h in headings if h['level'] == 3)
        }

        if h1_count == 1 and len(headings) >= 3:
            score += 6
            details['heading_hierarchy'] = 'correct'
        elif h1_count == 1:
            score += 3
            details['heading_hierarchy'] = 'minimal'
        else:
            details['heading_hierarchy'] = 'incorrect'

        # 4. 內外部連結 (6分)
        internal_links = self._count_internal_links(content)
        external_links = self._count_external_links(content)
        details['internal_links'] = internal_links
        details['external_links'] = external_links

        link_score = 0
        if 3 <= internal_links <= 8:
            link_score += 3
        elif 1 <= internal_links < 3 or 8 < internal_links <= 12:
            link_score += 2

        if 1 <= external_links <= 3:
            link_score += 3
        elif 3 < external_links <= 5:
            link_score += 2

        score += link_score
        details['link_status'] = 'optimal' if link_score >= 5 else 'needs_improvement'

        return score, details

    def _analyze_user_experience(self, content: str) -> Tuple[float, Dict]:
        """分析使用者體驗 (25分)"""
        score = 0
        details = {}

        # 1. 視覺元素 (8分)
        image_count = self._count_images(content)
        list_count = self._count_lists(content)
        details['image_count'] = image_count
        details['list_count'] = list_count

        if image_count >= 2:
            score += 4
        elif image_count == 1:
            score += 2

        if list_count >= 2:
            score += 4
        elif list_count == 1:
            score += 2

        # 2. 內容組織 (8分)
        headings = self._extract_all_headings(content)
        word_count = self._count_chinese_chars(content)
        words_per_heading = word_count / len(headings) if headings else word_count
        details['words_per_heading'] = round(words_per_heading, 1)

        if 200 <= words_per_heading <= 400:
            score += 8
            details['content_organization'] = 'optimal'
        elif 150 <= words_per_heading < 200 or 400 < words_per_heading <= 600:
            score += 5
            details['content_organization'] = 'acceptable'
        else:
            score += 2
            details['content_organization'] = 'needs_improvement'

        # 3. 掃描友好度 (5分)
        bold_count = len(re.findall(r'\*\*(.+?)\*\*', content))
        details['bold_text_count'] = bold_count

        if bold_count >= 5:
            score += 5
        elif bold_count >= 3:
            score += 3
        else:
            score += 1

        # 4. 多媒體豐富度 (4分)
        has_images = image_count > 0
        has_lists = list_count > 0
        has_bold = bold_count > 0
        diversity_score = sum([has_images, has_lists, has_bold])

        score += diversity_score + 1
        details['multimedia_diversity'] = diversity_score

        return score, details

    def _generate_recommendations(self, keyword_details: Dict, quality_details: Dict,
                                 technical_details: Dict, ux_details: Dict) -> List[Dict]:
        """生成優化建議"""
        recommendations = []

        # 關鍵字建議
        if keyword_details.get('density_status') != 'optimal':
            recommendations.append({
                'priority': 'High',
                'category': 'Keyword Optimization',
                'issue': f"關鍵字密度 {keyword_details.get('keyword_density')} 不在最佳範圍 (1-2%)",
                'solution': '調整關鍵字「' + keyword_details.get('focus_keyword', '') + '」的使用頻率',
                'expected_impact': 'SEO 排名 +10-15%'
            })

        if not keyword_details.get('keyword_in_title'):
            recommendations.append({
                'priority': 'High',
                'category': 'Keyword Optimization',
                'issue': '標題中未包含目標關鍵字',
                'solution': '在標題前半部分加入關鍵字「' + keyword_details.get('focus_keyword', '') + '」',
                'expected_impact': 'CTR +20-30%'
            })

        # 內容質量建議
        if quality_details.get('word_count_status') != 'optimal':
            current_count = quality_details.get('word_count', 0)
            if current_count < 1500:
                recommendations.append({
                    'priority': 'High',
                    'category': 'Content Quality',
                    'issue': f"字數 {current_count} 低於建議範圍 (1500-3000)",
                    'solution': f"增加 {1500 - current_count} 字的深度內容",
                    'expected_impact': '搜尋排名 +15-20%'
                })

        if quality_details.get('readability_status') == 'difficult':
            recommendations.append({
                'priority': 'Medium',
                'category': 'Content Quality',
                'issue': '可讀性偏低',
                'solution': '簡化句子結構，使用更日常的詞彙',
                'expected_impact': '停留時間 +25%'
            })

        # 技術 SEO 建議
        if technical_details.get('meta_description_status') == 'missing':
            recommendations.append({
                'priority': 'High',
                'category': 'Technical SEO',
                'issue': '缺少 Meta Description',
                'solution': '撰寫 120-160 字的吸引人摘要',
                'expected_impact': 'CTR +10-15%'
            })

        if technical_details.get('heading_hierarchy') != 'correct':
            recommendations.append({
                'priority': 'Medium',
                'category': 'Technical SEO',
                'issue': '標題階層結構不正確',
                'solution': '確保只有 1 個 H1，並合理使用 H2-H3',
                'expected_impact': 'SEO 分數 +8-12%'
            })

        # UX 建議
        if ux_details.get('image_count', 0) == 0:
            recommendations.append({
                'priority': 'Medium',
                'category': 'User Experience',
                'issue': '缺少視覺元素',
                'solution': '加入至少 2-3 張相關圖片',
                'expected_impact': '停留時間 +30-40%'
            })

        # 按優先級排序
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))

        return recommendations

    # === 輔助方法 ===

    def _extract_keywords(self, content: str, top_n: int = 5) -> List[str]:
        """提取關鍵字"""
        # 移除標點符號和特殊字元
        clean_content = re.sub(r'[^\w\s]', ' ', content)
        words = clean_content.split()

        # 過濾停用詞和單字詞
        words = [w for w in words if len(w) > 1 and w not in self.stop_words]

        # 統計詞頻
        word_freq = Counter(words)

        # 返回最常見的關鍵字
        return [word for word, _ in word_freq.most_common(top_n)]

    def _calculate_keyword_density(self, content: str, keyword: str) -> float:
        """計算關鍵字密度"""
        if not keyword:
            return 0.0

        total_words = len(content.split())
        keyword_count = content.lower().count(keyword.lower())

        if total_words == 0:
            return 0.0

        return (keyword_count / total_words) * 100

    def _get_first_paragraph(self, content: str) -> str:
        """獲取首段"""
        paragraphs = self._split_paragraphs(content)
        return paragraphs[0] if paragraphs else ""

    def _extract_headings(self, content: str) -> List[str]:
        """提取所有標題"""
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        return headings

    def _extract_all_headings(self, content: str) -> List[Dict]:
        """提取所有標題及其層級"""
        headings = []
        for match in re.finditer(r'^(#+)\s+(.+)$', content, re.MULTILINE):
            headings.append({
                'level': len(match.group(1)),
                'text': match.group(2)
            })
        return headings

    def _count_chinese_chars(self, text: str) -> int:
        """計算中文字數（包含英文單字）"""
        # 計算中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 計算英文單字
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        return chinese_chars + english_words

    def _calculate_readability(self, content: str) -> float:
        """計算可讀性分數 (簡化版)"""
        sentences = self._split_sentences(content)
        if not sentences:
            return 0.0

        total_words = sum(self._count_chinese_chars(s) for s in sentences)
        avg_sentence_length = total_words / len(sentences)

        # 簡化的可讀性公式（分數越高越易讀）
        readability = 100 - (avg_sentence_length * 1.5)
        return max(0, min(100, readability))

    def _split_paragraphs(self, content: str) -> List[str]:
        """分割段落"""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        # 過濾標題
        paragraphs = [p for p in paragraphs if not p.startswith('#')]
        return paragraphs

    def _split_sentences(self, content: str) -> List[str]:
        """分割句子"""
        # 簡化版：按句號、問號、驚嘆號分割
        sentences = re.split(r'[。！？\.\!\?]+', content)
        return [s.strip() for s in sentences if s.strip()]

    def _count_internal_links(self, content: str) -> int:
        """計算內部連結數"""
        # 簡化版：假設相對路徑為內部連結
        return len(re.findall(r'\[.+?\]\(/[^\)]+\)', content))

    def _count_external_links(self, content: str) -> int:
        """計算外部連結數"""
        # 簡化版：假設 http:// 或 https:// 開頭為外部連結
        return len(re.findall(r'\[.+?\]\(https?://[^\)]+\)', content))

    def _count_images(self, content: str) -> int:
        """計算圖片數量"""
        return len(re.findall(r'!\[.*?\]\(.*?\)', content))

    def _count_lists(self, content: str) -> int:
        """計算列表數量"""
        # 計算有序和無序列表
        unordered = len(re.findall(r'^\* .+$', content, re.MULTILINE))
        ordered = len(re.findall(r'^\d+\. .+$', content, re.MULTILINE))
        return (unordered + ordered) // 3  # 假設平均每個列表有 3 項

    def _get_grade(self, score: float) -> str:
        """根據分數獲取等級"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'


def main():
    """命令列介面"""
    if len(sys.argv) < 2:
        print("用法: python analyze.py <markdown_file> [title] [focus_keyword]")
        print("範例: python analyze.py article.md \"文章標題\" \"SEO優化\"")
        sys.exit(1)

    markdown_file = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    focus_keyword = sys.argv[3] if len(sys.argv) > 3 else None

    # 讀取 Markdown 內容
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分析 SEO
    analyzer = SEOAnalyzer()
    result = analyzer.analyze_article(content, title, focus_keyword=focus_keyword)

    # 輸出結果
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
