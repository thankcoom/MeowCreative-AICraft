#!/usr/bin/env python3
"""
內容改寫工具 v2.5.0
==================

將長篇文章改寫為多種社交媒體格式。

功能：
- Twitter/X 推文串
- LinkedIn 貼文
- Instagram 文案
- 短影片腳本
- 電子郵件摘要

使用方式：
---------
# 生成 Twitter 推文串
python3 repurpose.py twitter --input article.md --output thread.md

# 生成多平台內容
python3 repurpose.py all --input article.md --output-dir repurposed/

# 指定平台
python3 repurpose.py --platforms twitter,linkedin --input article.md
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

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


class ContentRepurposer(BaseSkill):
    """內容改寫器"""

    SKILL_NAME = "content-repurposer"
    VERSION = "1.0.0"

    # 平台配置
    PLATFORMS = {
        'twitter': {
            'name': 'Twitter/X',
            'max_chars': 280,
            'thread_max': 10,
            'hashtag_count': 3
        },
        'linkedin': {
            'name': 'LinkedIn',
            'max_chars': 3000,
            'optimal_chars': 1300,
            'hashtag_count': 5
        },
        'instagram': {
            'name': 'Instagram',
            'max_chars': 2200,
            'optimal_chars': 150,
            'hashtag_count': 30
        },
        'email': {
            'name': 'Email',
            'subject_max': 60,
            'preview_max': 140
        },
        'video': {
            'name': 'Short Video',
            'duration': '60s',
            'format': 'script'
        }
    }

    def _execute(self, input_file: str, platform: str = 'all',
                 output_dir: str = None) -> dict:
        """執行內容改寫"""
        content = self.read_file(input_file)
        results = {}

        if platform == 'all':
            platforms = self.PLATFORMS.keys()
        else:
            platforms = [p.strip() for p in platform.split(',')]

        for plat in platforms:
            if plat in self.PLATFORMS:
                results[plat] = self._repurpose_for_platform(content, plat)

        if output_dir:
            self._save_results(results, output_dir)

        return results

    def _repurpose_for_platform(self, content: str, platform: str) -> dict:
        """為特定平台改寫內容"""
        # 提取關鍵資訊
        title = self._extract_title(content)
        key_points = self._extract_key_points(content)
        quotes = self._extract_quotes(content)
        stats = self._extract_stats(content)

        if platform == 'twitter':
            return self._generate_twitter_thread(title, key_points, quotes, stats)
        elif platform == 'linkedin':
            return self._generate_linkedin_post(title, key_points, content)
        elif platform == 'instagram':
            return self._generate_instagram_caption(title, key_points)
        elif platform == 'email':
            return self._generate_email_content(title, key_points, content)
        elif platform == 'video':
            return self._generate_video_script(title, key_points)

        return {}

    def _extract_title(self, content: str) -> str:
        """提取標題"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else "無標題"

    def _extract_key_points(self, content: str, max_points: int = 5) -> List[str]:
        """提取關鍵要點"""
        points = []

        # 從 H2 標題提取
        h2_matches = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        points.extend(h2_matches[:max_points])

        # 從列表項提取
        if len(points) < max_points:
            list_matches = re.findall(r'^[-*]\s+(.+)$', content, re.MULTILINE)
            points.extend(list_matches[:max_points - len(points)])

        return points[:max_points]

    def _extract_quotes(self, content: str) -> List[str]:
        """提取引用"""
        quotes = re.findall(r'^>\s+(.+)$', content, re.MULTILINE)
        return quotes[:3]

    def _extract_stats(self, content: str) -> List[str]:
        """提取統計數據"""
        # 匹配包含數字的句子
        stats = re.findall(r'[^。！？.!?\n]*\d+[%％萬億千百]+[^。！？.!?\n]*[。！？.!?]', content)
        return stats[:5]

    def _generate_twitter_thread(self, title: str, key_points: List[str],
                                  quotes: List[str], stats: List[str]) -> dict:
        """生成 Twitter 推文串"""
        config = self.PLATFORMS['twitter']
        thread = []

        # 開頭推文
        hook = f"🧵 {title}\n\n一個重要的觀點，讓我用 thread 分享："
        thread.append(self._truncate(hook, config['max_chars']))

        # 要點推文
        for i, point in enumerate(key_points, 1):
            tweet = f"{i}/ {point}"
            thread.append(self._truncate(tweet, config['max_chars']))

        # 數據推文
        if stats:
            stat_tweet = f"📊 關鍵數據：\n\n{stats[0]}"
            thread.append(self._truncate(stat_tweet, config['max_chars']))

        # 結尾推文
        cta = f"如果你覺得有幫助：\n\n1. 轉推這個 thread\n2. 追蹤我獲取更多內容\n3. 留言告訴我你的想法！"
        thread.append(self._truncate(cta, config['max_chars']))

        return {
            'platform': 'Twitter/X',
            'format': 'thread',
            'tweet_count': len(thread),
            'content': thread,
            'hashtags': self._generate_hashtags(title, config['hashtag_count'])
        }

    def _generate_linkedin_post(self, title: str, key_points: List[str],
                                 full_content: str) -> dict:
        """生成 LinkedIn 貼文"""
        config = self.PLATFORMS['linkedin']

        # 開頭 hook
        hook = f"💡 {title}\n\n"

        # 核心內容
        body = "這是我學到的重要觀點：\n\n"
        for i, point in enumerate(key_points, 1):
            body += f"✅ {point}\n"

        # 個人觀點
        personal = "\n---\n\n我的看法：\n這些觀點對於專業人士來說特別重要...\n"

        # CTA
        cta = "\n👉 你有什麼想法？在評論區告訴我！\n"

        # 組合
        post = hook + body + personal + cta

        # 添加 hashtags
        hashtags = self._generate_hashtags(title, config['hashtag_count'])
        post += "\n" + " ".join(f"#{tag}" for tag in hashtags)

        return {
            'platform': 'LinkedIn',
            'format': 'post',
            'char_count': len(post),
            'content': self._truncate(post, config['max_chars']),
            'hashtags': hashtags
        }

    def _generate_instagram_caption(self, title: str, key_points: List[str]) -> dict:
        """生成 Instagram 文案"""
        config = self.PLATFORMS['instagram']

        # 開頭
        caption = f"✨ {title}\n\n"

        # 要點 (用 emoji)
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for i, point in enumerate(key_points[:5]):
            caption += f"{emojis[i]} {point}\n"

        # CTA
        caption += "\n💬 你認同嗎？留言告訴我！\n"
        caption += "📌 收藏這篇，之後用得到！\n"
        caption += "👉 追蹤 @youraccount 獲取更多內容\n"

        # Hashtags (分開放)
        hashtags = self._generate_hashtags(title, 15)

        return {
            'platform': 'Instagram',
            'format': 'caption',
            'char_count': len(caption),
            'content': caption,
            'hashtags': hashtags,
            'hashtag_block': "\n.\n.\n.\n" + " ".join(f"#{tag}" for tag in hashtags)
        }

    def _generate_email_content(self, title: str, key_points: List[str],
                                 full_content: str) -> dict:
        """生成電子郵件內容"""
        config = self.PLATFORMS['email']

        # 主旨行
        subject = f"💡 {title[:config['subject_max'] - 3]}"

        # 預覽文字
        preview = key_points[0][:config['preview_max']] if key_points else ""

        # 正文
        body = f"""
Hi {{name}},

{title}

這裡是你需要知道的重點：

"""
        for point in key_points:
            body += f"• {point}\n"

        body += """

想了解更多？點擊下方連結閱讀完整文章。

[閱讀完整文章]

Best,
{{sender_name}}
"""

        return {
            'platform': 'Email',
            'format': 'newsletter',
            'subject': subject,
            'preview': preview,
            'body': body.strip()
        }

    def _generate_video_script(self, title: str, key_points: List[str]) -> dict:
        """生成短影片腳本"""
        config = self.PLATFORMS['video']

        script = f"""
# 短影片腳本: {title}
# 預計時長: {config['duration']}

## 開場 (0-5秒)
[畫面: 文字標題動畫]
旁白: "{title}"

## Hook (5-10秒)
[畫面: 說話者特寫]
旁白: "很多人都問我這個問題..."

## 主要內容 (10-45秒)
"""
        for i, point in enumerate(key_points[:3], 1):
            script += f"""
### 要點 {i}
[畫面: 說明圖示]
旁白: "{point}"
"""

        script += """
## 結尾 (45-60秒)
[畫面: CTA 動畫]
旁白: "如果你覺得有幫助，記得按讚和追蹤！"

---
## 製作提示
- 使用快節奏剪輯
- 添加字幕
- 背景音樂: 輕快、積極
- B-roll: 相關場景素材
"""

        return {
            'platform': 'Short Video',
            'format': 'script',
            'duration': config['duration'],
            'content': script.strip()
        }

    def _truncate(self, text: str, max_length: int) -> str:
        """截斷文字"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

    def _generate_hashtags(self, title: str, count: int) -> List[str]:
        """生成 hashtags"""
        # 基礎 hashtags
        base_tags = ['內容創作', '自媒體', '知識分享', '學習成長', '職場',
                     'ContentCreation', 'SocialMedia', 'Marketing']

        # 從標題提取關鍵詞
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', title)
        title_tags = [w for w in words if len(w) >= 2]

        # 組合並限制數量
        all_tags = title_tags + base_tags
        return list(dict.fromkeys(all_tags))[:count]

    def _save_results(self, results: dict, output_dir: str) -> None:
        """儲存結果"""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        for platform, data in results.items():
            # 儲存為 Markdown
            md_content = f"# {platform.upper()} 內容\n\n"
            md_content += f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

            if platform == 'twitter':
                md_content += "## 推文串\n\n"
                for i, tweet in enumerate(data.get('content', []), 1):
                    md_content += f"### Tweet {i}\n{tweet}\n\n"

            elif platform in ['linkedin', 'instagram']:
                md_content += f"## 貼文內容\n\n{data.get('content', '')}\n\n"
                if data.get('hashtags'):
                    md_content += f"## Hashtags\n\n{' '.join('#' + t for t in data['hashtags'])}\n"

            elif platform == 'email':
                md_content += f"## 主旨\n{data.get('subject', '')}\n\n"
                md_content += f"## 預覽\n{data.get('preview', '')}\n\n"
                md_content += f"## 正文\n{data.get('body', '')}\n"

            elif platform == 'video':
                md_content += f"## 腳本\n\n{data.get('content', '')}\n"

            self.write_file(str(out_path / f"{platform}.md"), md_content)

        # 儲存 JSON 摘要
        summary = {
            'generated_at': datetime.now().isoformat(),
            'platforms': list(results.keys()),
            'results': results
        }
        self.write_file(str(out_path / "summary.json"),
                        json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="內容改寫工具 v2.5.0")

    parser.add_argument('platform', nargs='?', default='all',
                        help='目標平台 (twitter, linkedin, instagram, email, video, all)')
    parser.add_argument('--input', '-i', required=True, help='輸入文章路徑')
    parser.add_argument('--output', '-o', help='輸出檔案路徑')
    parser.add_argument('--output-dir', '-d', help='輸出目錄')
    parser.add_argument('--platforms', '-p', help='多平台，逗號分隔')

    args = parser.parse_args()

    platform = args.platforms if args.platforms else args.platform
    output_dir = args.output_dir or args.output

    repurposer = ContentRepurposer()
    results = repurposer._execute(args.input, platform, output_dir)

    if not output_dir:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"內容已儲存至: {output_dir}")


if __name__ == '__main__':
    main()
