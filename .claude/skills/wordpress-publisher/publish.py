#!/usr/bin/env python3
"""
WordPress Publisher Helper Script
處理 WordPress REST API 發布操作
"""

import requests
import yaml
import json
import base64
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class WordPressPublisher:
    """WordPress 發布管理類"""

    def __init__(self, credentials_path: str = None):
        """
        初始化 WordPress Publisher

        Args:
            credentials_path: WordPress 憑證檔案路徑
        """
        if credentials_path is None:
            credentials_path = Path(__file__).parent.parent.parent / "config" / "wordpress-credentials.yaml"

        self.credentials = self._load_credentials(credentials_path)
        self.site_url = self.credentials.get('site_url')
        self.username = self.credentials.get('username')
        self.app_password = self.credentials.get('application_password')

        # 驗證必要欄位
        if not all([self.site_url, self.username, self.app_password]):
            raise ValueError("缺少必要的 WordPress 憑證欄位")

        # 設定 API endpoint
        self.api_base = f"{self.site_url.rstrip('/')}/wp-json/wp/v2"

        # 設定認證
        self.auth = (self.username, self.app_password)

    def _load_credentials(self, path: str) -> Dict:
        """載入 WordPress 憑證"""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def markdown_to_wordpress_html(self, markdown_content: str) -> str:
        """
        將 Markdown 轉換為 WordPress HTML

        Args:
            markdown_content: Markdown 內容

        Returns:
            WordPress 格式的 HTML
        """
        html = markdown_content

        # H2-H6 標題
        html = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
        html = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

        # H1 (通常是標題，不放在內容中)
        html = re.sub(r'^#\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

        # 粗體
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

        # 斜體
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # 連結
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

        # 無序列表
        html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*</li>)', r'<ul>\n\1\n</ul>', html, flags=re.DOTALL)

        # 段落 (雙換行)
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<'):
                para = f'<p>{para}</p>'
            html_paragraphs.append(para)

        html = '\n\n'.join(html_paragraphs)

        return html

    def get_or_create_category(self, category_name: str) -> int:
        """
        獲取或創建分類

        Args:
            category_name: 分類名稱

        Returns:
            分類 ID
        """
        # 搜尋現有分類
        response = requests.get(
            f"{self.api_base}/categories",
            params={'search': category_name},
            auth=self.auth
        )

        if response.status_code == 200 and response.json():
            return response.json()[0]['id']

        # 創建新分類
        response = requests.post(
            f"{self.api_base}/categories",
            json={'name': category_name},
            auth=self.auth
        )

        if response.status_code == 201:
            return response.json()['id']

        raise Exception(f"無法創建分類: {response.text}")

    def get_or_create_tag(self, tag_name: str) -> int:
        """
        獲取或創建標籤

        Args:
            tag_name: 標籤名稱

        Returns:
            標籤 ID
        """
        # 搜尋現有標籤
        response = requests.get(
            f"{self.api_base}/tags",
            params={'search': tag_name},
            auth=self.auth
        )

        if response.status_code == 200 and response.json():
            return response.json()[0]['id']

        # 創建新標籤
        response = requests.post(
            f"{self.api_base}/tags",
            json={'name': tag_name},
            auth=self.auth
        )

        if response.status_code == 201:
            return response.json()['id']

        raise Exception(f"無法創建標籤: {response.text}")

    def upload_featured_image(self, image_path: str) -> int:
        """
        上傳特色圖片

        Args:
            image_path: 圖片檔案路徑

        Returns:
            媒體 ID
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"找不到圖片檔案: {image_path}")

        # 讀取圖片
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # 取得檔名和 MIME type
        filename = os.path.basename(image_path)
        mime_type = 'image/jpeg'
        if filename.lower().endswith('.png'):
            mime_type = 'image/png'
        elif filename.lower().endswith('.gif'):
            mime_type = 'image/gif'

        # 上傳圖片
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': mime_type
        }

        response = requests.post(
            f"{self.api_base}/media",
            data=image_data,
            headers=headers,
            auth=self.auth
        )

        if response.status_code == 201:
            return response.json()['id']

        raise Exception(f"無法上傳圖片: {response.text}")

    def publish_post(
        self,
        title: str,
        content: str,
        categories: List[str] = None,
        tags: List[str] = None,
        featured_image_path: str = None,
        status: str = 'publish',
        excerpt: str = None,
        meta_description: str = None,
        focus_keyword: str = None
    ) -> Dict:
        """
        發布文章到 WordPress

        Args:
            title: 文章標題
            content: 文章內容 (Markdown 或 HTML)
            categories: 分類列表
            tags: 標籤列表
            featured_image_path: 特色圖片路徑
            status: 文章狀態 ('draft', 'publish', 'pending')
            excerpt: 摘要
            meta_description: SEO meta description
            focus_keyword: SEO focus keyword

        Returns:
            發布結果資訊
        """
        # 轉換 Markdown 到 HTML
        if not content.startswith('<'):
            html_content = self.markdown_to_wordpress_html(content)
        else:
            html_content = content

        # 準備文章資料
        post_data = {
            'title': title,
            'content': html_content,
            'status': status
        }

        # 處理摘要
        if excerpt:
            post_data['excerpt'] = excerpt

        # 處理分類
        if categories:
            category_ids = [self.get_or_create_category(cat) for cat in categories]
            post_data['categories'] = category_ids

        # 處理標籤
        if tags:
            tag_ids = [self.get_or_create_tag(tag) for tag in tags]
            post_data['tags'] = tag_ids

        # 處理特色圖片
        if featured_image_path:
            try:
                media_id = self.upload_featured_image(featured_image_path)
                post_data['featured_media'] = media_id
            except Exception as e:
                print(f"⚠️ 特色圖片上傳失敗: {e}")

        # 處理 SEO meta (需要 Yoast SEO 或類似外掛)
        if meta_description or focus_keyword:
            post_data['meta'] = {}
            if meta_description:
                post_data['meta']['_yoast_wpseo_metadesc'] = meta_description
            if focus_keyword:
                post_data['meta']['_yoast_wpseo_focuskw'] = focus_keyword

        # 發布文章
        response = requests.post(
            f"{self.api_base}/posts",
            json=post_data,
            auth=self.auth
        )

        if response.status_code in [200, 201]:
            result = response.json()
            return {
                'success': True,
                'post_id': result['id'],
                'url': result['link'],
                'status': result['status'],
                'title': result['title']['rendered'],
                'date': result['date']
            }
        else:
            return {
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }

    def update_post(
        self,
        post_id: int,
        title: str = None,
        content: str = None,
        status: str = None
    ) -> Dict:
        """
        更新現有文章

        Args:
            post_id: 文章 ID
            title: 新標題 (可選)
            content: 新內容 (可選)
            status: 新狀態 (可選)

        Returns:
            更新結果資訊
        """
        post_data = {}

        if title:
            post_data['title'] = title

        if content:
            if not content.startswith('<'):
                post_data['content'] = self.markdown_to_wordpress_html(content)
            else:
                post_data['content'] = content

        if status:
            post_data['status'] = status

        response = requests.post(
            f"{self.api_base}/posts/{post_id}",
            json=post_data,
            auth=self.auth
        )

        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'post_id': result['id'],
                'url': result['link']
            }
        else:
            return {
                'success': False,
                'error': response.text
            }


def main():
    """命令列介面"""
    if len(sys.argv) < 3:
        print("用法: python publish.py <markdown_file> <title> [categories] [tags]")
        print("範例: python publish.py article.md \"文章標題\" \"技術,教學\" \"Python,自動化\"")
        sys.exit(1)

    markdown_file = sys.argv[1]
    title = sys.argv[2]
    categories = sys.argv[3].split(',') if len(sys.argv) > 3 else []
    tags = sys.argv[4].split(',') if len(sys.argv) > 4 else []

    # 讀取 Markdown 內容
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 發布文章
    publisher = WordPressPublisher()
    result = publisher.publish_post(
        title=title,
        content=content,
        categories=categories,
        tags=tags
    )

    # 輸出結果
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
