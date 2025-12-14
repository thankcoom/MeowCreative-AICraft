#!/usr/bin/env python3
"""
WordPress 精選圖片 (OG Image) 生成器
用於社交媒體分享的 1200x630 圖片
"""

import svgwrite
from pathlib import Path
import re


class OGImageGenerator:
    """OG Image 生成器"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_featured_image(self, title: str, subtitle: str = None, category: str = "技術分析"):
        """
        創建 WordPress 精選圖片

        Args:
            title: 文章標題
            subtitle: 副標題
            category: 文章分類
        """
        output_path = self.output_dir / "featured-image.svg"

        # 標準 OG Image 尺寸
        width = 1200
        height = 630

        dwg = svgwrite.Drawing(str(output_path), size=(width, height))

        # 漸層背景（專業的藍紫漸層）
        gradient = dwg.defs.add(dwg.linearGradient(
            id="bgGradient",
            x1="0%", y1="0%", x2="100%", y2="100%"
        ))
        gradient.add_stop_color(0, '#1e3a8a')  # 深藍
        gradient.add_stop_color(0.5, '#3b82f6')  # 中藍
        gradient.add_stop_color(1, '#8b5cf6')  # 紫色
        dwg.add(dwg.rect((0, 0), (width, height), fill="url(#bgGradient)"))

        # 幾何裝飾元素（增加設計感）
        self._add_geometric_decorations(dwg, width, height)

        # 分類標籤（左上角）
        category_x = 60
        category_y = 60

        dwg.add(dwg.rect(
            (category_x, category_y),
            (len(category) * 20 + 30, 40),
            fill='#ffffff',
            opacity=0.2,
            rx=20
        ))
        dwg.add(dwg.text(
            category,
            insert=(category_x + 15, category_y + 28),
            font_size=18,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 主標題（自動換行）
        title_lines = self._wrap_text(title, max_width=50)
        title_y_start = 200 if len(title_lines) <= 2 else 180

        for idx, line in enumerate(title_lines[:3]):  # 最多3行
            y = title_y_start + idx * 80

            # 標題陰影效果
            dwg.add(dwg.text(
                line,
                insert=(width // 2 + 3, y + 3),
                text_anchor='middle',
                font_size=58 if len(title_lines) <= 2 else 48,
                font_weight='bold',
                fill='#000000',
                opacity=0.3,
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 標題文字
            dwg.add(dwg.text(
                line,
                insert=(width // 2, y),
                text_anchor='middle',
                font_size=58 if len(title_lines) <= 2 else 48,
                font_weight='bold',
                fill='white',
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        # 副標題
        if subtitle:
            subtitle_y = title_y_start + len(title_lines) * 80 + 40
            dwg.add(dwg.text(
                subtitle,
                insert=(width // 2, subtitle_y),
                text_anchor='middle',
                font_size=24,
                fill='#ffffff',
                opacity=0.9,
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        # 品牌標識（底部）
        brand_y = height - 60

        # Logo 圓形
        dwg.add(dwg.circle(
            center=(60, brand_y),
            r=25,
            fill='white',
            opacity=0.9
        ))
        dwg.add(dwg.text(
            '喵',
            insert=(60, brand_y + 10),
            text_anchor='middle',
            font_size=28,
            font_weight='bold',
            fill='#3b82f6',
            font_family='Microsoft JhengHei'
        ))

        # 品牌名稱
        dwg.add(dwg.text(
            '喵哩文創 • 技術部落格',
            insert=(100, brand_y + 8),
            font_size=20,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 底部裝飾線
        dwg.add(dwg.line(
            (width - 400, brand_y),
            (width - 60, brand_y),
            stroke='#ffffff',
            stroke_width=2,
            opacity=0.3
        ))

        dwg.save()
        print(f"✓ 已生成精選圖片: {output_path.name}")

        # 同時生成 PNG 版本（如果需要）
        print(f"💡 提示: SVG 已生成，如需 PNG 請使用:")
        print(f"   npx @squoosh/cli --resize '{{\"enabled\":true,\"width\":1200}}' {output_path}")

    def _add_geometric_decorations(self, dwg, width, height):
        """添加幾何裝飾元素"""
        # 右上角圓圈
        dwg.add(dwg.circle(
            center=(width - 100, 100),
            r=150,
            fill='none',
            stroke='#ffffff',
            stroke_width=3,
            opacity=0.1
        ))

        dwg.add(dwg.circle(
            center=(width - 100, 100),
            r=120,
            fill='none',
            stroke='#ffffff',
            stroke_width=2,
            opacity=0.1
        ))

        # 左下角幾何圖形
        dwg.add(dwg.polygon(
            points=[(50, height - 50), (150, height - 50), (100, height - 150)],
            fill='#ffffff',
            opacity=0.05
        ))

        # 散點裝飾
        dots = [
            (200, 100, 8),
            (width - 300, height - 100, 6),
            (100, height // 2, 5),
            (width - 150, 250, 7)
        ]

        for x, y, r in dots:
            dwg.add(dwg.circle(
                center=(x, y),
                r=r,
                fill='#ffffff',
                opacity=0.2
            ))

    def _wrap_text(self, text: str, max_width: int = 50) -> list:
        """
        智能文字換行

        Args:
            text: 要換行的文字
            max_width: 每行最大字數

        Returns:
            換行後的文字列表
        """
        # 移除特殊字元
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\-:：]', '', text)

        if len(text) <= max_width:
            return [text]

        lines = []
        current_line = ""

        # 優先在標點符號或空格處斷行
        words = text.replace('：', ': ').replace(':', ': ').split()

        for word in words:
            if len(current_line + word) <= max_width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        # 如果沒有空格，強制按字數斷行
        if len(lines) == 0:
            for i in range(0, len(text), max_width):
                lines.append(text[i:i+max_width])

        return lines


def extract_title_from_article(article_path: Path) -> tuple:
    """
    從文章中提取標題和副標題

    Returns:
        (title, subtitle)
    """
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 H1 標題
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = h1_match.group(1) if h1_match else "技術分析"

    # 嘗試提取第一段作為副標題
    lines = content.split('\n')
    subtitle = None
    for line in lines[2:10]:  # 跳過標題，在前幾行中尋找
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('!') and len(line) > 20:
            # 取前50字作為副標題
            subtitle = line[:50] + "..." if len(line) > 50 else line
            break

    return title, subtitle


def main():
    """主函數"""
    import sys

    if len(sys.argv) > 1:
        session_dir = Path(sys.argv[1])
    else:
        session_dir = Path("output/session_20251112_201238")

    article_path = session_dir / "final_article.md"
    images_dir = session_dir / "images"
    images_dir.mkdir(exist_ok=True)

    print("╔════════════════════════════════════════════════════════════╗")
    print("║       🎨 WordPress 精選圖片生成器 🎨                      ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    if not article_path.exists():
        print(f"❌ 找不到文章: {article_path}")
        return

    # 提取標題
    print("📖 分析文章內容...")
    title, subtitle = extract_title_from_article(article_path)
    print(f"  標題: {title}")
    if subtitle:
        print(f"  副標題: {subtitle}")

    # 生成精選圖片
    print("\n🎨 生成精選圖片...")
    generator = OGImageGenerator(images_dir)

    # 根據標題判斷分類
    category = "技術分析"
    if "交易" in title or "機器人" in title:
        category = "量化交易"
    elif "開發" in title or "程式" in title:
        category = "軟體開發"
    elif "AI" in title or "人工智慧" in title:
        category = "人工智慧"

    generator.create_featured_image(title, subtitle, category)

    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                   ✅ 生成完成！                            ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    print("📊 生成檔案:")
    print(f"  - SVG: {images_dir}/featured-image.svg")
    print("\n💡 WordPress 使用:")
    print("  1. 上傳 featured-image.svg 作為精選圖片")
    print("  2. 或使用線上工具轉換為 PNG:")
    print("     https://cloudconvert.com/svg-to-png")


if __name__ == "__main__":
    main()
