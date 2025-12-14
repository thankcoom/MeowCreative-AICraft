#!/usr/bin/env python3
"""
使用 Pollinations.ai 免費 API 生成圖片
完全免費，無需註冊，無需 Token！
"""

import os
import sys
import time
import requests
from pathlib import Path
from urllib.parse import quote

# 顏色輸出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def generate_image_pollinations(prompt: str, output_path: str, width: int = 1024, height: int = 1024) -> bool:
    """
    使用 Pollinations.ai API 生成圖片

    Args:
        prompt: 圖片生成提示詞
        output_path: 輸出檔案路徑
        width: 圖片寬度
        height: 圖片高度

    Returns:
        bool: 是否成功
    """
    try:
        print_info(f"正在生成圖片...")
        print_info(f"提示詞: {prompt[:100]}...")

        # Pollinations.ai API URL
        encoded_prompt = quote(prompt)
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"

        print_info(f"呼叫 API: {api_url[:80]}...")

        # 下載圖片
        response = requests.get(api_url, timeout=60)

        if response.status_code == 200:
            # 儲存圖片
            with open(output_path, 'wb') as f:
                f.write(response.content)

            # 檢查檔案大小
            file_size = os.path.getsize(output_path)
            size_mb = file_size / (1024 * 1024)

            print_success(f"圖片已儲存: {output_path}")
            print_info(f"檔案大小: {size_mb:.2f} MB")
            return True
        else:
            print_error(f"API 錯誤: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"發生錯誤: {str(e)}")
        return False

def main():
    """主程式"""
    print_header("🎨 WordPress 部落格 AI 圖片自動生成系統")
    print_info("使用 Pollinations.ai - 完全免費，無需 Token！")

    # 尋找最新的 session 資料夾
    output_dir = Path(__file__).parent.parent.parent.parent / 'output'
    sessions = sorted(output_dir.glob('session_*'), reverse=True)

    if not sessions:
        print_error("找不到 session 資料夾")
        sys.exit(1)

    session_dir = sessions[0]
    print_info(f"使用 session: {session_dir.name}")

    # 建立圖片資料夾
    images_dir = session_dir / 'images'
    images_dir.mkdir(exist_ok=True)
    print_success(f"圖片將儲存至: {images_dir}")

    # 圖片配置
    images = [
        {
            'name': 'hero-image',
            'filename': 'cover-claude-code-guide.webp',
            'width': 1920,
            'height': 1080,
            'priority': 1,
            'prompt': 'A modern tech illustration showing a developer using Claude Code. Center: dark terminal window with clean CLI interface and Claude chat bubbles. Surrounded by 5 glowing icons representing best practices: file icon, permission lock, toolbox, memory chip, workflow arrows. Background: gradient blue-purple with subtle code snippets as texture. Style: minimal, flat design, tech-savvy, high quality, 4K, professional.'
        },
        {
            'name': 'subagent-architecture',
            'filename': 'subagent-system-architecture.webp',
            'width': 1600,
            'height': 900,
            'priority': 1,
            'prompt': 'Futuristic network architecture diagram. Center: large main node labeled Main Agent. Surrounding: 4-5 smaller sub-nodes labeled Sub-agent, connected by glowing lines with arrows showing data flow. Each sub-agent has different color (blue, green, orange, purple). Dark background, neural network visualization style, tech-inspired, glowing neon lines, high quality, 4K, professional.'
        },
        {
            'name': 'tool-comparison',
            'filename': 'tool-comparison-chart.webp',
            'width': 1400,
            'height': 1000,
            'priority': 2,
            'prompt': 'Three-column comparison infographic. Each column represents a tool (Claude Code, Cursor, GitHub Copilot) with brand colors. Each column contains: tool icon, name, 5 feature icons (checkmarks or crosses), use-case text. Modern minimal design, clear icons, short text labels. Background: light gray or white, high readability, professional style, high quality.'
        },
        {
            'name': 'efficiency-comparison',
            'filename': 'efficiency-before-after.webp',
            'width': 1600,
            'height': 900,
            'priority': 2,
            'prompt': 'Split comparison illustration. LEFT Before: developer tired at messy desk, late night clock, stressed. RIGHT After: same developer happy, clean desk, daytime clock, screen showing Claude Code interface, checkmark icons around. Center: large arrow with +300% label. Colors: left side darker/cooler, right side bright/warm. Illustration style, flat design, friendly aesthetic, high quality.'
        },
        {
            'name': 'claude-md-concept',
            'filename': 'claude-md-concept.webp',
            'width': 1200,
            'height': 800,
            'priority': 3,
            'prompt': 'Isometric illustration: project folder and Claude.md file icon on left, soft light beam connecting to Claude AI avatar (circular) on right. Around AI: gear icons and memory symbols. Background: light gray. Color scheme: Anthropic orange and blue. Style: flat, clean, minimal, high quality, digital art.'
        }
    ]

    # 詢問要生成哪些圖片
    print_header("選擇要生成的圖片")
    print("1. 全部生成（5 張）")
    print("2. 只生成必要圖片（2 張：封面 + Sub-agent 架構）")
    print("3. 自訂選擇")

    choice = input("\n請選擇 (1-3): ").strip()

    if choice == '2':
        images = [img for img in images if img['priority'] == 1]
    elif choice == '3':
        print("\n可用圖片：")
        for i, img in enumerate(images, 1):
            print(f"{i}. {img['name']} (優先度: {img['priority']})")
        selected = input("請輸入要生成的圖片編號（用逗號分隔，如 1,2,3）: ").strip()
        indices = [int(x.strip()) - 1 for x in selected.split(',') if x.strip().isdigit()]
        images = [images[i] for i in indices if 0 <= i < len(images)]

    if not images:
        print_error("未選擇任何圖片")
        sys.exit(1)

    print_success(f"將生成 {len(images)} 張圖片")

    # 批次生成
    print_header("開始生成圖片")
    success_count = 0

    for i, img in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] 生成: {img['name']}")
        print("-" * 60)

        output_path = images_dir / img['filename']

        # 檢查是否已存在
        if output_path.exists():
            overwrite = input(f"檔案已存在，是否覆蓋? (y/N): ").strip().lower()
            if overwrite != 'y':
                print_warning("已跳過")
                continue

        # 生成圖片
        if generate_image_pollinations(
            img['prompt'],
            str(output_path),
            img.get('width', 1024),
            img.get('height', 1024)
        ):
            success_count += 1
        else:
            print_error(f"生成失敗: {img['name']}")

        # 避免過快請求
        if i < len(images):
            print_info("等待 2 秒...")
            time.sleep(2)

    # 結果統計
    print_header("生成完成")
    print_success(f"成功生成: {success_count}/{len(images)} 張圖片")
    print_info(f"圖片位置: {images_dir}")

    # 詢問是否更新文章
    if success_count > 0:
        print_header("更新文章")
        print_info("圖片已生成，你現在可以：")
        print_info("1. 查看生成的圖片")
        print_info("2. 手動將圖片插入文章")
        print_info("3. 或使用其他工具自動插入")

        print(f"\n圖片位置: {images_dir}")
        print(f"文章位置: {session_dir / 'final_article.md'}")

    print_header("🎉 完成！")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式已中斷")
        sys.exit(0)
    except Exception as e:
        print_error(f"發生未預期的錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
