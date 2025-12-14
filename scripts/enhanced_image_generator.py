#!/usr/bin/env python3
"""
增強版圖片生成器 v2.1
專注於美觀、專業的圖表設計
"""

import svgwrite
from pathlib import Path


class EnhancedChartGenerator:
    """增強版圖表生成器 - 現代化設計"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

        # 現代化配色方案
        self.colors = {
            'primary': '#2563eb',      # 藍色
            'success': '#10b981',      # 綠色
            'warning': '#f59e0b',      # 橙色
            'danger': '#ef4444',       # 紅色
            'purple': '#8b5cf6',       # 紫色
            'gray': {
                '50': '#f9fafb',
                '100': '#f3f4f6',
                '200': '#e5e7eb',
                '300': '#d1d5db',
                '600': '#4b5563',
                '900': '#111827'
            }
        }

    def create_modern_tool_comparison(self):
        """創建現代化的工具比較雷達圖"""
        output_path = self.output_dir / "tool-comparison.svg"

        dwg = svgwrite.Drawing(str(output_path), size=(1200, 700))

        # 漸層背景
        gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, self.colors['gray']['50'])
        gradient.add_stop_color(1, '#fff')
        dwg.add(dwg.rect((0, 0), (1200, 700), fill="url(#bgGradient)"))

        # 標題區域
        dwg.add(dwg.text(
            '開源交易機器人多維度對比',
            insert=(600, 50),
            text_anchor='middle',
            font_size=32,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 副標題
        dwg.add(dwg.text(
            '代碼品質、易用性、社群規模、功能完整度全方位比較',
            insert=(600, 80),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 數據
        metrics = ['代碼品質', '易用性', '社群規模', '功能完整度']
        tools_data = {
            'crypto-trading-open': {
                'values': [5, 3, 2, 4],
                'color': self.colors['success']
            },
            'Freqtrade': {
                'values': [4, 4, 5, 4],
                'color': self.colors['primary']
            },
            'Hummingbot': {
                'values': [5, 3, 4, 5],
                'color': self.colors['warning']
            },
            'OctoBot': {
                'values': [3, 5, 3, 3],
                'color': self.colors['purple']
            }
        }

        # 繪製分組長條圖
        chart_x = 100
        chart_y = 140
        chart_width = 1000
        chart_height = 400

        # 網格線
        for i in range(6):
            y = chart_y + chart_height - (i * chart_height / 5)
            dwg.add(dwg.line(
                (chart_x, y),
                (chart_x + chart_width, y),
                stroke=self.colors['gray']['200'],
                stroke_width=1,
                stroke_dasharray="4,4"
            ))
            dwg.add(dwg.text(
                str(i),
                insert=(chart_x - 30, y + 5),
                text_anchor='middle',
                font_size=12,
                fill=self.colors['gray']['600']
            ))

        # 繪製長條圖
        metric_width = chart_width / len(metrics)
        bar_width = 50
        bar_spacing = 10

        for metric_idx, metric in enumerate(metrics):
            metric_x = chart_x + metric_idx * metric_width + metric_width / 2

            # 指標標籤
            dwg.add(dwg.text(
                metric,
                insert=(metric_x, chart_y + chart_height + 30),
                text_anchor='middle',
                font_size=14,
                font_weight='bold',
                fill=self.colors['gray']['900']
            ))

            # 繪製每個工具的長條
            tool_idx = 0
            for tool_name, tool_data in tools_data.items():
                value = tool_data['values'][metric_idx]
                color = tool_data['color']

                bar_height = (value / 5) * chart_height
                bar_x = metric_x - (len(tools_data) * (bar_width + bar_spacing)) / 2 + tool_idx * (bar_width + bar_spacing)
                bar_y = chart_y + chart_height - bar_height

                # 長條（帶陰影）
                shadow = dwg.rect(
                    (bar_x + 2, bar_y + 2),
                    (bar_width, bar_height),
                    fill='#e5e7eb',
                    rx=4
                )
                dwg.add(shadow)

                bar = dwg.rect(
                    (bar_x, bar_y),
                    (bar_width, bar_height),
                    fill=color,
                    rx=4,
                    opacity=0.9
                )
                dwg.add(bar)

                # 數值標籤
                dwg.add(dwg.text(
                    f'{value}',
                    insert=(bar_x + bar_width / 2, bar_y - 8),
                    text_anchor='middle',
                    font_size=13,
                    font_weight='bold',
                    fill=color
                ))

                tool_idx += 1

        # 圖例
        legend_y = chart_y + chart_height + 70
        legend_x_start = 300

        for idx, (tool_name, tool_data) in enumerate(tools_data.items()):
            legend_x = legend_x_start + idx * 200

            # 色塊
            dwg.add(dwg.rect(
                (legend_x, legend_y),
                (30, 20),
                fill=tool_data['color'],
                rx=4,
                opacity=0.9
            ))

            # 名稱
            dwg.add(dwg.text(
                tool_name,
                insert=(legend_x + 40, legend_y + 15),
                font_size=13,
                fill=self.colors['gray']['900'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        dwg.save()
        print(f"✓ 已生成現代化比較圖表: {output_path.name}")

    def create_modern_risk_assessment(self):
        """創建現代化的風險評估圖"""
        output_path = self.output_dir / "risk-assessment.svg"

        dwg = svgwrite.Drawing(str(output_path), size=(1200, 600))

        # 背景
        gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient2", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#ffffff')
        gradient.add_stop_color(1, self.colors['gray']['50'])
        dwg.add(dwg.rect((0, 0), (1200, 600), fill="url(#bgGradient2)"))

        # 標題
        dwg.add(dwg.text(
            '交易機器人風險等級評估',
            insert=(600, 50),
            text_anchor='middle',
            font_size=32,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            '各類風險的嚴重程度評估（10分制，分數越高風險越大）',
            insert=(600, 80),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 風險數據
        risks = [
            {'name': '技術風險', 'level': 7, 'icon': '⚙️', 'desc': '系統故障、網路中斷'},
            {'name': '市場風險', 'level': 9, 'icon': '📉', 'desc': '黑天鵝事件、流動性不足'},
            {'name': '配置錯誤', 'level': 6, 'icon': '🔧', 'desc': '參數設定不當、權限錯誤'},
            {'name': '安全風險', 'level': 8, 'icon': '🔒', 'desc': 'API 金鑰洩露、帳號被盜'},
            {'name': '法律風險', 'level': 5, 'icon': '⚖️', 'desc': '監管不確定性、合規要求'}
        ]

        # 繪製風險條
        y_start = 140
        bar_height = 70
        max_bar_width = 900

        for idx, risk in enumerate(risks):
            y = y_start + idx * bar_height

            # 圖示和名稱
            dwg.add(dwg.text(
                f"{risk['icon']} {risk['name']}",
                insert=(80, y + 30),
                font_size=18,
                font_weight='bold',
                fill=self.colors['gray']['900'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 說明文字
            dwg.add(dwg.text(
                risk['desc'],
                insert=(80, y + 50),
                font_size=12,
                fill=self.colors['gray']['600'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 背景條
            dwg.add(dwg.rect(
                (280, y + 10),
                (max_bar_width, 40),
                fill=self.colors['gray']['100'],
                rx=20
            ))

            # 風險條（漸層）
            bar_width = (risk['level'] / 10) * max_bar_width
            risk_color = self._get_risk_color(risk['level'])

            gradient_id = f"riskGradient{idx}"
            risk_gradient = dwg.defs.add(dwg.linearGradient(id=gradient_id, x1="0%", y1="0%", x2="100%", y2="0%"))
            risk_gradient.add_stop_color(0, risk_color)
            risk_gradient.add_stop_color(1, self._lighten_color(risk_color))

            dwg.add(dwg.rect(
                (280, y + 10),
                (bar_width, 40),
                fill=f"url(#{gradient_id})",
                rx=20
            ))

            # 分數標籤
            score_x = 280 + bar_width + 20
            dwg.add(dwg.text(
                f'{risk["level"]}/10',
                insert=(score_x, y + 35),
                font_size=20,
                font_weight='bold',
                fill=risk_color,
                font_family='Arial, sans-serif'
            ))

        # 底部說明
        dwg.add(dwg.text(
            '💡 建議：實施嚴格的風險管理措施，不要投入超過可承受損失的資金',
            insert=(600, 570),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['primary'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成現代化風險評估圖: {output_path.name}")

    def create_modern_feature_matrix(self):
        """創建現代化的功能矩陣圖"""
        output_path = self.output_dir / "feature-matrix.svg"

        dwg = svgwrite.Drawing(str(output_path), size=(1200, 700))

        # 背景
        dwg.add(dwg.rect((0, 0), (1200, 700), fill=self.colors['gray']['50']))

        # 標題
        dwg.add(dwg.text(
            'crypto-trading-open 功能矩陣',
            insert=(600, 50),
            text_anchor='middle',
            font_size=32,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 功能數據
        features = [
            {
                'name': '網格交易',
                'icon': '📊',
                'modes': 7,
                'difficulty': '中',
                'color': self.colors['success'],
                'desc': '支援 7 種網格模式'
            },
            {
                'name': '虛擬網格模擬',
                'icon': '🎮',
                'modes': 1,
                'difficulty': '低',
                'color': self.colors['primary'],
                'desc': '零風險策略測試'
            },
            {
                'name': '刷量交易',
                'icon': '💹',
                'modes': 2,
                'difficulty': '高',
                'color': self.colors['warning'],
                'desc': '限價單/市價單模式'
            },
            {
                'name': '套利監控',
                'icon': '🔍',
                'modes': 3,
                'difficulty': '中',
                'color': self.colors['purple'],
                'desc': '跨交易所套利機會'
            },
            {
                'name': '價格提醒',
                'icon': '🔔',
                'modes': 1,
                'difficulty': '低',
                'color': '#06b6d4',
                'desc': '實時價格監控'
            }
        ]

        # 繪製功能卡片（2行3列佈局）
        card_width = 350
        card_height = 200
        gap = 30
        start_x = 75
        start_y = 120

        for idx, feature in enumerate(features):
            row = idx // 3
            col = idx % 3

            card_x = start_x + col * (card_width + gap)
            card_y = start_y + row * (card_height + gap)

            # 卡片陰影
            dwg.add(dwg.rect(
                (card_x + 4, card_y + 4),
                (card_width, card_height),
                fill='#d1d5db',
                rx=12
            ))

            # 卡片背景
            dwg.add(dwg.rect(
                (card_x, card_y),
                (card_width, card_height),
                fill='white',
                stroke=feature['color'],
                stroke_width=2,
                rx=12
            ))

            # 頂部色帶
            dwg.add(dwg.rect(
                (card_x, card_y),
                (card_width, 8),
                fill=feature['color'],
                rx=12
            ))

            # 圖示和功能名稱
            dwg.add(dwg.text(
                f"{feature['icon']} {feature['name']}",
                insert=(card_x + 20, card_y + 50),
                font_size=22,
                font_weight='bold',
                fill=self.colors['gray']['900'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 說明
            dwg.add(dwg.text(
                feature['desc'],
                insert=(card_x + 20, card_y + 80),
                font_size=14,
                fill=self.colors['gray']['600'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 模式數量標籤
            dwg.add(dwg.rect(
                (card_x + 20, card_y + 105),
                (150, 30),
                fill=self.colors['gray']['100'],
                rx=6
            ))
            dwg.add(dwg.text(
                f"支援模式: {feature['modes']} 種",
                insert=(card_x + 30, card_y + 125),
                font_size=13,
                fill=self.colors['gray']['900'],
                font_family='Arial, sans-serif'
            ))

            # 難度標籤
            difficulty_colors = {'低': self.colors['success'], '中': self.colors['warning'], '高': self.colors['danger']}
            dwg.add(dwg.rect(
                (card_x + 190, card_y + 105),
                (140, 30),
                fill=difficulty_colors[feature['difficulty']],
                rx=6,
                opacity=0.15
            ))
            dwg.add(dwg.text(
                f"難度: {feature['difficulty']}",
                insert=(card_x + 200, card_y + 125),
                font_size=13,
                font_weight='bold',
                fill=difficulty_colors[feature['difficulty']],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 支援標記
            dwg.add(dwg.circle(
                center=(card_x + card_width - 30, card_y + 30),
                r=18,
                fill=self.colors['success']
            ))
            dwg.add(dwg.text(
                '✓',
                insert=(card_x + card_width - 30, card_y + 36),
                text_anchor='middle',
                font_size=22,
                font_weight='bold',
                fill='white'
            ))

        # 底部統計
        stats_y = start_y + 2 * (card_height + gap) + 20
        dwg.add(dwg.text(
            '🎯 完整支援 5 大核心功能 • 總計 14 種交易模式 • 支援 6 大交易所',
            insert=(600, stats_y),
            text_anchor='middle',
            font_size=15,
            font_weight='bold',
            fill=self.colors['primary'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成現代化功能矩陣圖: {output_path.name}")

    def _get_risk_color(self, level):
        """根據風險等級返回顏色"""
        if level >= 8:
            return self.colors['danger']
        elif level >= 6:
            return self.colors['warning']
        else:
            return self.colors['success']

    def _lighten_color(self, color):
        """將顏色變淺"""
        # 簡單實現：返回稍微不同的顏色
        color_map = {
            self.colors['danger']: '#fca5a5',
            self.colors['warning']: '#fbbf24',
            self.colors['success']: '#6ee7b7',
            self.colors['primary']: '#93c5fd',
            self.colors['purple']: '#c4b5fd'
        }
        return color_map.get(color, color)


def main():
    """主函數"""
    import sys

    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1]) / "images"
    else:
        output_dir = Path("output/session_20251112_201238/images")

    output_dir.mkdir(parents=True, exist_ok=True)

    print("╔════════════════════════════════════════════════════════════╗")
    print("║         🎨 增強版圖片生成器 v2.1 🎨                       ║")
    print("║         現代化、專業、美觀的圖表設計                      ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    generator = EnhancedChartGenerator(output_dir)

    print("🎨 生成現代化圖表...")
    generator.create_modern_tool_comparison()
    generator.create_modern_risk_assessment()
    generator.create_modern_feature_matrix()

    print("\n✅ 所有圖表已生成完成！")
    print(f"📁 輸出目錄: {output_dir}")


if __name__ == "__main__":
    main()
