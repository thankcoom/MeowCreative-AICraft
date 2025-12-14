#!/usr/bin/env python3
"""
WordPress 文章發布腳本
用於自動將 Markdown 文章發布到 WordPress
"""

import os
import sys
import argparse
import yaml
import json
import requests
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class WordPressPublisher:
    """WordPress 發布器"""

    def __init__(self, site_url: str, username: str, app_password: str):
        self.site_url = site_url.rstrip('/')
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.auth = (username, app_password)

    def test_connection(self) -> Tuple[bool, str]:
        """測試 WordPress API 連線"""
        try:
            response = requests.get(
                f"{self.api_base}/posts",
                auth=self.auth,
                params={'per_page': 1},
                timeout=10
            )

            if response.status_code == 200:
                return True, "連線成功"
            elif response.status_code == 401:
                return False, "認證失敗：請檢查 username 和 app_password"
            elif response.status_code == 403:
                return False, "權限不足：請確認帳號有發布文章的權限"
            elif response.status_code == 404:
                return False, "API 端點不存在：請確認 WordPress 版本支援 REST API"
            else:
                return False, f"連線失敗：HTTP {response.status_code}"

        except requests.exceptions.Timeout:
            return False, "連線超時：請檢查網路連線"
        except requests.exceptions.ConnectionError:
            return False, "無法連線到伺服器：請檢查 site_url 是否正確"
        except Exception as e:
            return False, f"未知錯誤：{str(e)}"

    def get_or_create_category(self, category_name: str) -> Optional[int]:
        """取得或建立分類"""
        try:
            # 先搜尋是否存在
            response = requests.get(
                f"{self.api_base}/categories",
                auth=self.auth,
                params={'search': category_name},
                timeout=10
            )

            if response.status_code == 200:
                categories = response.json()
                if categories:
                    return categories[0]['id']

            # 不存在則建立
            response = requests.post(
                f"{self.api_base}/categories",
                auth=self.auth,
                json={'name': category_name},
                timeout=10
            )

            if response.status_code == 201:
                return response.json()['id']

            return None

        except Exception as e:
            print(f"警告：無法處理分類 '{category_name}': {str(e)}")
            return None

    def get_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """取得或建立標籤"""
        tag_ids = []

        for tag_name in tag_names:
            try:
                # 先搜尋是否存在
                response = requests.get(
                    f"{self.api_base}/tags",
                    auth=self.auth,
                    params={'search': tag_name},
                    timeout=10
                )

                if response.status_code == 200:
                    tags = response.json()
                    if tags:
                        tag_ids.append(tags[0]['id'])
                        continue

                # 不存在則建立
                response = requests.post(
                    f"{self.api_base}/tags",
                    auth=self.auth,
                    json={'name': tag_name},
                    timeout=10
                )

                if response.status_code == 201:
                    tag_ids.append(response.json()['id'])

            except Exception as e:
                print(f"警告：無法處理標籤 '{tag_name}': {str(e)}")
                continue

        return tag_ids

    def publish_post(
        self,
        title: str,
        content: str,
        status: str = 'draft',
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
        meta_description: Optional[str] = None,
        focus_keyword: Optional[str] = None
    ) -> Tuple[bool, Dict]:
        """發布文章"""

        # 準備文章資料
        post_data = {
            'title': title,
            'content': content,
            'status': status,
        }

        if category_id:
            post_data['categories'] = [category_id]

        if tag_ids:
            post_data['tags'] = tag_ids

        # 設定 Yoast SEO meta (如果有安裝 Yoast)
        if meta_description or focus_keyword:
            post_data['meta'] = {}
            if meta_description:
                post_data['meta']['_yoast_wpseo_metadesc'] = meta_description
            if focus_keyword:
                post_data['meta']['_yoast_wpseo_focuskw'] = focus_keyword

        try:
            response = requests.post(
                f"{self.api_base}/posts",
                auth=self.auth,
                json=post_data,
                timeout=30
            )

            if response.status_code == 201:
                result = response.json()
                return True, {
                    'id': result['id'],
                    'link': result['link'],
                    'status': result['status'],
                    'title': result['title']['rendered']
                }
            else:
                return False, {
                    'error': f"HTTP {response.status_code}",
                    'message': response.text
                }

        except Exception as e:
            return False, {
                'error': 'Exception',
                'message': str(e)
            }


def parse_article(article_path: str) -> Tuple[str, str, Dict]:
    """解析 Markdown 文章"""

    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 從第一行提取標題
    lines = content.split('\n')
    title = lines[0].lstrip('# ').strip() if lines else '無標題'
    body = '\n'.join(lines[1:]) if len(lines) > 1 else content
    metadata = {}

    # 從內容提取 meta description (如果有)
    meta_match = re.search(r'> Meta Description: (.+)', body)
    if meta_match:
        metadata['meta_description'] = meta_match.group(1).strip()

    # 從內容提取標籤 (如果有)
    tags_match = re.search(r'\*\*標籤\*\*[：:]\s*([^\n]+)', body)
    if tags_match:
        tags_str = tags_match.group(1)
        # 移除 # 符號並分割
        tags = [tag.strip().lstrip('#') for tag in tags_str.split(',')]
        metadata['tags'] = tags

    # 從內容提取分類 (如果有)
    category_match = re.search(r'\*\*分類\*\*[：:]\s*([^\n]+)', body)
    if category_match:
        category_str = category_match.group(1).strip()
        # 提取最後一個分類 (如: "技術分享 > AI 應用" -> "AI 應用")
        if '>' in category_str:
            category = category_str.split('>')[-1].strip()
        else:
            category = category_str
        metadata['category'] = category

    return title, body, metadata


def create_publish_report(
    session_dir: str,
    article_title: str,
    success: bool,
    result: Dict,
    word_count: int,
    category: str,
    tags: List[str]
):
    """建立發布報告"""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if success:
        report_content = f"""# 發布報告

## 基本資訊
- 發布時間：{timestamp}
- 文章標題：{article_title}
- WordPress URL：{result.get('link', 'N/A')}
- 文章 ID：{result.get('id', 'N/A')}
- 狀態：{result.get('status', 'N/A')}

## 發布內容
- 字數：{word_count:,}
- 分類：{category}
- 標籤：{', '.join(tags)}

## 發布結果
狀態：成功

## 相關連結
- WordPress 編輯頁面：{result.get('link', '').replace('?p=', 'wp-admin/post.php?post=').replace('&preview=true', '&action=edit')}
- 預覽連結：{result.get('link', '')}

## 後續建議
- [ ] 檢查文章在前台顯示是否正常
- [ ] 分享到社群媒體（Facebook, Twitter, LinkedIn）
- [ ] 通知訂閱者（如有電子報）
- [ ] 監控初期流量和互動
- [ ] 一週後檢查 Google Search Console

## 錯誤記錄
無
"""
    else:
        report_content = f"""# 發布報告

## 基本資訊
- 嘗試時間：{timestamp}
- 文章標題：{article_title}

## 發布內容
- 字數：{word_count:,}
- 分類：{category}
- 標籤：{', '.join(tags)}

## 發布結果
狀態：失敗

## 錯誤記錄
- 錯誤類型：{result.get('error', 'Unknown')}
- 錯誤訊息：{result.get('message', 'No details')}

## 建議處理方式
請參考錯誤訊息進行問題排查，或考慮手動發布。
"""

    report_path = os.path.join(session_dir, 'publish_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\n發布報告已儲存：{report_path}")


def main():
    parser = argparse.ArgumentParser(description='WordPress 文章發布工具')
    parser.add_argument('--article', required=True, help='文章檔案路徑')
    parser.add_argument('--credentials', required=True, help='認證資訊檔案路徑')
    parser.add_argument('--status', default='draft', choices=['draft', 'publish'], help='發布狀態')
    parser.add_argument('--category', help='分類名稱')
    parser.add_argument('--tags', help='標籤，用逗號分隔')

    args = parser.parse_args()

    # 讀取認證資訊
    print("正在讀取 WordPress 認證資訊...")
    with open(args.credentials, 'r', encoding='utf-8') as f:
        creds = yaml.safe_load(f)['wordpress']

    # 初始化發布器
    publisher = WordPressPublisher(
        site_url=creds['site_url'],
        username=creds['username'],
        app_password=creds['app_password']
    )

    # 測試連線
    print("\n正在測試 WordPress API 連線...")
    success, message = publisher.test_connection()
    if not success:
        print(f"連線測試失敗：{message}")
        sys.exit(1)
    print(f"連線測試成功")

    # 解析文章
    print("\n正在解析文章...")
    title, content, metadata = parse_article(args.article)
    print(f"文章標題：{title}")
    print(f"文章字數：{len(content):,}")

    # 取得分類
    category_name = args.category or metadata.get('category', '技術分享')
    print(f"\n正在處理分類：{category_name}")
    category_id = publisher.get_or_create_category(category_name)
    if category_id:
        print(f"分類 ID：{category_id}")

    # 取得標籤
    if args.tags:
        tag_names = [tag.strip() for tag in args.tags.split(',')]
    else:
        tag_names = metadata.get('tags', [])

    if tag_names:
        print(f"\n正在處理標籤：{', '.join(tag_names)}")
        tag_ids = publisher.get_or_create_tags(tag_names)
        print(f"標籤 IDs：{tag_ids}")
    else:
        tag_ids = []

    # 發布文章
    print(f"\n正在發布文章（狀態：{args.status}）...")
    success, result = publisher.publish_post(
        title=title,
        content=content,
        status=args.status,
        category_id=category_id,
        tag_ids=tag_ids,
        meta_description=metadata.get('meta_description'),
        focus_keyword=tag_names[0] if tag_names else None
    )

    # 建立報告
    session_dir = os.path.dirname(args.article)
    create_publish_report(
        session_dir=session_dir,
        article_title=title,
        success=success,
        result=result,
        word_count=len(content),
        category=category_name,
        tags=tag_names
    )

    # 輸出結果
    print("\n" + "="*60)
    if success:
        print("發布成功！")
        print(f"\n文章 ID：{result['id']}")
        print(f"文章連結：{result['link']}")
        print(f"狀態：{result['status']}")
    else:
        print("發布失敗！")
        print(f"\n錯誤類型：{result.get('error')}")
        print(f"錯誤訊息：{result.get('message')}")
    print("="*60)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
