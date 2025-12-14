#!/usr/bin/env python3
"""
Analytics Reporter Helper Script
整合 Google Analytics 生成分析報告
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非 GUI backend

# 配置中文字體支援
try:
    import platform
    system = platform.system()
    if system == 'Darwin':  # macOS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang TC']
    elif system == 'Windows':
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    else:  # Linux
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
except Exception:
    # 如果字體設定失敗，使用默認字體（會有警告但不影響功能）
    pass


class AnalyticsReporter:
    """Analytics 報告生成器"""

    def __init__(self):
        self.report_data = {}

    def generate_weekly_report(self, data: Dict, output_dir: str = '.') -> Dict:
        """
        生成週報告

        Args:
            data: 從 GA MCP 獲取的數據
            output_dir: 輸出目錄

        Returns:
            報告摘要
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        report = {
            'report_type': 'weekly',
            'generated_at': datetime.now().isoformat(),
            'period': self._get_last_week_period(),
            'summary': {},
            'top_content': [],
            'traffic_sources': {},
            'recommendations': []
        }

        # 1. 核心指標摘要
        report['summary'] = self._calculate_summary_metrics(data)

        # 2. 熱門內容分析
        report['top_content'] = self._analyze_top_content(data)

        # 3. 流量來源分析
        report['traffic_sources'] = self._analyze_traffic_sources(data)

        # 4. 生成建議
        report['recommendations'] = self._generate_recommendations(report)

        # 5. 生成圖表
        self._generate_charts(report, output_path)

        # 6. 生成 Markdown 報告
        markdown_report = self._generate_markdown_report(report)
        with open(output_path / 'weekly_report.md', 'w', encoding='utf-8') as f:
            f.write(markdown_report)

        # 7. 保存 JSON 資料
        with open(output_path / 'weekly_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

    def generate_monthly_report(self, data: Dict, output_dir: str = '.') -> Dict:
        """
        生成月報告

        Args:
            data: 從 GA MCP 獲取的數據
            output_dir: 輸出目錄

        Returns:
            報告摘要
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        report = {
            'report_type': 'monthly',
            'generated_at': datetime.now().isoformat(),
            'period': self._get_last_month_period(),
            'summary': {},
            'trends': {},
            'platform_comparison': {},
            'content_performance': [],
            'recommendations': []
        }

        # 1. 核心指標摘要
        report['summary'] = self._calculate_summary_metrics(data)

        # 2. 趨勢分析
        report['trends'] = self._analyze_trends(data)

        # 3. 平台比較
        report['platform_comparison'] = self._compare_platforms(data)

        # 4. 內容表現
        report['content_performance'] = self._analyze_content_performance(data)

        # 5. 生成建議
        report['recommendations'] = self._generate_monthly_recommendations(report)

        # 6. 生成圖表
        self._generate_monthly_charts(report, output_path)

        # 7. 生成 Markdown 報告
        markdown_report = self._generate_monthly_markdown_report(report)
        with open(output_path / 'monthly_report.md', 'w', encoding='utf-8') as f:
            f.write(markdown_report)

        # 8. 保存 JSON 資料
        with open(output_path / 'monthly_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

    def _calculate_summary_metrics(self, data: Dict) -> Dict:
        """計算摘要指標"""
        # 從 GA 數據計算核心指標
        summary = {
            'total_pageviews': data.get('pageviews', 0),
            'unique_visitors': data.get('users', 0),
            'avg_session_duration': data.get('avgSessionDuration', 0),
            'bounce_rate': data.get('bounceRate', 0),
            'pages_per_session': data.get('pageviewsPerSession', 0)
        }

        # 計算變化百分比（與上週/上月比較）
        if 'previous_period' in data:
            prev = data['previous_period']
            summary['pageviews_change'] = self._calculate_change_percent(
                summary['total_pageviews'],
                prev.get('pageviews', 0)
            )
            summary['visitors_change'] = self._calculate_change_percent(
                summary['unique_visitors'],
                prev.get('users', 0)
            )

        return summary

    def _analyze_top_content(self, data: Dict) -> List[Dict]:
        """分析熱門內容"""
        top_content = []

        # 假設 GA 數據包含頁面資訊
        pages = data.get('pages', [])
        for page in pages[:10]:  # 前 10 名
            top_content.append({
                'title': page.get('pageTitle', ''),
                'url': page.get('pagePath', ''),
                'pageviews': page.get('pageviews', 0),
                'avg_time': page.get('avgTimeOnPage', 0),
                'bounce_rate': page.get('bounceRate', 0),
                'performance_score': self._calculate_content_score(page)
            })

        return top_content

    def _analyze_traffic_sources(self, data: Dict) -> Dict:
        """分析流量來源"""
        sources = {
            'organic': {'sessions': 0, 'percentage': 0},
            'direct': {'sessions': 0, 'percentage': 0},
            'referral': {'sessions': 0, 'percentage': 0},
            'social': {'sessions': 0, 'percentage': 0},
            'email': {'sessions': 0, 'percentage': 0}
        }

        # 從 GA 數據提取流量來源
        if 'sources' in data:
            total_sessions = sum(s.get('sessions', 0) for s in data['sources'])

            for source in data['sources']:
                source_type = source.get('medium', '').lower()
                sessions = source.get('sessions', 0)

                if source_type in sources:
                    sources[source_type]['sessions'] = sessions
                    if total_sessions > 0:
                        sources[source_type]['percentage'] = (sessions / total_sessions) * 100

        return sources

    def _analyze_trends(self, data: Dict) -> Dict:
        """分析趨勢"""
        trends = {
            'daily_pageviews': [],
            'weekly_pattern': {},
            'growth_rate': 0
        }

        # 分析每日流量
        if 'daily_data' in data:
            for day in data['daily_data']:
                trends['daily_pageviews'].append({
                    'date': day.get('date', ''),
                    'pageviews': day.get('pageviews', 0)
                })

        # 分析星期模式
        weekday_data = defaultdict(list)
        for day in trends['daily_pageviews']:
            date = datetime.fromisoformat(day['date'])
            weekday = date.strftime('%A')
            weekday_data[weekday].append(day['pageviews'])

        for weekday, pageviews in weekday_data.items():
            trends['weekly_pattern'][weekday] = sum(pageviews) / len(pageviews) if pageviews else 0

        return trends

    def _compare_platforms(self, data: Dict) -> Dict:
        """比較平台表現"""
        platforms = {
            'blog': {'traffic': 0, 'engagement': 0, 'conversions': 0},
            'social_media': {'traffic': 0, 'engagement': 0, 'conversions': 0},
            'email': {'traffic': 0, 'engagement': 0, 'conversions': 0}
        }

        # 從 GA 數據計算各平台 ROI
        if 'platform_data' in data:
            for platform, metrics in data['platform_data'].items():
                if platform in platforms:
                    platforms[platform]['traffic'] = metrics.get('sessions', 0)
                    platforms[platform]['engagement'] = metrics.get('avgSessionDuration', 0)
                    platforms[platform]['conversions'] = metrics.get('goalCompletions', 0)

        return platforms

    def _analyze_content_performance(self, data: Dict) -> List[Dict]:
        """分析內容表現"""
        content = []

        pages = data.get('pages', [])
        for page in pages[:20]:
            performance = {
                'title': page.get('pageTitle', ''),
                'url': page.get('pagePath', ''),
                'metrics': {
                    'pageviews': page.get('pageviews', 0),
                    'avg_time': page.get('avgTimeOnPage', 0),
                    'bounce_rate': page.get('bounceRate', 0),
                    'exit_rate': page.get('exitRate', 0)
                },
                'category': self._categorize_content(page.get('pagePath', '')),
                'performance_level': self._get_performance_level(page)
            }
            content.append(performance)

        return content

    def _generate_recommendations(self, report: Dict) -> List[Dict]:
        """生成週報告建議"""
        recommendations = []
        summary = report['summary']
        top_content = report['top_content']

        # 1. 流量建議
        if summary.get('pageviews_change', 0) < 0:
            recommendations.append({
                'priority': 'High',
                'category': 'Traffic Growth',
                'issue': f"本週流量下降 {abs(summary.get('pageviews_change', 0)):.1f}%",
                'action': '增加社群媒體推廣頻率，重新發布熱門文章',
                'expected_impact': '流量回升 15-20%'
            })

        # 2. 內容建議
        if top_content:
            best_performer = top_content[0]
            recommendations.append({
                'priority': 'Medium',
                'category': 'Content Strategy',
                'issue': f"熱門文章：{best_performer['title']}",
                'action': '基於此主題創作系列文章，擴展相關內容',
                'expected_impact': '相關流量 +30-40%'
            })

        # 3. 轉換建議
        if summary.get('bounce_rate', 0) > 60:
            recommendations.append({
                'priority': 'High',
                'category': 'User Engagement',
                'issue': f"跳出率高達 {summary.get('bounce_rate', 0):.1f}%",
                'action': '優化首屏內容，增加內部連結，改善 CTA',
                'expected_impact': '跳出率降低 10-15%'
            })

        return recommendations

    def _generate_monthly_recommendations(self, report: Dict) -> List[Dict]:
        """生成月報告建議"""
        recommendations = []
        summary = report['summary']
        trends = report['trends']
        platforms = report['platform_comparison']

        # 1. 趨勢建議
        growth_rate = trends.get('growth_rate', 0)
        if growth_rate < 5:
            recommendations.append({
                'priority': 'High',
                'category': 'Growth Strategy',
                'issue': f"本月成長率僅 {growth_rate:.1f}%，低於預期",
                'action': '啟動 SEO 優化專案，增加長尾關鍵字內容',
                'expected_impact': '下月成長率提升至 10-15%'
            })

        # 2. 平台建議
        best_platform = max(platforms.items(), key=lambda x: x[1]['traffic'])
        recommendations.append({
            'priority': 'Medium',
            'category': 'Platform Optimization',
            'issue': f"{best_platform[0]} 表現最佳",
            'action': f"加大 {best_platform[0]} 投資，優化其他平台策略",
            'expected_impact': '整體轉換率 +20%'
        })

        return recommendations

    def _generate_charts(self, report: Dict, output_path: Path):
        """生成週報告圖表"""
        # 1. 流量來源圓餅圖
        sources = report['traffic_sources']
        labels = [s.capitalize() for s in sources.keys()]
        sizes = [sources[s]['sessions'] for s in sources.keys()]

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Traffic Sources Distribution')
        plt.savefig(output_path / 'traffic_sources.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 2. 熱門內容條形圖
        top_content = report['top_content'][:5]
        titles = [c['title'][:30] + '...' if len(c['title']) > 30 else c['title'] for c in top_content]
        pageviews = [c['pageviews'] for c in top_content]

        plt.figure(figsize=(12, 6))
        plt.barh(titles, pageviews)
        plt.xlabel('Pageviews')
        plt.title('Top 5 Content Performance')
        plt.tight_layout()
        plt.savefig(output_path / 'top_content.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_monthly_charts(self, report: Dict, output_path: Path):
        """生成月報告圖表"""
        # 1. 每日流量趨勢圖
        trends = report['trends']
        daily_data = trends.get('daily_pageviews', [])

        if daily_data:
            dates = [d['date'] for d in daily_data]
            pageviews = [d['pageviews'] for d in daily_data]

            plt.figure(figsize=(14, 6))
            plt.plot(dates, pageviews, marker='o', linestyle='-', linewidth=2)
            plt.xlabel('Date')
            plt.ylabel('Pageviews')
            plt.title('Daily Traffic Trend')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_path / 'daily_trend.png', dpi=300, bbox_inches='tight')
            plt.close()

        # 2. 平台比較圖
        platforms = report['platform_comparison']
        platform_names = list(platforms.keys())
        traffic = [platforms[p]['traffic'] for p in platform_names]

        plt.figure(figsize=(10, 6))
        plt.bar(platform_names, traffic)
        plt.xlabel('Platform')
        plt.ylabel('Sessions')
        plt.title('Platform Performance Comparison')
        plt.tight_layout()
        plt.savefig(output_path / 'platform_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_markdown_report(self, report: Dict) -> str:
        """生成週報告 Markdown"""
        md = f"""# 週報告 - {report['period']['start']} 至 {report['period']['end']}

生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 核心指標摘要

| 指標 | 數值 | 變化 |
|------|------|------|
| 總瀏覽量 | {report['summary']['total_pageviews']:,} | {report['summary'].get('pageviews_change', 0):+.1f}% |
| 獨立訪客 | {report['summary']['unique_visitors']:,} | {report['summary'].get('visitors_change', 0):+.1f}% |
| 平均停留時間 | {report['summary']['avg_session_duration']:.1f}s | - |
| 跳出率 | {report['summary']['bounce_rate']:.1f}% | - |
| 頁面/工作階段 | {report['summary']['pages_per_session']:.2f} | - |

## 🏆 熱門內容 TOP 5

"""
        for i, content in enumerate(report['top_content'][:5], 1):
            md += f"{i}. **{content['title']}**\n"
            md += f"   - 瀏覽量: {content['pageviews']:,}\n"
            md += f"   - 平均停留: {content['avg_time']:.1f}s\n"
            md += f"   - 跳出率: {content['bounce_rate']:.1f}%\n\n"

        md += "\n## 🌐 流量來源分析\n\n"
        for source, data in report['traffic_sources'].items():
            md += f"- **{source.capitalize()}**: {data['sessions']:,} ({data['percentage']:.1f}%)\n"

        md += "\n## 💡 行動建議\n\n"
        for i, rec in enumerate(report['recommendations'], 1):
            md += f"### {i}. {rec['category']} ({rec['priority']} Priority)\n\n"
            md += f"**問題**: {rec['issue']}\n\n"
            md += f"**建議行動**: {rec['action']}\n\n"
            md += f"**預期影響**: {rec['expected_impact']}\n\n"

        md += "\n## 📈 視覺化圖表\n\n"
        md += "![流量來源分布](traffic_sources.png)\n\n"
        md += "![熱門內容表現](top_content.png)\n"

        return md

    def _generate_monthly_markdown_report(self, report: Dict) -> str:
        """生成月報告 Markdown"""
        md = f"""# 月報告 - {report['period']['month']}

生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 整體表現摘要

| 指標 | 本月 | 上月 | 變化 |
|------|------|------|------|
| 總瀏覽量 | {report['summary']['total_pageviews']:,} | - | {report['summary'].get('pageviews_change', 0):+.1f}% |
| 獨立訪客 | {report['summary']['unique_visitors']:,} | - | {report['summary'].get('visitors_change', 0):+.1f}% |
| 平均停留時間 | {report['summary']['avg_session_duration']:.1f}s | - | - |

## 📈 趨勢分析

**成長率**: {report['trends'].get('growth_rate', 0):.1f}%

### 星期流量模式

"""
        weekly_pattern = report['trends'].get('weekly_pattern', {})
        for day, avg_pageviews in weekly_pattern.items():
            md += f"- **{day}**: {avg_pageviews:.0f} 平均瀏覽量\n"

        md += "\n## 🏆 平台表現比較\n\n"
        for platform, data in report['platform_comparison'].items():
            md += f"### {platform.replace('_', ' ').title()}\n\n"
            md += f"- 流量: {data['traffic']:,}\n"
            md += f"- 互動: {data['engagement']:.1f}s\n"
            md += f"- 轉換: {data['conversions']}\n\n"

        md += "\n## 💡 策略建議\n\n"
        for i, rec in enumerate(report['recommendations'], 1):
            md += f"### {i}. {rec['category']} ({rec['priority']} Priority)\n\n"
            md += f"**問題**: {rec['issue']}\n\n"
            md += f"**建議行動**: {rec['action']}\n\n"
            md += f"**預期影響**: {rec['expected_impact']}\n\n"

        md += "\n## 📈 視覺化圖表\n\n"
        md += "![每日流量趨勢](daily_trend.png)\n\n"
        md += "![平台表現比較](platform_comparison.png)\n"

        return md

    # === 輔助方法 ===

    def _get_last_week_period(self) -> Dict:
        """獲取上週時間範圍"""
        today = datetime.now()
        start = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        end = today.strftime('%Y-%m-%d')
        return {'start': start, 'end': end}

    def _get_last_month_period(self) -> Dict:
        """獲取上月時間範圍"""
        today = datetime.now()
        first_day = today.replace(day=1)
        last_month = (first_day - timedelta(days=1))
        return {
            'month': last_month.strftime('%Y-%m'),
            'start': last_month.replace(day=1).strftime('%Y-%m-%d'),
            'end': last_month.strftime('%Y-%m-%d')
        }

    def _calculate_change_percent(self, current: float, previous: float) -> float:
        """計算變化百分比"""
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100

    def _calculate_content_score(self, page: Dict) -> float:
        """計算內容表現分數"""
        # 簡化版評分算法
        pageviews = page.get('pageviews', 0)
        avg_time = page.get('avgTimeOnPage', 0)
        bounce_rate = page.get('bounceRate', 100)

        score = (pageviews * 0.4) + (avg_time * 0.3) + ((100 - bounce_rate) * 0.3)
        return round(score, 1)

    def _categorize_content(self, url: str) -> str:
        """根據 URL 分類內容"""
        if '/tutorial' in url or '/how-to' in url:
            return 'Tutorial'
        elif '/news' in url:
            return 'News'
        elif '/review' in url:
            return 'Review'
        else:
            return 'General'

    def _get_performance_level(self, page: Dict) -> str:
        """評估內容表現等級"""
        score = self._calculate_content_score(page)

        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        else:
            return 'Needs Improvement'


def main():
    """命令列介面"""
    if len(sys.argv) < 3:
        print("用法: python generate_report.py <report_type> <data_file> [output_dir]")
        print("範例: python generate_report.py weekly ga_data.json ./reports")
        print("report_type: weekly 或 monthly")
        sys.exit(1)

    report_type = sys.argv[1]
    data_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else '.'

    # 讀取 GA 數據
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 生成報告
    reporter = AnalyticsReporter()

    if report_type == 'weekly':
        result = reporter.generate_weekly_report(data, output_dir)
    elif report_type == 'monthly':
        result = reporter.generate_monthly_report(data, output_dir)
    else:
        print(f"❌ 不支援的報告類型: {report_type}")
        sys.exit(1)

    print(f"✅ {report_type.capitalize()} 報告已生成於: {output_dir}")
    print(json.dumps(result['summary'], indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
