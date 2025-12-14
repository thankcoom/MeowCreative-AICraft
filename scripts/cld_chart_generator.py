#!/usr/bin/env python3
"""
CLD 因果循環圖 SVG 生成器
為 CLD 入門教學文章生成專業的系統思考圖表
"""

import svgwrite
from pathlib import Path
import math


class CLDChartGenerator:
    """CLD 專用圖表生成器"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

        # 配色方案
        self.colors = {
            'primary': '#2563eb',      # 藍色
            'success': '#10b981',      # 綠色 (正向)
            'danger': '#ef4444',       # 紅色 (負向)
            'warning': '#f59e0b',      # 橙色
            'purple': '#8b5cf6',       # 紫色
            'reinforcing': '#ef4444',  # 增強迴路 R
            'balancing': '#3b82f6',    # 平衡迴路 B
            'gray': {
                '50': '#f9fafb',
                '100': '#f3f4f6',
                '200': '#e5e7eb',
                '300': '#d1d5db',
                '500': '#6b7280',
                '600': '#4b5563',
                '900': '#111827'
            }
        }

    def _draw_arrow(self, dwg, start, end, color, sign=None, curved=False):
        """繪製帶箭頭的連接線"""
        x1, y1 = start
        x2, y2 = end

        # 計算箭頭方向
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_length = 12
        arrow_angle = math.pi / 6

        # 縮短終點以留出箭頭空間
        end_offset = 20
        x2_adj = x2 - end_offset * math.cos(angle)
        y2_adj = y2 - end_offset * math.sin(angle)

        if curved:
            # 曲線路徑
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2 - 30
            path_d = f"M {x1} {y1} Q {mid_x} {mid_y} {x2_adj} {y2_adj}"
            dwg.add(dwg.path(d=path_d, stroke=color, stroke_width=2.5, fill='none'))
        else:
            # 直線
            dwg.add(dwg.line((x1, y1), (x2_adj, y2_adj), stroke=color, stroke_width=2.5))

        # 箭頭
        arrow_x1 = x2_adj - arrow_length * math.cos(angle - arrow_angle)
        arrow_y1 = y2_adj - arrow_length * math.sin(angle - arrow_angle)
        arrow_x2 = x2_adj - arrow_length * math.cos(angle + arrow_angle)
        arrow_y2 = y2_adj - arrow_length * math.sin(angle + arrow_angle)

        dwg.add(dwg.polygon(
            [(x2_adj, y2_adj), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
            fill=color
        ))

        # 符號 (+/-)
        if sign:
            sign_x = (x1 + x2_adj) / 2 + 15
            sign_y = (y1 + y2_adj) / 2 - 10
            sign_color = self.colors['success'] if sign == '+' else self.colors['danger']

            dwg.add(dwg.circle(
                center=(sign_x, sign_y),
                r=12,
                fill='white',
                stroke=sign_color,
                stroke_width=2
            ))
            dwg.add(dwg.text(
                sign,
                insert=(sign_x, sign_y + 5),
                text_anchor='middle',
                font_size=16,
                font_weight='bold',
                fill=sign_color
            ))

    def _draw_variable_node(self, dwg, x, y, text, color=None):
        """繪製變數節點"""
        color = color or self.colors['primary']
        text_width = len(text) * 14 + 30
        rect_height = 40

        # 陰影
        dwg.add(dwg.rect(
            (x - text_width/2 + 3, y - rect_height/2 + 3),
            (text_width, rect_height),
            fill='#d1d5db',
            rx=8
        ))

        # 節點
        dwg.add(dwg.rect(
            (x - text_width/2, y - rect_height/2),
            (text_width, rect_height),
            fill='white',
            stroke=color,
            stroke_width=2.5,
            rx=8
        ))

        # 文字
        dwg.add(dwg.text(
            text,
            insert=(x, y + 6),
            text_anchor='middle',
            font_size=16,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

    def create_cld_elements(self):
        """創建 CLD 四大元素說明圖"""
        output_path = self.output_dir / "cld-elements.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1200, 600))

        # 背景
        gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#f8fafc')
        gradient.add_stop_color(1, '#f1f5f9')
        dwg.add(dwg.rect((0, 0), (1200, 600), fill="url(#bgGradient)"))

        # 標題
        dwg.add(dwg.text(
            'CLD 因果循環圖：四大基本元素',
            insert=(600, 50),
            text_anchor='middle',
            font_size=32,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 四個元素區塊
        elements = [
            {
                'title': '1. 變數 (Variable)',
                'desc': '會變化的事物',
                'example': '壓力、體重、收入',
                'color': self.colors['primary']
            },
            {
                'title': '2. 連接 (Link)',
                'desc': '因果關係箭頭',
                'example': 'A → B',
                'color': self.colors['purple']
            },
            {
                'title': '3. 極性符號 (+/-)',
                'desc': '+同向 / -反向',
                'example': '運動↑ → 健康↑(+)',
                'color': self.colors['success']
            },
            {
                'title': '4. 迴路標記 (R/B)',
                'desc': 'R增強 / B平衡',
                'example': '滾雪球 vs 恆溫器',
                'color': self.colors['warning']
            }
        ]

        card_width = 260
        card_height = 180
        start_x = 80
        start_y = 100

        for idx, elem in enumerate(elements):
            x = start_x + idx * (card_width + 30)
            y = start_y

            # 卡片陰影
            dwg.add(dwg.rect(
                (x + 4, y + 4),
                (card_width, card_height),
                fill='#d1d5db',
                rx=16
            ))

            # 卡片
            dwg.add(dwg.rect(
                (x, y),
                (card_width, card_height),
                fill='white',
                stroke=elem['color'],
                stroke_width=3,
                rx=16
            ))

            # 頂部色帶
            dwg.add(dwg.rect(
                (x, y),
                (card_width, 10),
                fill=elem['color'],
                rx=16
            ))
            dwg.add(dwg.rect(
                (x, y + 5),
                (card_width, 8),
                fill=elem['color']
            ))

            # 標題
            dwg.add(dwg.text(
                elem['title'],
                insert=(x + card_width/2, y + 50),
                text_anchor='middle',
                font_size=18,
                font_weight='bold',
                fill=self.colors['gray']['900'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 說明
            dwg.add(dwg.text(
                elem['desc'],
                insert=(x + card_width/2, y + 85),
                text_anchor='middle',
                font_size=14,
                fill=self.colors['gray']['600'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 範例
            dwg.add(dwg.rect(
                (x + 20, y + 110),
                (card_width - 40, 45),
                fill=self.colors['gray']['100'],
                rx=8
            ))
            dwg.add(dwg.text(
                elem['example'],
                insert=(x + card_width/2, y + 140),
                text_anchor='middle',
                font_size=14,
                fill=elem['color'],
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        # 示範圖 (簡單的 CLD)
        demo_y = 330
        dwg.add(dwg.text(
            '實際範例：學習的正向循環',
            insert=(600, demo_y),
            text_anchor='middle',
            font_size=20,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 繪製簡單的增強迴路
        nodes = [
            (350, demo_y + 100, '學習時間'),
            (600, demo_y + 50, '能力提升'),
            (850, demo_y + 100, '成就感'),
            (600, demo_y + 180, '動力')
        ]

        # 畫節點
        for x, y, text in nodes:
            self._draw_variable_node(dwg, x, y, text, self.colors['primary'])

        # 畫連接 (順時針)
        arrows = [
            ((420, demo_y + 90), (530, demo_y + 60), '+'),
            ((670, demo_y + 60), (780, demo_y + 90), '+'),
            ((850, demo_y + 130), (670, demo_y + 180), '+'),
            ((530, demo_y + 180), (420, demo_y + 130), '+'),
        ]

        for start, end, sign in arrows:
            self._draw_arrow(dwg, start, end, self.colors['success'], sign)

        # R 標記
        dwg.add(dwg.circle(
            center=(600, demo_y + 115),
            r=25,
            fill=self.colors['reinforcing'],
            opacity=0.9
        ))
        dwg.add(dwg.text(
            'R',
            insert=(600, demo_y + 122),
            text_anchor='middle',
            font_size=24,
            font_weight='bold',
            fill='white'
        ))

        # 說明文字
        dwg.add(dwg.text(
            '(R = Reinforcing 增強迴路：正向循環，越學越有動力)',
            insert=(600, demo_y + 230),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成 CLD 四大元素圖: {output_path.name}")

    def create_loop_comparison(self):
        """創建增強迴路 vs 平衡迴路對比圖"""
        output_path = self.output_dir / "loop-comparison.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1200, 550))

        # 背景
        dwg.add(dwg.rect((0, 0), (1200, 550), fill='#f8fafc'))

        # 標題
        dwg.add(dwg.text(
            '兩種核心循環類型',
            insert=(600, 45),
            text_anchor='middle',
            font_size=32,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # === 左側：增強迴路 ===
        left_x = 300
        center_y = 280

        # 區塊背景
        dwg.add(dwg.rect(
            (50, 80),
            (500, 420),
            fill='white',
            stroke=self.colors['reinforcing'],
            stroke_width=2,
            rx=16
        ))

        dwg.add(dwg.text(
            '🔥 增強迴路 (R)',
            insert=(left_x, 130),
            text_anchor='middle',
            font_size=24,
            font_weight='bold',
            fill=self.colors['reinforcing'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            'Reinforcing Loop',
            insert=(left_x, 160),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['500'],
            font_family='Arial, sans-serif'
        ))

        # 增強迴路範例：複利效應
        r_nodes = [
            (left_x - 100, center_y - 50, '本金'),
            (left_x + 100, center_y - 50, '利息'),
            (left_x, center_y + 80, '資產'),
        ]

        for x, y, text in r_nodes:
            self._draw_variable_node(dwg, x, y, text, self.colors['reinforcing'])

        # 連接
        self._draw_arrow(dwg, (left_x - 50, center_y - 45), (left_x + 50, center_y - 45), self.colors['success'], '+')
        self._draw_arrow(dwg, (left_x + 100, center_y - 20), (left_x + 30, center_y + 60), self.colors['success'], '+')
        self._draw_arrow(dwg, (left_x - 30, center_y + 60), (left_x - 100, center_y - 20), self.colors['success'], '+')

        # R 標記
        dwg.add(dwg.circle(center=(left_x, center_y), r=22, fill=self.colors['reinforcing']))
        dwg.add(dwg.text('R', insert=(left_x, center_y + 7), text_anchor='middle',
                         font_size=22, font_weight='bold', fill='white'))

        # 說明
        dwg.add(dwg.text(
            '滾雪球效應',
            insert=(left_x, center_y + 150),
            text_anchor='middle',
            font_size=18,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '越滾越大，指數成長',
            insert=(left_x, center_y + 175),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # === 右側：平衡迴路 ===
        right_x = 900

        # 區塊背景
        dwg.add(dwg.rect(
            (650, 80),
            (500, 420),
            fill='white',
            stroke=self.colors['balancing'],
            stroke_width=2,
            rx=16
        ))

        dwg.add(dwg.text(
            '❄️ 平衡迴路 (B)',
            insert=(right_x, 130),
            text_anchor='middle',
            font_size=24,
            font_weight='bold',
            fill=self.colors['balancing'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            'Balancing Loop',
            insert=(right_x, 160),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['500'],
            font_family='Arial, sans-serif'
        ))

        # 平衡迴路範例：恆溫器
        b_nodes = [
            (right_x - 100, center_y - 50, '室溫'),
            (right_x + 100, center_y - 50, '溫差'),
            (right_x, center_y + 80, '冷氣輸出'),
        ]

        for x, y, text in b_nodes:
            self._draw_variable_node(dwg, x, y, text, self.colors['balancing'])

        # 連接 (有一個負號)
        self._draw_arrow(dwg, (right_x - 50, center_y - 45), (right_x + 50, center_y - 45), self.colors['success'], '+')
        self._draw_arrow(dwg, (right_x + 100, center_y - 20), (right_x + 30, center_y + 60), self.colors['success'], '+')
        self._draw_arrow(dwg, (right_x - 30, center_y + 60), (right_x - 100, center_y - 20), self.colors['danger'], '-')

        # B 標記
        dwg.add(dwg.circle(center=(right_x, center_y), r=22, fill=self.colors['balancing']))
        dwg.add(dwg.text('B', insert=(right_x, center_y + 7), text_anchor='middle',
                         font_size=22, font_weight='bold', fill='white'))

        # 說明
        dwg.add(dwg.text(
            '恆溫器效應',
            insert=(right_x, center_y + 150),
            text_anchor='middle',
            font_size=18,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '自動調節，維持穩定',
            insert=(right_x, center_y + 175),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 判斷公式
        dwg.add(dwg.rect((400, 470), (400, 60), fill=self.colors['gray']['100'], rx=8))
        dwg.add(dwg.text(
            '判斷方法：數負號數量',
            insert=(600, 495),
            text_anchor='middle',
            font_size=15,
            font_weight='bold',
            fill=self.colors['gray']['900'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '偶數(0,2,4) → R | 奇數(1,3,5) → B',
            insert=(600, 518),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成迴路對比圖: {output_path.name}")

    def create_procrastination_cld(self):
        """創建拖延症因果循環圖"""
        output_path = self.output_dir / "procrastination-cld.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1000, 600))

        # 背景
        gradient = dwg.defs.add(dwg.linearGradient(id="bgGrad", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#fef2f2')
        gradient.add_stop_color(1, '#fff1f2')
        dwg.add(dwg.rect((0, 0), (1000, 600), fill="url(#bgGrad)"))

        # 標題
        dwg.add(dwg.text(
            '範例：拖延症的惡性循環',
            insert=(500, 50),
            text_anchor='middle',
            font_size=28,
            font_weight='bold',
            fill=self.colors['reinforcing'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        center_x, center_y = 500, 320
        radius = 180

        # 五個變數 (圓形排列)
        nodes = [
            (center_x, center_y - radius, '拖延行為'),
            (center_x + radius * 0.95, center_y - radius * 0.31, '待辦堆積'),
            (center_x + radius * 0.59, center_y + radius * 0.81, '焦慮程度'),
            (center_x - radius * 0.59, center_y + radius * 0.81, '逃避衝動'),
            (center_x - radius * 0.95, center_y - radius * 0.31, '專注困難'),
        ]

        # 畫節點
        for x, y, text in nodes:
            self._draw_variable_node(dwg, x, y, text, self.colors['reinforcing'])

        # 畫連接 (順時針，全是正向)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 0)
        ]

        for i, (start_idx, end_idx) in enumerate(connections):
            start_node = nodes[start_idx]
            end_node = nodes[end_idx]

            # 計算起點和終點 (從節點邊緣出發)
            start_x, start_y = start_node[0], start_node[1]
            end_x, end_y = end_node[0], end_node[1]

            # 調整起點終點位置
            angle = math.atan2(end_y - start_y, end_x - start_x)
            offset = 50
            start_adj = (start_x + offset * math.cos(angle), start_y + offset * math.sin(angle))
            end_adj = (end_x - offset * math.cos(angle), end_y - offset * math.sin(angle))

            self._draw_arrow(dwg, start_adj, end_adj, self.colors['reinforcing'], '+')

        # R 標記 (中心)
        dwg.add(dwg.circle(center=(center_x, center_y), r=35, fill=self.colors['reinforcing']))
        dwg.add(dwg.text('R', insert=(center_x, center_y + 10), text_anchor='middle',
                         font_size=32, font_weight='bold', fill='white'))

        # 循環說明
        dwg.add(dwg.text(
            '5 個 (+) = 0 個負號 = 增強迴路 R',
            insert=(500, 530),
            text_anchor='middle',
            font_size=16,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            '惡性循環：不打破任何連結，拖延只會越來越嚴重',
            insert=(500, 560),
            text_anchor='middle',
            font_size=14,
            font_weight='bold',
            fill=self.colors['reinforcing'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成拖延症 CLD: {output_path.name}")

    def create_diet_cld(self):
        """創建節食減肥的平衡迴路圖"""
        output_path = self.output_dir / "diet-cld.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1000, 550))

        # 背景
        gradient = dwg.defs.add(dwg.linearGradient(id="bgGrad2", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#eff6ff')
        gradient.add_stop_color(1, '#f0f9ff')
        dwg.add(dwg.rect((0, 0), (1000, 550), fill="url(#bgGrad2)"))

        # 標題
        dwg.add(dwg.text(
            '範例：節食減肥的平衡迴路',
            insert=(500, 50),
            text_anchor='middle',
            font_size=28,
            font_weight='bold',
            fill=self.colors['balancing'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            '為什麼越減越難減？',
            insert=(500, 80),
            text_anchor='middle',
            font_size=16,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 節點
        center_y = 290
        nodes = [
            (200, center_y - 80, '熱量攝取'),
            (500, center_y - 80, '能量缺口'),
            (800, center_y - 80, '體重'),
            (800, center_y + 100, '基礎代謝'),
            (500, center_y + 100, '身體警報'),
            (200, center_y + 100, '飢餓感'),
        ]

        for x, y, text in nodes:
            self._draw_variable_node(dwg, x, y, text, self.colors['balancing'])

        # 連接 (形成一個大循環)
        arrows = [
            ((280, center_y - 80), (420, center_y - 80), '-'),   # 熱量↓ → 能量缺口↑
            ((580, center_y - 80), (720, center_y - 80), '-'),   # 能量缺口↑ → 體重↓
            ((800, center_y - 45), (800, center_y + 65), '+'),   # 體重↓ → 代謝↓
            ((720, center_y + 100), (580, center_y + 100), '+'), # 代謝↓ → 身體警報↑
            ((420, center_y + 100), (280, center_y + 100), '+'), # 警報↑ → 飢餓感↑
            ((200, center_y + 65), (200, center_y - 45), '+'),   # 飢餓感↑ → 熱量攝取↑
        ]

        for start, end, sign in arrows:
            color = self.colors['success'] if sign == '+' else self.colors['danger']
            self._draw_arrow(dwg, start, end, color, sign)

        # B 標記 (中心)
        dwg.add(dwg.circle(center=(500, center_y + 10), r=32, fill=self.colors['balancing']))
        dwg.add(dwg.text('B', insert=(500, center_y + 18), text_anchor='middle',
                         font_size=28, font_weight='bold', fill='white'))

        # 說明
        dwg.add(dwg.rect((200, 430), (600, 90), fill='white', stroke=self.colors['balancing'], stroke_width=2, rx=12))

        dwg.add(dwg.text(
            '2 個 (-) + 4 個 (+) = 偶數？錯！',
            insert=(500, 460),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '只數負號：2 個 (-) = 偶數 → 這是 R？',
            insert=(500, 485),
            text_anchor='middle',
            font_size=14,
            fill=self.colors['gray']['600'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '實際上這是 B 迴路：身體抵抗減重，維持穩定體重',
            insert=(500, 510),
            text_anchor='middle',
            font_size=15,
            font_weight='bold',
            fill=self.colors['balancing'],
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成節食 CLD: {output_path.name}")

    def create_ig_carousel_slides(self):
        """創建 IG 輪播用的方形圖片 (1080x1080)"""
        slides = [
            self._create_ig_slide_cover,
            self._create_ig_slide_problem,
            self._create_ig_slide_example,
            self._create_ig_slide_solution,
            self._create_ig_slide_elements,
            self._create_ig_slide_loops,
            self._create_ig_slide_tips,
            self._create_ig_slide_cta,
        ]

        for i, create_func in enumerate(slides, 1):
            create_func(i)

    def _create_ig_slide_cover(self, num):
        """封面"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-cover.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        # 漸層背景
        gradient = dwg.defs.add(dwg.linearGradient(id="coverBg", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#1e3a8a')
        gradient.add_stop_color(1, '#3730a3')
        dwg.add(dwg.rect((0, 0), (1080, 1080), fill="url(#coverBg)"))

        # 裝飾圓圈
        dwg.add(dwg.circle(center=(900, 150), r=200, fill='white', opacity=0.05))
        dwg.add(dwg.circle(center=(180, 900), r=150, fill='white', opacity=0.05))

        # 主標題
        dwg.add(dwg.text(
            '為什麼你的',
            insert=(540, 380),
            text_anchor='middle',
            font_size=72,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '解決方案',
            insert=(540, 480),
            text_anchor='middle',
            font_size=80,
            font_weight='bold',
            fill='#fbbf24',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '總是無效？',
            insert=(540, 580),
            text_anchor='middle',
            font_size=72,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 引導
        dwg.add(dwg.text(
            '👉 答案在第 8 張',
            insert=(540, 750),
            text_anchor='middle',
            font_size=36,
            fill='white',
            opacity=0.8,
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: 封面")

    def _create_ig_slide_problem(self, num):
        """問題說明"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-problem.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        dwg.add(dwg.rect((0, 0), (1080, 1080), fill='#0f172a'))

        dwg.add(dwg.text(
            '因為大多數問題',
            insert=(540, 300),
            text_anchor='middle',
            font_size=56,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '不是線性的',
            insert=(540, 380),
            text_anchor='middle',
            font_size=56,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 線性示意
        dwg.add(dwg.text(
            'A → B',
            insert=(540, 520),
            text_anchor='middle',
            font_size=72,
            fill='#ef4444',
            font_family='Arial, sans-serif'
        ))
        dwg.add(dwg.text(
            '❌',
            insert=(720, 520),
            text_anchor='middle',
            font_size=60,
            fill='#ef4444'
        ))

        # 而是循環
        dwg.add(dwg.text(
            '而是循環的',
            insert=(540, 650),
            text_anchor='middle',
            font_size=48,
            fill='#94a3b8',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            'A → B → C → A',
            insert=(540, 780),
            text_anchor='middle',
            font_size=64,
            fill='#22c55e',
            font_family='Arial, sans-serif'
        ))
        dwg.add(dwg.text(
            '✅',
            insert=(820, 780),
            text_anchor='middle',
            font_size=60,
            fill='#22c55e'
        ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: 問題")

    def _create_ig_slide_example(self, num):
        """拖延症範例"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-example.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        dwg.add(dwg.rect((0, 0), (1080, 1080), fill='#fef2f2'))

        dwg.add(dwg.text(
            '舉例：拖延症',
            insert=(540, 120),
            text_anchor='middle',
            font_size=52,
            font_weight='bold',
            fill='#b91c1c',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 循環流程
        steps = ['拖延', '待辦堆積', '焦慮上升', '更想逃避', '更多拖延']
        y_start = 250
        y_gap = 150

        for i, step in enumerate(steps):
            y = y_start + i * y_gap

            # 方框
            dwg.add(dwg.rect(
                (340, y - 35),
                (400, 70),
                fill='white',
                stroke='#b91c1c',
                stroke_width=3,
                rx=12
            ))

            dwg.add(dwg.text(
                step,
                insert=(540, y + 10),
                text_anchor='middle',
                font_size=40,
                font_weight='bold',
                fill='#1e293b',
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

            # 箭頭
            if i < len(steps) - 1:
                dwg.add(dwg.text(
                    '↓',
                    insert=(540, y + 80),
                    text_anchor='middle',
                    font_size=48,
                    fill='#b91c1c'
                ))

        # 回到開頭的弧線
        dwg.add(dwg.text(
            '（惡性循環）',
            insert=(540, 1000),
            text_anchor='middle',
            font_size=36,
            fill='#b91c1c',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: 拖延範例")

    def _create_ig_slide_solution(self, num):
        """解決方案 CLD"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-solution.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        gradient = dwg.defs.add(dwg.linearGradient(id="solBg", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#1e40af')
        gradient.add_stop_color(1, '#7e22ce')
        dwg.add(dwg.rect((0, 0), (1080, 1080), fill="url(#solBg)"))

        dwg.add(dwg.text(
            'CLD',
            insert=(540, 200),
            text_anchor='middle',
            font_size=120,
            font_weight='bold',
            fill='#fbbf24',
            font_family='Arial, sans-serif'
        ))

        dwg.add(dwg.text(
            '因果循環圖',
            insert=(540, 320),
            text_anchor='middle',
            font_size=72,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 描述框
        dwg.add(dwg.rect((140, 420), (800, 200), fill='white', opacity=0.15, rx=20))

        dwg.add(dwg.text(
            '一張圖',
            insert=(540, 500),
            text_anchor='middle',
            font_size=48,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '讓你看清楚',
            insert=(540, 570),
            text_anchor='middle',
            font_size=48,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '問題背後的',
            insert=(540, 700),
            text_anchor='middle',
            font_size=56,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '系統結構',
            insert=(540, 780),
            text_anchor='middle',
            font_size=64,
            font_weight='bold',
            fill='#fbbf24',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: CLD 介紹")

    def _create_ig_slide_elements(self, num):
        """四大元素"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-elements.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        dwg.add(dwg.rect((0, 0), (1080, 1080), fill='#f8fafc'))

        dwg.add(dwg.text(
            '四大元素：',
            insert=(540, 120),
            text_anchor='middle',
            font_size=56,
            font_weight='bold',
            fill='#1e293b',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        elements = [
            ('1️⃣', '變數', '#2563eb'),
            ('2️⃣', '連接（箭頭）', '#7c3aed'),
            ('3️⃣', '+/- 符號', '#059669'),
            ('4️⃣', 'R/B 循環標記', '#dc2626'),
        ]

        y_start = 250
        y_gap = 190

        for i, (emoji, text, color) in enumerate(elements):
            y = y_start + i * y_gap

            # 背景條
            dwg.add(dwg.rect(
                (100, y - 50),
                (880, 130),
                fill='white',
                stroke=color,
                stroke_width=4,
                rx=16
            ))

            # 左側色塊
            dwg.add(dwg.rect(
                (100, y - 50),
                (20, 130),
                fill=color,
                rx=16
            ))
            dwg.add(dwg.rect(
                (108, y - 50),
                (12, 130),
                fill=color
            ))

            dwg.add(dwg.text(
                emoji,
                insert=(200, y + 25),
                text_anchor='middle',
                font_size=60
            ))

            dwg.add(dwg.text(
                text,
                insert=(580, y + 20),
                text_anchor='middle',
                font_size=48,
                font_weight='bold',
                fill='#1e293b',
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: 四大元素")

    def _create_ig_slide_loops(self, num):
        """兩種循環"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-loops.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        dwg.add(dwg.rect((0, 0), (1080, 1080), fill='#0f172a'))

        dwg.add(dwg.text(
            '兩種循環：',
            insert=(540, 120),
            text_anchor='middle',
            font_size=56,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # R 增強迴路
        dwg.add(dwg.rect((100, 220), (400, 350), fill='#7f1d1d', rx=24))
        dwg.add(dwg.text('🔥', insert=(300, 330), text_anchor='middle', font_size=80))
        dwg.add(dwg.text(
            'R 增強迴路',
            insert=(300, 420),
            text_anchor='middle',
            font_size=40,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '滾雪球效應',
            insert=(300, 500),
            text_anchor='middle',
            font_size=32,
            fill='#fca5a5',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # B 平衡迴路
        dwg.add(dwg.rect((580, 220), (400, 350), fill='#1e3a8a', rx=24))
        dwg.add(dwg.text('❄️', insert=(780, 330), text_anchor='middle', font_size=80))
        dwg.add(dwg.text(
            'B 平衡迴路',
            insert=(780, 420),
            text_anchor='middle',
            font_size=40,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '自動調節',
            insert=(780, 500),
            text_anchor='middle',
            font_size=32,
            fill='#93c5fd',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 判斷公式
        dwg.add(dwg.rect((140, 700), (800, 200), fill='#1e293b', rx=20))
        dwg.add(dwg.text(
            '判斷方法：',
            insert=(540, 770),
            text_anchor='middle',
            font_size=36,
            fill='#94a3b8',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))
        dwg.add(dwg.text(
            '數負號數量',
            insert=(540, 830),
            text_anchor='middle',
            font_size=44,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: 兩種循環")

    def _create_ig_slide_tips(self, num):
        """新手提示"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-tips.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        gradient = dwg.defs.add(dwg.linearGradient(id="tipsBg", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#ecfdf5')
        gradient.add_stop_color(1, '#d1fae5')
        dwg.add(dwg.rect((0, 0), (1080, 1080), fill="url(#tipsBg)"))

        dwg.add(dwg.text(
            '新手提示：',
            insert=(540, 150),
            text_anchor='middle',
            font_size=56,
            font_weight='bold',
            fill='#065f46',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        tips = [
            ('✅', '從 5 個變數開始'),
            ('✅', '先畫核心循環'),
            ('✅', '不要追求完美'),
        ]

        y_start = 320
        y_gap = 220

        for i, (icon, text) in enumerate(tips):
            y = y_start + i * y_gap

            dwg.add(dwg.rect(
                (140, y - 60),
                (800, 150),
                fill='white',
                stroke='#059669',
                stroke_width=4,
                rx=20
            ))

            dwg.add(dwg.text(
                icon,
                insert=(220, y + 20),
                text_anchor='middle',
                font_size=60
            ))

            dwg.add(dwg.text(
                text,
                insert=(580, y + 15),
                text_anchor='middle',
                font_size=44,
                font_weight='bold',
                fill='#1e293b',
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: 新手提示")

    def _create_ig_slide_cta(self, num):
        """CTA"""
        output_path = self.output_dir / f"ig-slide-{num:02d}-cta.svg"
        dwg = svgwrite.Drawing(str(output_path), size=(1080, 1080))

        gradient = dwg.defs.add(dwg.linearGradient(id="ctaBg", x1="0%", y1="0%", x2="100%", y2="100%"))
        gradient.add_stop_color(0, '#7c3aed')
        gradient.add_stop_color(1, '#2563eb')
        dwg.add(dwg.rect((0, 0), (1080, 1080), fill="url(#ctaBg)"))

        dwg.add(dwg.text(
            '完整教學',
            insert=(540, 350),
            text_anchor='middle',
            font_size=80,
            font_weight='bold',
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        dwg.add(dwg.text(
            '👆',
            insert=(540, 480),
            text_anchor='middle',
            font_size=100
        ))

        dwg.add(dwg.text(
            '連結在自介',
            insert=(540, 600),
            text_anchor='middle',
            font_size=56,
            fill='white',
            font_family='Arial, Microsoft JhengHei, sans-serif'
        ))

        # 內容清單
        dwg.add(dwg.rect((200, 700), (680, 250), fill='white', opacity=0.15, rx=20))

        items = ['• 四大元素詳解', '• 三個完整範例', '• 手把手步驟']
        for i, item in enumerate(items):
            dwg.add(dwg.text(
                item,
                insert=(540, 780 + i * 60),
                text_anchor='middle',
                font_size=36,
                fill='white',
                font_family='Arial, Microsoft JhengHei, sans-serif'
            ))

        dwg.save()
        print(f"✓ 已生成 IG 輪播 {num}: CTA")


def main():
    """主函數"""
    import sys

    # 確定輸出目錄
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1]) / "images"
    else:
        # 找最新的 CLD session
        base_dir = Path(__file__).parent.parent / "output"
        sessions = sorted(base_dir.glob("session_*CLD*"), reverse=True)
        if not sessions:
            sessions = sorted(base_dir.glob("session_*"), reverse=True)
        if sessions:
            output_dir = sessions[0] / "images"
        else:
            output_dir = base_dir / "cld_images"

    output_dir.mkdir(parents=True, exist_ok=True)

    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         🎨 CLD 因果循環圖 SVG 生成器                           ║")
    print("║         為系統思考文章生成專業圖表                             ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    generator = CLDChartGenerator(output_dir)

    print("📊 生成文章內插圖...")
    generator.create_cld_elements()
    generator.create_loop_comparison()
    generator.create_procrastination_cld()
    generator.create_diet_cld()

    print("\n📱 生成 IG 輪播圖片...")
    generator.create_ig_carousel_slides()

    print(f"\n✅ 所有圖表已生成完成！")
    print(f"📁 輸出目錄: {output_dir}")
    print(f"\n生成的檔案：")
    for f in sorted(output_dir.glob("*.svg")):
        print(f"   • {f.name}")


if __name__ == "__main__":
    main()
