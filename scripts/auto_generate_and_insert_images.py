#!/usr/bin/env python3
"""
智能圖片生成和插入系統
自動分析文章內容，生成合適的圖片並插入到對應位置
"""

import os
import re
import json
import subprocess
from typing import List, Dict, Tuple
from pathlib import Path


class SmartImageGenerator:
    """智能圖片生成器"""

    def __init__(self, session_dir: str):
        self.session_dir = Path(session_dir)
        self.article_path = self.session_dir / "final_article.md"
        self.images_dir = self.session_dir / "images"
        self.mermaid_dir = self.session_dir / "mermaid_diagrams"

        # 確保目錄存在
        self.images_dir.mkdir(exist_ok=True)
        self.mermaid_dir.mkdir(exist_ok=True)

        self.image_rules = []

    def analyze_article_content(self) -> Dict:
        """分析文章內容，識別需要圖片的位置"""
        with open(self.article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分析文章結構
        headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

        analysis = {
            'headings': headings,
            'word_count': len(content.split()),
            'has_code_blocks': '```' in content,
            'has_tables': '|' in content,
            'topic': self._identify_topic(content)
        }

        return analysis

    def _identify_topic(self, content: str) -> str:
        """識別文章主題"""
        # 簡單的關鍵字匹配
        if any(kw in content for kw in ['交易', '機器人', 'trading', 'bot']):
            return 'trading'
        elif any(kw in content for kw in ['API', '開發', 'code', '程式']):
            return 'development'
        elif any(kw in content for kw in ['分析', '數據', 'analytics']):
            return 'analytics'
        return 'general'

    def generate_trading_bot_images(self):
        """為交易機器人文章生成專用圖片"""

        # 1. 系統架構圖
        self._create_mermaid_diagram(
            'system-architecture',
            """graph TB
    A[用戶配置] --> B[API Layer]
    B --> C[Services Layer]
    C --> D[Domain Layer]
    D --> E[Adapter Layer]
    E --> F1[Binance API]
    E --> F2[OKX API]
    E --> F3[Hyperliquid API]
    C --> G[Event Bus]
    G --> H1[網格交易]
    G --> H2[套利監控]
    G --> H3[價格提醒]

    style A fill:#e1f5ff
    style B fill:#fff9c4
    style C fill:#f8bbd0
    style D fill:#dcedc8
    style E fill:#ffe0b2
    style G fill:#b2dfdb
""",
            "crypto-trading-open 系統架構圖"
        )

        # 2. 網格交易流程圖
        self._create_mermaid_diagram(
            'grid-trading-flow',
            """flowchart TD
    Start([開始網格交易]) --> Config[讀取配置參數]
    Config --> Validate{驗證參數}
    Validate -->|失敗| Error[返回錯誤]
    Validate -->|成功| Connect[連接交易所]
    Connect --> Price[獲取當前價格]
    Price --> Calculate[計算網格參數]
    Calculate --> Place[下單網格訂單]
    Place --> Monitor[監控訂單狀態]
    Monitor --> Check{訂單成交?}
    Check -->|是| Execute[執行對應策略]
    Check -->|否| Wait[等待]
    Execute --> Log[記錄交易]
    Log --> Monitor
    Wait --> Monitor

    style Start fill:#4caf50,color:#fff
    style Error fill:#f44336,color:#fff
    style Execute fill:#2196f3,color:#fff
""",
            "網格交易執行流程"
        )

        # 3. 比較圖表 (使用 SVG)
        self._create_comparison_chart()

        # 4. 風險評估圖表
        self._create_risk_assessment_chart()

        # 5. 功能對比表格圖
        self._create_feature_comparison_svg()

    def _create_mermaid_diagram(self, filename: str, diagram_code: str, description: str):
        """創建 Mermaid 流程圖"""
        mmd_file = self.mermaid_dir / f"{filename}.mmd"
        png_file = self.images_dir / f"{filename}.png"

        # 寫入 Mermaid 文件
        with open(mmd_file, 'w', encoding='utf-8') as f:
            f.write(diagram_code)

        # 使用 mermaid-cli 生成圖片
        try:
            subprocess.run([
                'npx', 'mmdc',
                '-i', str(mmd_file),
                '-o', str(png_file),
                '-w', '1200',
                '-H', '800',
                '-b', 'white'
            ], check=True, capture_output=True, text=True)

            print(f"✓ 已生成 Mermaid 圖表: {filename}.png")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Mermaid 圖表生成失敗: {filename}")
            print(f"  錯誤: {e.stderr}")
            return False
        except FileNotFoundError:
            print("✗ 未找到 mermaid-cli (mmdc)，請先安裝:")
            print("  npm install -g @mermaid-js/mermaid-cli")
            return False

    def _create_comparison_chart(self):
        """創建比較圖表 (Python SVG)"""
        import svgwrite

        output_path = self.images_dir / "tool-comparison.svg"

        dwg = svgwrite.Drawing(str(output_path), size=(1200, 600))

        # 背景
        dwg.add(dwg.rect((0, 0), (1200, 600), fill='#f8f9fa'))

        # 標題
        dwg.add(dwg.text(
            '開源交易機器人對比',
            insert=(600, 50),
            text_anchor='middle',
            font_size=36,
            font_weight='bold',
            fill='#1a1a1a'
        ))

        # 數據
        tools = ['crypto-trading-open', 'Freqtrade', 'Hummingbot', 'OctoBot']
        metrics = {
            '代碼品質': [5, 4, 5, 3],
            '易用性': [3, 4, 3, 5],
            '社群規模': [2, 5, 4, 3],
            '功能完整度': [4, 4, 5, 3]
        }

        colors = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0']

        # 繪製雷達圖風格的比較
        y_offset = 120
        bar_height = 40

        for i, (metric, values) in enumerate(metrics.items()):
            y = y_offset + i * 100

            # 指標名稱
            dwg.add(dwg.text(
                metric,
                insert=(100, y + 25),
                font_size=18,
                fill='#333'
            ))

            # 繪製長條圖
            for j, (tool, value) in enumerate(zip(tools, values)):
                bar_y = y + j * (bar_height + 5)
                bar_width = value * 160  # 最大 5 分 = 800px

                # 長條
                dwg.add(dwg.rect(
                    (300, bar_y),
                    (bar_width, bar_height - 5),
                    fill=colors[j],
                    opacity=0.8,
                    rx=5
                ))

                # 分數標籤
                dwg.add(dwg.text(
                    f'{value}/5',
                    insert=(300 + bar_width + 10, bar_y + 25),
                    font_size=16,
                    fill='#666'
                ))

        # 圖例
        legend_y = 560
        for i, (tool, color) in enumerate(zip(tools, colors)):
            legend_x = 150 + i * 250

            dwg.add(dwg.rect(
                (legend_x, legend_y),
                (20, 20),
                fill=color,
                rx=3
            ))

            dwg.add(dwg.text(
                tool,
                insert=(legend_x + 30, legend_y + 15),
                font_size=14,
                fill='#333'
            ))

        dwg.save()
        print("✓ 已生成 SVG 比較圖表: tool-comparison.svg")

    def _create_risk_assessment_chart(self):
        """創建風險評估圖表"""
        import svgwrite

        output_path = self.images_dir / "risk-assessment.svg"

        dwg = svgwrite.Drawing(str(output_path), size=(1000, 500))

        # 背景
        dwg.add(dwg.rect((0, 0), (1000, 500), fill='#ffffff'))

        # 標題
        dwg.add(dwg.text(
            '交易機器人風險等級評估',
            insert=(500, 50),
            text_anchor='middle',
            font_size=32,
            font_weight='bold',
            fill='#1a1a1a'
        ))

        # 風險等級
        risks = [
            ('技術風險', 7, '#ff5722'),
            ('市場風險', 9, '#f44336'),
            ('配置錯誤', 6, '#ff9800'),
            ('安全風險', 8, '#e91e63'),
            ('法律風險', 5, '#ffc107')
        ]

        y_start = 120

        for i, (risk_name, level, color) in enumerate(risks):
            y = y_start + i * 70

            # 風險名稱
            dwg.add(dwg.text(
                risk_name,
                insert=(100, y + 30),
                font_size=20,
                fill='#333'
            ))

            # 風險等級條
            max_width = 600
            bar_width = (level / 10) * max_width

            # 背景條
            dwg.add(dwg.rect(
                (300, y + 10),
                (max_width, 30),
                fill='#e0e0e0',
                rx=15
            ))

            # 風險條
            dwg.add(dwg.rect(
                (300, y + 10),
                (bar_width, 30),
                fill=color,
                rx=15
            ))

            # 分數
            dwg.add(dwg.text(
                f'{level}/10',
                insert=(910, y + 30),
                font_size=18,
                font_weight='bold',
                fill=color
            ))

        dwg.save()
        print("✓ 已生成風險評估圖表: risk-assessment.svg")

    def _create_feature_comparison_svg(self):
        """創建功能對比 SVG 圖表"""
        import svgwrite

        output_path = self.images_dir / "feature-matrix.svg"

        dwg = svgwrite.Drawing(str(output_path), size=(1200, 800))

        # 背景
        dwg.add(dwg.rect((0, 0), (1200, 800), fill='#f5f5f5'))

        # 標題
        dwg.add(dwg.text(
            'crypto-trading-open 功能矩陣',
            insert=(600, 50),
            text_anchor='middle',
            font_size=36,
            font_weight='bold',
            fill='#1a1a1a'
        ))

        # 功能列表
        features = [
            {'name': '網格交易', 'modes': 7, 'difficulty': '中', 'color': '#4caf50'},
            {'name': '虛擬網格模擬', 'modes': 1, 'difficulty': '低', 'color': '#2196f3'},
            {'name': '刷量交易', 'modes': 2, 'difficulty': '高', 'color': '#ff9800'},
            {'name': '套利監控', 'modes': 3, 'difficulty': '中', 'color': '#9c27b0'},
            {'name': '價格提醒', 'modes': 1, 'difficulty': '低', 'color': '#00bcd4'},
        ]

        # 繪製功能卡片
        card_width = 220
        card_height = 180
        x_start = 80
        y_start = 120

        for i, feature in enumerate(features):
            row = i // 5
            col = i % 5

            x = x_start + col * (card_width + 20)
            y = y_start + row * (card_height + 20)

            # 卡片背景
            dwg.add(dwg.rect(
                (x, y),
                (card_width, card_height),
                fill='white',
                stroke=feature['color'],
                stroke_width=3,
                rx=10
            ))

            # 功能名稱
            dwg.add(dwg.text(
                feature['name'],
                insert=(x + card_width/2, y + 40),
                text_anchor='middle',
                font_size=20,
                font_weight='bold',
                fill=feature['color']
            ))

            # 模式數量
            dwg.add(dwg.text(
                f"模式數: {feature['modes']}",
                insert=(x + 20, y + 80),
                font_size=16,
                fill='#666'
            ))

            # 難度等級
            difficulty_colors = {'低': '#4caf50', '中': '#ff9800', '高': '#f44336'}
            dwg.add(dwg.text(
                f"難度: {feature['difficulty']}",
                insert=(x + 20, y + 110),
                font_size=16,
                fill=difficulty_colors[feature['difficulty']]
            ))

            # 支援標記
            dwg.add(dwg.circle(
                center=(x + card_width - 30, y + 30),
                r=15,
                fill='#4caf50'
            ))
            dwg.add(dwg.text(
                '✓',
                insert=(x + card_width - 30, y + 36),
                text_anchor='middle',
                font_size=20,
                fill='white',
                font_weight='bold'
            ))

        # 圖例
        legend_items = [
            ('✓ 完整支援', '#4caf50'),
            ('難度等級: 低/中/高', '#666')
        ]

        for i, (text, color) in enumerate(legend_items):
            dwg.add(dwg.text(
                text,
                insert=(100, 720 + i * 30),
                font_size=16,
                fill=color
            ))

        dwg.save()
        print("✓ 已生成功能矩陣圖表: feature-matrix.svg")

    def define_insertion_rules(self):
        """定義圖片插入規則"""
        self.image_rules = [
            {
                'after_heading': '## 二、技術架構深度分析',
                'image': 'system-architecture.png',
                'alt': 'crypto-trading-open 系統架構圖',
                'caption': '*crypto-trading-open 的分層架構設計*'
            },
            {
                'after_heading': '### 1. 網格交易系統：七種模式任你選',
                'image': 'grid-trading-flow.png',
                'alt': '網格交易執行流程圖',
                'caption': '*網格交易的完整執行流程*'
            },
            {
                'after_heading': '## 五、與其他開源工具的對比',
                'image': 'tool-comparison.svg',
                'alt': '開源交易機器人對比',
                'caption': '*crypto-trading-open 與其他主流工具的多維度比較*'
            },
            {
                'after_heading': '### 競品對比總表',
                'image': 'feature-matrix.svg',
                'alt': 'crypto-trading-open 功能矩陣',
                'caption': '*crypto-trading-open 的完整功能列表*'
            },
            {
                'after_heading': '## 八、風險與注意事項',
                'image': 'risk-assessment.svg',
                'alt': '交易機器人風險等級評估',
                'caption': '*使用交易機器人的各類風險評估*'
            }
        ]

    def insert_images_to_article(self):
        """將圖片插入到文章中"""
        with open(self.article_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        modified_lines = []
        images_inserted = 0

        i = 0
        while i < len(lines):
            line = lines[i]
            modified_lines.append(line)

            # 檢查是否匹配插入規則
            for rule in self.image_rules:
                heading = rule['after_heading']

                if line.strip() == heading.strip():
                    image_filename = rule['image']

                    # 檢查圖片是否已存在
                    next_lines = '\n'.join(lines[i:min(i+10, len(lines))])
                    if image_filename not in next_lines:
                        # 插入圖片
                        image_markdown = f"\n\n![{rule['alt']}](images/{image_filename})\n{rule['caption']}\n\n"
                        modified_lines.append(image_markdown)
                        images_inserted += 1
                        print(f"  ✓ 已在「{heading[:40]}...」後插入圖片: {image_filename}")

            i += 1

        # 備份原文章
        backup_path = str(self.article_path).replace('.md', '_backup.md')
        with open(self.article_path, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        print(f"✓ 原文章已備份至: {Path(backup_path).name}")

        # 寫入新內容
        new_content = '\n'.join(modified_lines)
        with open(self.article_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return images_inserted

    def generate_image_index(self):
        """生成圖片索引文件"""
        index_data = {
            'session': str(self.session_dir),
            'total_images': len(list(self.images_dir.glob('*'))),
            'images': []
        }

        for img_file in self.images_dir.glob('*'):
            if img_file.suffix in ['.png', '.svg', '.jpg']:
                index_data['images'].append({
                    'filename': img_file.name,
                    'format': img_file.suffix[1:],
                    'size': img_file.stat().st_size
                })

        index_path = self.images_dir / 'image-index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        print(f"✓ 已生成圖片索引: {index_path.name}")

    def run(self):
        """執行完整流程"""
        print("╔════════════════════════════════════════════════════════════╗")
        print("║       🎨 智能圖片生成和插入系統 v2.0 🎨                   ║")
        print("╚════════════════════════════════════════════════════════════╝\n")

        # 1. 分析文章
        print("📊 步驟 1/5: 分析文章內容...")
        analysis = self.analyze_article_content()
        print(f"  - 文章主題: {analysis['topic']}")
        print(f"  - 總字數: {analysis['word_count']}")
        print(f"  - 標題數量: {len(analysis['headings'])}")
        print()

        # 2. 生成圖片
        print("🎨 步驟 2/5: 生成專用圖片...")
        if analysis['topic'] == 'trading':
            self.generate_trading_bot_images()
        print()

        # 3. 定義插入規則
        print("📋 步驟 3/5: 定義插入規則...")
        self.define_insertion_rules()
        print(f"  - 共定義 {len(self.image_rules)} 個插入點")
        print()

        # 4. 插入圖片
        print("📝 步驟 4/5: 插入圖片到文章...")
        images_inserted = self.insert_images_to_article()
        print(f"  - 共插入 {images_inserted} 張圖片")
        print()

        # 5. 生成索引
        print("📑 步驟 5/5: 生成圖片索引...")
        self.generate_image_index()
        print()

        print("╔════════════════════════════════════════════════════════════╗")
        print("║                   ✅ 處理完成！                            ║")
        print("╚════════════════════════════════════════════════════════════╝\n")

        print("📊 處理摘要:")
        print(f"  - 文章路徑: {self.article_path}")
        print(f"  - 圖片目錄: {self.images_dir}")
        print(f"  - 插入圖片: {images_inserted} 張")
        print(f"  - 原文備份: {self.article_path.name.replace('.md', '_backup.md')}")
        print()
        print("💡 下一步:")
        print("  1. 檢查文章中的圖片位置是否合適")
        print("  2. 確認所有圖片都已正確生成")
        print("  3. 準備發布到 WordPress")


def main():
    """主函數"""
    import sys

    if len(sys.argv) > 1:
        session_dir = sys.argv[1]
    else:
        # 默認使用最新的 session
        base_dir = Path(__file__).parent.parent
        output_dir = base_dir / 'output'

        # 查找最新的 session
        sessions = sorted(output_dir.glob('session_*'), reverse=True)
        if not sessions:
            print("❌ 找不到任何 session 目錄")
            return

        session_dir = sessions[0]
        print(f"📁 使用最新 session: {session_dir.name}\n")

    # 執行圖片生成和插入
    generator = SmartImageGenerator(session_dir)
    generator.run()


if __name__ == "__main__":
    main()
