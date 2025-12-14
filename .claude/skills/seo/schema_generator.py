#!/usr/bin/env python3
"""
Schema.org Markup Generator
為文章生成結構化數據標記，提升 AI Overviews 和 Featured Snippets 的可見度

支援的 Schema 類型：
- Article (文章)
- FAQPage (常見問題)
- HowTo (操作指南)
- BreadcrumbList (麵包屑導航)

Version: 1.0.0
Date: 2025-11-04
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SchemaMarkup:
    """Schema markup 數據結構"""
    schema_type: str  # Article, FAQPage, HowTo, BreadcrumbList
    json_ld: Dict[str, Any]  # JSON-LD 格式
    validation_status: str  # valid, warning, invalid
    issues: List[str]  # 驗證問題


class SchemaGenerator:
    """Schema.org 標記生成器"""

    def __init__(self):
        self.context = "https://schema.org"

    def generate_article_schema(
        self,
        title: str,
        description: str,
        author: str,
        date_published: str,
        date_modified: Optional[str] = None,
        image_url: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        article_body: Optional[str] = None
    ) -> SchemaMarkup:
        """
        生成 Article Schema
        適用於：部落格文章、新聞、教學文章

        Args:
            title: 文章標題
            description: 文章描述
            author: 作者名稱
            date_published: 發布日期 (YYYY-MM-DD)
            date_modified: 修改日期 (可選)
            image_url: 特色圖片 URL (可選)
            keywords: 關鍵字列表 (可選)
            article_body: 文章內容 (可選，用於驗證)

        Returns:
            SchemaMarkup: Article schema 標記
        """
        schema = {
            "@context": self.context,
            "@type": "Article",
            "headline": title,
            "description": description,
            "author": {
                "@type": "Person",
                "name": author
            },
            "datePublished": date_published
        }

        # 可選欄位
        if date_modified:
            schema["dateModified"] = date_modified
        else:
            schema["dateModified"] = date_published  # Google 建議提供

        if image_url:
            schema["image"] = image_url

        if keywords:
            schema["keywords"] = ", ".join(keywords)

        # 驗證
        issues = []
        if len(title) > 110:
            issues.append("標題過長（建議 <= 110 字元）")

        if len(description) > 160:
            issues.append("描述過長（建議 <= 160 字元）")

        if not image_url:
            issues.append("建議提供 image URL 以提升可見度")

        validation_status = "valid" if not issues else "warning"

        return SchemaMarkup(
            schema_type="Article",
            json_ld=schema,
            validation_status=validation_status,
            issues=issues
        )

    def generate_faq_schema(
        self,
        faq_list: List[Dict[str, str]]
    ) -> SchemaMarkup:
        """
        生成 FAQPage Schema
        適用於：FAQ 頁面、問答式內容

        非常適合 AI Overviews，因為 AI 偏好問答格式

        Args:
            faq_list: FAQ 列表，每項包含 'question' 和 'answer'
                      例如: [{"question": "什麼是...", "answer": "..."}]

        Returns:
            SchemaMarkup: FAQPage schema 標記
        """
        main_entity = []

        for faq in faq_list:
            if 'question' not in faq or 'answer' not in faq:
                continue

            main_entity.append({
                "@type": "Question",
                "name": faq['question'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq['answer']
                }
            })

        schema = {
            "@context": self.context,
            "@type": "FAQPage",
            "mainEntity": main_entity
        }

        # 驗證
        issues = []
        if len(main_entity) < 2:
            issues.append("FAQ 項目太少（建議至少 2 個）")

        if len(main_entity) > 10:
            issues.append("FAQ 項目過多（建議 <= 10 個）")

        # 檢查答案長度
        for i, faq in enumerate(main_entity, 1):
            answer_text = faq['acceptedAnswer']['text']
            if len(answer_text) < 20:
                issues.append(f"FAQ {i} 答案太短（建議 >= 20 字）")

        validation_status = "valid" if len(issues) <= 1 else "warning"

        return SchemaMarkup(
            schema_type="FAQPage",
            json_ld=schema,
            validation_status=validation_status,
            issues=issues
        )

    def generate_howto_schema(
        self,
        title: str,
        description: str,
        steps: List[Dict[str, str]],
        total_time: Optional[str] = None,
        tools: Optional[List[str]] = None,
        supply: Optional[List[str]] = None
    ) -> SchemaMarkup:
        """
        生成 HowTo Schema
        適用於：教學文章、操作指南、步驟說明

        AI Overviews 高度重視此類結構化內容

        Args:
            title: 教學標題
            description: 教學描述
            steps: 步驟列表，每項包含 'name' 和 'text'
                   例如: [{"name": "步驟 1", "text": "詳細說明..."}]
            total_time: 總耗時 (可選，格式: PT30M 表示 30 分鐘)
            tools: 需要的工具列表 (可選)
            supply: 需要的材料列表 (可選)

        Returns:
            SchemaMarkup: HowTo schema 標記
        """
        step_entities = []

        for i, step in enumerate(steps, 1):
            step_entity = {
                "@type": "HowToStep",
                "position": i,
                "name": step.get('name', f"步驟 {i}"),
                "text": step.get('text', '')
            }

            # 可選：加入圖片
            if 'image' in step:
                step_entity["image"] = step['image']

            step_entities.append(step_entity)

        schema = {
            "@context": self.context,
            "@type": "HowTo",
            "name": title,
            "description": description,
            "step": step_entities
        }

        # 可選欄位
        if total_time:
            schema["totalTime"] = total_time

        if tools:
            schema["tool"] = [{"@type": "HowToTool", "name": tool} for tool in tools]

        if supply:
            schema["supply"] = [{"@type": "HowToSupply", "name": item} for item in supply]

        # 驗證
        issues = []
        if len(step_entities) < 2:
            issues.append("步驟太少（建議至少 2 個步驟）")

        if len(step_entities) > 20:
            issues.append("步驟過多（建議 <= 20 個步驟）")

        # 檢查步驟描述長度
        for i, step in enumerate(step_entities, 1):
            if len(step['text']) < 20:
                issues.append(f"步驟 {i} 說明太短（建議 >= 20 字）")

        validation_status = "valid" if not issues else "warning"

        return SchemaMarkup(
            schema_type="HowTo",
            json_ld=schema,
            validation_status=validation_status,
            issues=issues
        )

    def generate_breadcrumb_schema(
        self,
        breadcrumbs: List[Dict[str, str]]
    ) -> SchemaMarkup:
        """
        生成 BreadcrumbList Schema
        適用於：網站導航結構

        Args:
            breadcrumbs: 麵包屑列表，每項包含 'name' 和 'url'
                        例如: [{"name": "首頁", "url": "https://..."}]

        Returns:
            SchemaMarkup: BreadcrumbList schema 標記
        """
        list_items = []

        for i, crumb in enumerate(breadcrumbs, 1):
            list_items.append({
                "@type": "ListItem",
                "position": i,
                "name": crumb['name'],
                "item": crumb['url']
            })

        schema = {
            "@context": self.context,
            "@type": "BreadcrumbList",
            "itemListElement": list_items
        }

        # 驗證
        issues = []
        if len(list_items) < 2:
            issues.append("麵包屑層級太少（建議至少 2 層）")

        validation_status = "valid" if not issues else "warning"

        return SchemaMarkup(
            schema_type="BreadcrumbList",
            json_ld=schema,
            validation_status=validation_status,
            issues=issues
        )

    def extract_faq_from_article(self, article_content: str) -> List[Dict[str, str]]:
        """
        從文章中自動提取 FAQ 項目

        檢測模式：
        - Q: ... / A: ...
        - Q. ... / A. ...
        - **問題**: ... / **答案**: ...
        - ## 什麼是... / 段落內容

        Args:
            article_content: 文章內容

        Returns:
            List[Dict]: FAQ 項目列表
        """
        faq_list = []

        # 模式 1: Q: ... A: ...
        qa_pattern = r'Q[:：]\s*(.+?)\s*(?:\n|$)\s*A[:：]\s*(.+?)(?:\n\n|\n(?=[QA][:：])|$)'
        matches = re.finditer(qa_pattern, article_content, re.DOTALL)
        for match in matches:
            question = match.group(1).strip()
            answer = match.group(2).strip()
            faq_list.append({"question": question, "answer": answer})

        # 模式 2: **問**: ... **答**: ...
        qa_bold_pattern = r'\*\*問[題]?[:：]?\*\*\s*(.+?)\s*(?:\n|$)\s*\*\*答[:：]?\*\*\s*(.+?)(?:\n\n|$)'
        matches = re.finditer(qa_bold_pattern, article_content, re.DOTALL)
        for match in matches:
            question = match.group(1).strip()
            answer = match.group(2).strip()
            faq_list.append({"question": question, "answer": answer})

        # 模式 3: ### 什麼是... / ## 如何... (H2/H3 標題作為問題)
        h_pattern = r'^(#{2,3})\s+(.+?[？?])$\n\n(.+?)(?=\n#{2,3}|\Z)'
        matches = re.finditer(h_pattern, article_content, re.MULTILINE | re.DOTALL)
        for match in matches:
            question = match.group(2).strip()
            # 提取第一段作為答案
            answer_text = match.group(3).strip()
            # 取第一段
            first_para = answer_text.split('\n\n')[0]
            # 清理 markdown
            first_para = re.sub(r'\*\*(.+?)\*\*', r'\1', first_para)
            first_para = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', first_para)

            if len(first_para) >= 20:
                faq_list.append({"question": question, "answer": first_para})

        return faq_list

    def extract_howto_from_article(self, article_content: str) -> Optional[List[Dict[str, str]]]:
        """
        從文章中自動提取 HowTo 步驟

        檢測模式：
        - ## 步驟 1: ...
        - ### 1. ...
        - 編號列表

        Args:
            article_content: 文章內容

        Returns:
            List[Dict] | None: 步驟列表，如果沒有檢測到返回 None
        """
        steps = []

        # 模式 1: ## 步驟 N: ...
        step_h_pattern = r'^#{2,3}\s+(?:步驟\s*)?(\d+)[:：.、]\s*(.+?)$\n\n(.+?)(?=\n#{2,3}|\Z)'
        matches = re.finditer(step_h_pattern, article_content, re.MULTILINE | re.DOTALL)

        for match in matches:
            step_num = match.group(1)
            step_name = match.group(2).strip()
            step_text = match.group(3).strip()

            # 取第一段作為描述
            first_para = step_text.split('\n\n')[0]
            # 清理 markdown
            first_para = re.sub(r'\*\*(.+?)\*\*', r'\1', first_para)

            steps.append({
                "name": f"步驟 {step_num}: {step_name}",
                "text": first_para
            })

        # 如果沒有找到標題格式的步驟，嘗試編號列表
        if not steps:
            list_pattern = r'^\d+\.\s+(.+?)$'
            matches = re.finditer(list_pattern, article_content, re.MULTILINE)

            for match in matches:
                step_text = match.group(1).strip()
                if len(step_text) >= 10:  # 過濾太短的
                    steps.append({
                        "name": step_text[:30] + "..." if len(step_text) > 30 else step_text,
                        "text": step_text
                    })

        # 如果步驟太少，返回 None
        if len(steps) < 2:
            return None

        return steps

    def generate_from_article(
        self,
        article_path: str,
        base_url: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[SchemaMarkup]:
        """
        從文章自動生成所有適用的 Schema markups

        Args:
            article_path: 文章檔案路徑
            base_url: 網站基礎 URL (用於 breadcrumb)
            category: 文章分類 (用於 breadcrumb)

        Returns:
            List[SchemaMarkup]: 所有生成的 schema markups
        """
        schemas = []

        # 讀取文章
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析 frontmatter
        frontmatter = self._extract_frontmatter(content)
        article_body = self._remove_frontmatter(content)

        # 1. 總是生成 Article Schema
        article_schema = self.generate_article_schema(
            title=frontmatter.get('title', '未命名文章'),
            description=frontmatter.get('meta_description', frontmatter.get('description', '')),
            author=frontmatter.get('author', '未知作者'),
            date_published=frontmatter.get('date', datetime.now().strftime('%Y-%m-%d')),
            date_modified=frontmatter.get('date_modified'),
            image_url=frontmatter.get('og_image', frontmatter.get('image')),
            keywords=frontmatter.get('keywords', []),
            article_body=article_body
        )
        schemas.append(article_schema)

        # 2. 嘗試生成 FAQ Schema
        faq_list = self.extract_faq_from_article(article_body)
        if len(faq_list) >= 2:
            faq_schema = self.generate_faq_schema(faq_list)
            schemas.append(faq_schema)

        # 3. 嘗試生成 HowTo Schema
        steps = self.extract_howto_from_article(article_body)
        if steps and len(steps) >= 2:
            howto_schema = self.generate_howto_schema(
                title=frontmatter.get('title', '操作指南'),
                description=frontmatter.get('meta_description', ''),
                steps=steps
            )
            schemas.append(howto_schema)

        # 4. 生成 Breadcrumb Schema (如果有 base_url)
        if base_url:
            breadcrumbs = [
                {"name": "首頁", "url": base_url}
            ]
            if category:
                breadcrumbs.append({
                    "name": category,
                    "url": f"{base_url}/category/{category.lower()}"
                })
            breadcrumbs.append({
                "name": frontmatter.get('title', '文章'),
                "url": f"{base_url}/article/{Path(article_path).stem}"
            })

            breadcrumb_schema = self.generate_breadcrumb_schema(breadcrumbs)
            schemas.append(breadcrumb_schema)

        return schemas

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """從文章提取 frontmatter"""
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return {}

        fm_text = match.group(1)
        frontmatter = {}

        # 簡單 YAML 解析（僅處理基本鍵值對和列表）
        for line in fm_text.split('\n'):
            if ':' not in line:
                continue

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')

            # 處理列表
            if value.startswith('['):
                value = [v.strip().strip('"\'') for v in value.strip('[]').split(',')]

            frontmatter[key] = value

        return frontmatter

    def _remove_frontmatter(self, content: str) -> str:
        """移除 frontmatter，返回純文章內容"""
        return re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    def generate_html_script_tags(self, schemas: List[SchemaMarkup]) -> str:
        """
        生成可嵌入 HTML 的 <script> 標籤

        Args:
            schemas: Schema markups 列表

        Returns:
            str: HTML script 標籤
        """
        html_output = ""

        for schema in schemas:
            json_str = json.dumps(schema.json_ld, ensure_ascii=False, indent=2)
            html_output += f'<script type="application/ld+json">\n{json_str}\n</script>\n\n'

        return html_output

    def generate_markdown_report(
        self,
        schemas: List[SchemaMarkup],
        output_path: Optional[str] = None
    ) -> str:
        """
        生成 Markdown 格式的 Schema 報告

        Args:
            schemas: Schema markups 列表
            output_path: 輸出檔案路徑 (可選)

        Returns:
            str: Markdown 格式報告
        """
        report = "# Schema.org 結構化數據報告\n\n"

        report += f"**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"**生成的 Schema 類型**: {len(schemas)} 個\n\n"

        report += "---\n\n"

        for i, schema in enumerate(schemas, 1):
            status_emoji = {
                'valid': '✅',
                'warning': '⚠️',
                'invalid': '❌'
            }

            report += f"## {i}. {schema.schema_type} Schema\n\n"
            report += f"**驗證狀態**: {status_emoji[schema.validation_status]} {schema.validation_status.upper()}\n\n"

            if schema.issues:
                report += "**驗證問題**:\n"
                for issue in schema.issues:
                    report += f"- {issue}\n"
                report += "\n"

            report += "### JSON-LD 代碼\n\n"
            report += "```json\n"
            report += json.dumps(schema.json_ld, ensure_ascii=False, indent=2)
            report += "\n```\n\n"

            report += "### HTML 嵌入代碼\n\n"
            report += "```html\n"
            json_str = json.dumps(schema.json_ld, ensure_ascii=False, indent=2)
            report += f'<script type="application/ld+json">\n{json_str}\n</script>\n'
            report += "```\n\n"

            report += "---\n\n"

        report += "## 📊 Schema 優化建議\n\n"

        # 根據生成的 Schema 類型提供建議
        schema_types = [s.schema_type for s in schemas]

        if 'FAQPage' in schema_types:
            report += "✅ **FAQ Schema 已生成** - 高度提升 AI Overviews 可見度\n"
        else:
            report += "💡 **建議加入 FAQ 內容** - FAQ Schema 對 AI Overviews 非常有效\n"

        if 'HowTo' in schema_types:
            report += "✅ **HowTo Schema 已生成** - 適合教學類文章\n"
        else:
            report += "💡 **如果是教學文章，建議加入步驟說明** - 可生成 HowTo Schema\n"

        report += "\n---\n\n"
        report += "## 🔗 相關資源\n\n"
        report += "- [Google Schema Markup 測試工具](https://validator.schema.org/)\n"
        report += "- [Schema.org 官方文檔](https://schema.org/)\n"
        report += "- [Google 搜尋結構化數據指南](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)\n"

        # 如果指定輸出路徑，寫入檔案
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Schema 報告已生成: {output_path}")

        return report


def main():
    """命令行介面"""
    parser = argparse.ArgumentParser(
        description='為文章生成 Schema.org 結構化數據標記'
    )
    parser.add_argument(
        'article',
        help='文章檔案路徑'
    )
    parser.add_argument(
        '-u', '--base-url',
        help='網站基礎 URL (用於 breadcrumb)'
    )
    parser.add_argument(
        '-c', '--category',
        help='文章分類 (用於 breadcrumb)'
    )
    parser.add_argument(
        '-o', '--output',
        help='輸出報告路徑 (可選)'
    )
    parser.add_argument(
        '--html',
        help='輸出 HTML script 標籤到指定檔案 (可選)'
    )

    args = parser.parse_args()

    # 創建生成器
    generator = SchemaGenerator()

    # 生成 schemas
    print(f"🔍 分析文章: {args.article}")
    schemas = generator.generate_from_article(
        args.article,
        args.base_url,
        args.category
    )

    print(f"✅ 生成 {len(schemas)} 個 Schema markups")

    # 生成報告
    report = generator.generate_markdown_report(schemas, args.output)

    # 如果沒有指定輸出路徑，列印到終端
    if not args.output:
        print("\n" + report)

    # 如果指定 HTML 輸出，生成 HTML script 標籤
    if args.html:
        html_tags = generator.generate_html_script_tags(schemas)
        with open(args.html, 'w', encoding='utf-8') as f:
            f.write(html_tags)
        print(f"✅ HTML script 標籤已生成: {args.html}")

    # 顯示摘要
    for schema in schemas:
        status_emoji = {'valid': '✅', 'warning': '⚠️', 'invalid': '❌'}
        print(f"{status_emoji[schema.validation_status]} {schema.schema_type}: {schema.validation_status}")


if __name__ == '__main__':
    main()
