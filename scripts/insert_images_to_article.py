#!/usr/bin/env python3
"""
文章圖片自動插入系統
根據文章內容，自動在適當位置插入生成的圖片
"""

import os
import re
from typing import List, Tuple


class ArticleImageInserter:
    """文章圖片插入器"""

    def __init__(self, article_path: str, images_dir: str):
        self.article_path = article_path
        self.images_dir = images_dir

        # 圖片插入規則：(插入位置關鍵字, 圖片檔名, 圖片說明)
        self.insertion_rules = [
            # 系統架構圖
            {
                'after_heading': '## 5 分鐘看懂:Social Analyzer 如何在 1000 個平台找到目標?',
                'image': 'system-architecture.png',
                'alt': 'Social Analyzer 系統架構圖',
                'caption': '*Social Analyzer 的前後端架構與技術堆疊*'
            },
            # 比較圖表
            {
                'after_heading': '### 與傳統工具的差異',
                'image': 'comparison-chart.svg',
                'alt': '傳統方式 vs Social Analyzer 比較',
                'caption': '*傳統搜尋方式與 Social Analyzer 的效率比較*'
            },
            # 偵測模式流程圖
            {
                'after_heading': '### 四種偵測模式實戰解析',
                'image': 'detection-modes.png',
                'alt': '四種偵測模式流程圖',
                'caption': '*Social Analyzer 四種偵測模式的運作流程*'
            },
            # 信心度評分圖
            {
                'after_heading': '### 信心度評分實戰指南',
                'image': 'confidence-score-chart.svg',
                'alt': '信心度評分指南',
                'caption': '*不同信心度分數的可信度等級*'
            },
            # 詐騙查證流程
            {
                'after_heading': '### 1. 詐騙防制：追蹤多平台詐騙集團',
                'image': 'scam-investigation-flow.png',
                'alt': '詐騙查證流程示意圖',
                'caption': '*使用 Social Analyzer 追蹤詐騙帳號的完整流程*'
            },
            # 法律合規圖表
            {
                'after_heading': '## 法律紅線必讀:用錯了可能坐牢!台灣個資法完整解析',
                'image': 'legal-compliance-guide.svg',
                'alt': '個資法合規指南',
                'caption': '*個資法規範下的合法使用 vs 違法行為對照*'
            },
            # 合法性判斷流程樹
            {
                'after_heading': '### 灰色地帶的判斷原則',
                'image': 'legality-decision-tree.png',
                'alt': '使用場景合法性判斷流程',
                'caption': '*判斷使用場景是否合法的決策流程*'
            }
        ]

    def read_article(self) -> str:
        """讀取文章內容"""
        with open(self.article_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_article(self, content: str):
        """寫入文章內容"""
        # 先備份原文章
        backup_path = self.article_path.replace('.md', '_backup.md')
        with open(self.article_path, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        print(f"✓ 原文章已備份至: {backup_path}")

        # 寫入新內容
        with open(self.article_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def create_image_markdown(self, image: str, alt: str, caption: str) -> str:
        """創建圖片的 Markdown 語法"""
        return f"\n\n![{alt}](images/{image})\n{caption}\n\n"

    def insert_images(self):
        """在文章中插入圖片"""
        content = self.read_article()
        lines = content.split('\n')
        modified_lines = []
        images_inserted = 0

        i = 0
        while i < len(lines):
            line = lines[i]
            modified_lines.append(line)

            # 檢查是否匹配任何插入規則
            for rule in self.insertion_rules:
                heading = rule['after_heading']

                # 檢查當前行是否為目標標題
                if line.strip() == heading.strip():
                    # 確認圖片尚未插入（避免重複插入）
                    image_filename = rule['image']

                    # 檢查接下來的幾行是否已經包含這個圖片
                    next_lines = '\n'.join(lines[i:min(i+10, len(lines))])
                    if image_filename not in next_lines:
                        # 插入圖片
                        image_markdown = self.create_image_markdown(
                            rule['image'],
                            rule['alt'],
                            rule['caption']
                        )
                        modified_lines.append(image_markdown)
                        images_inserted += 1
                        print(f"  ✓ 已在「{heading[:50]}...」後插入圖片: {image_filename}")

            i += 1

        # 組合新內容
        new_content = '\n'.join(modified_lines)

        # 寫入文章
        if images_inserted > 0:
            self.write_article(new_content)
            print(f"\n✓ 共插入 {images_inserted} 張圖片")
        else:
            print("\n⚠️  沒有找到適合的插入位置或圖片已經存在")

        return images_inserted


def main():
    """主函數"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║            📝 文章圖片自動插入系統 📝                      ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    # 設定路徑
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    article_path = os.path.join(
        base_dir,
        'output', 'session_20251030_115533', 'final_article.md'
    )
    images_dir = os.path.join(
        base_dir,
        'output', 'session_20251030_115533', 'images'
    )

    # 檢查文件是否存在
    if not os.path.exists(article_path):
        print(f"❌ 文章不存在: {article_path}")
        return

    if not os.path.exists(images_dir):
        print(f"❌ 圖片目錄不存在: {images_dir}")
        return

    print(f"📄 文章路徑: {article_path}")
    print(f"🖼️  圖片目錄: {images_dir}\n")

    # 執行插入
    inserter = ArticleImageInserter(article_path, images_dir)

    print("🔄 正在分析文章並插入圖片...\n")
    images_inserted = inserter.insert_images()

    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                   ✅ 處理完成！                            ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    if images_inserted > 0:
        print("💡 提示:")
        print(f"  - 更新後的文章: {article_path}")
        print(f"  - 原文章備份: {article_path.replace('.md', '_backup.md')}")
        print(f"  - 共插入 {images_inserted} 張圖片")
        print("\n  請檢查文章，確認圖片位置是否合適！")
    else:
        print("⚠️  未插入任何圖片，可能的原因：")
        print("  - 標題格式不匹配")
        print("  - 圖片已經存在")
        print("  - 請檢查插入規則設定")


if __name__ == "__main__":
    main()
