---
name: analytics-reporter
description: Generate comprehensive analytics reports from Google Analytics data. Use when you need weekly/monthly performance reports, traffic analysis, content insights, or A/B testing results. Integrates with Google Analytics MCP to fetch data and create actionable reports.
license: MIT
version: 1.0.0
allowed-tools:
  - read
  - write
  - bash
---

# Analytics Reporter Skill

Automatically generates comprehensive analytics reports by integrating with Google Analytics 4 MCP server. Creates weekly/monthly reports with visualizations, insights, and actionable recommendations.

## When to Use This Skill

Activate this skill when you need to:
- Generate weekly/monthly analytics reports
- Analyze article performance and traffic trends
- Compare platform effectiveness (Medium, LinkedIn, FB, etc.)
- Track A/B testing results for headlines
- Identify top-performing content
- Generate executive summaries for stakeholders
- Monitor KPIs and conversion rates

## Prerequisites

### 1. Google Analytics MCP Server

**Installation**:
```bash
npm install -g google-analytics-mcp
```

**Configuration** (`~/.claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "google-analytics": {
      "command": "google-analytics-mcp",
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json",
        "GA4_PROPERTY_ID": "your-property-id"
      }
    }
  }
}
```

### 2. Python Dependencies

```bash
pip install pandas matplotlib seaborn pyyaml openpyxl
```

### 3. Google Cloud Setup

1. Create Google Cloud Project
2. Enable Google Analytics Data API
3. Create Service Account
4. Download credentials.json
5. Share GA4 property with service account email

## Usage Workflow

### Standard Report Generation

```
User: "生成這週的分析報告"

Skill Actions:
1. Query GA4 for last 7 days data
2. Fetch metrics: pageviews, users, sessions, bounce rate
3. Identify top 10 articles
4. Compare with previous period
5. Generate insights and recommendations
6. Create report (Markdown + Excel + Charts)
7. Save to output/analytics/
```

### Custom Time Range

```
User: "生成 10 月份的月報"

Skill Actions:
1. Parse date range (2025-10-01 to 2025-10-31)
2. Query GA4 for the entire month
3. Compare with September
4. Generate comprehensive monthly report
```

### Platform Comparison

```
User: "比較 Medium 和 LinkedIn 的流量表現"

Skill Actions:
1. Query GA4 with source/medium filters
2. Compare metrics between platforms
3. Calculate ROI and engagement rates
4. Provide platform-specific recommendations
```

## Report Structure

### Weekly Report Format

**Output**: `output/analytics/weekly_report_YYYYMMDD.md`

```markdown
# 📊 週報分析 (YYYY-MM-DD ~ YYYY-MM-DD)

## 執行摘要

本週整體表現 [↑/↓ XX%]
- 總瀏覽數: XX,XXX (↑ XX%)
- 獨立訪客: X,XXX (↑ XX%)
- 平均停留時間: Xm XXs (↑ XX%)
- 跳出率: XX% (↓ XX%)

## 🏆 Top 10 文章

| # | 標題 | 瀏覽數 | CTR | 停留時間 | 變化 |
|---|------|--------|-----|----------|------|
| 1 | [文章標題](URL) | X,XXX | X.X% | Xm XXs | ↑ XX% |
| 2 | ... | ... | ... | ... | ... |

## 📈 流量趨勢

[圖表: 7 天瀏覽數趨勢]

觀察:
- 週二流量最高 (X,XXX)
- 週末流量下降 XX%
- 突增原因: [分析]

## 🎯 平台表現

| 平台 | 瀏覽數 | 佔比 | CTR | ROI |
|------|--------|------|-----|-----|
| Medium | X,XXX | XX% | X.X% | ⭐⭐⭐⭐⭐ |
| LinkedIn | X,XXX | XX% | X.X% | ⭐⭐⭐⭐ |
| Facebook | X,XXX | XX% | X.X% | ⭐⭐⭐ |

## 💡 關鍵洞察

### 1. 標題類型效果

數字型標題 vs 技術型標題:
- 數字型平均 CTR: X.X% (↑ XX%)
- 技術型平均 CTR: X.X%
- **建議**: 增加數字型標題使用比例至 60%

### 2. 最佳發布時間

- 週二 08:00-10:00: 最高 CTR (X.X%)
- 週四 18:00-20:00: 最多分享數
- **建議**: 重點文章安排在週二早上

### 3. 內容類型偏好

- 實戰教學類: 平均停留 Xm XXs
- 工具評測類: 平均停留 Xm XXs
- **建議**: 增加實戰教學比例

## 🎬 下週行動建議

1. **內容策略**
   - 撰寫 [主題] 相關文章（預測流量: X,XXX）
   - 更新表現不佳的舊文章（3 篇候選）

2. **發布優化**
   - 週二早上發布重點文章
   - 測試新的標題公式

3. **平台分配**
   - 加強 Medium 推廣（ROI 最高）
   - 優化 Facebook 貼文文案

## 📊 詳細數據

完整數據請查看:
- Excel 報表: weekly_report_YYYYMMDD.xlsx
- 圖表: weekly_charts_YYYYMMDD/

---

**報告生成時間**: YYYY-MM-DD HH:MM:SS
**數據來源**: Google Analytics 4
**涵蓋期間**: 7 天
```

### Monthly Report Format

**Output**: `output/analytics/monthly_report_YYYYMM.md`

```markdown
# 📊 月度分析報告 (YYYY-MM)

## 執行摘要

### 整體表現

本月達成情況:
- ✅ 目標瀏覽數: XX,XXX (目標 XX,XXX, 達成率 XXX%)
- ✅ 新訪客: X,XXX (↑ XX% MoM)
- ⚠️ 轉化率: X.X% (目標 X.X%, 差距 -X.X%)

### 月度亮點

1. 🎉 突破性增長: [具體成就]
2. 📈 關鍵指標改善: [具體數據]
3. 🏆 最佳文章: [標題] (X,XXX views)

## 📈 月度趨勢分析

[圖表: 30 天瀏覽數、用戶數、停留時間趨勢]

### 流量模式

- 週間平均: X,XXX views/day
- 週末平均: X,XXX views/day
- 峰值日期: YYYY-MM-DD (X,XXX views)
- 谷底日期: YYYY-MM-DD (X,XXX views)

### 成長動能

- 有機搜尋: ↑ XX% (主要驅動力)
- 社群媒體: ↑ XX%
- 直接流量: ↓ XX% (需關注)

## 🏆 Top 20 文章 (月度)

[詳細表格，包含瀏覽數、停留時間、跳出率、分享數]

### 內容分類表現

| 分類 | 文章數 | 總瀏覽 | 平均停留 | CTR |
|------|--------|--------|----------|-----|
| AI 開發 | XX | XX,XXX | Xm XXs | X.X% |
| 自動化 | XX | XX,XXX | Xm XXs | X.X% |
| 工具評測 | XX | XX,XXX | Xm XXs | X.X% |

## 🎯 平台深度分析

### Medium

表現: ⭐⭐⭐⭐⭐ (優秀)
- 流量貢獻: XX,XXX (佔比 XX%)
- 平均 CTR: X.X%
- 粉絲增長: +XXX (↑ XX%)

策略建議:
- 持續投入，ROI 最高
- 建議發文頻率: 每週 2-3 篇
- 測試 Series 功能增加訂閱

### LinkedIn

表現: ⭐⭐⭐⭐ (良好)
- 流量貢獻: XX,XXX (佔比 XX%)
- 專業受眾比例: XX%
- B2B 轉化率: X.X%

策略建議:
- 增加商業導向內容
- 參與社群討論提升能見度

### Facebook

表現: ⭐⭐⭐ (中等)
- 流量貢獻: XX,XXX (佔比 XX%)
- 互動率: X.X% (低於平均)

改善建議:
- 優化貼文文案（參考 Marketing Optimizer）
- 增加視覺元素（圖片、影片）
- 測試不同發布時間

## 💡 關鍵洞察與發現

### 1. A/B Testing 結果

測試對象: 標題類型
- 組 A（數字型）: CTR X.X%
- 組 B（技術型）: CTR X.X%
- **結論**: 數字型標題提升 XX% 點擊率

### 2. 用戶行為模式

平均用戶旅程:
1. 首次訪問: 社群媒體 (XX%)
2. 閱讀時間: X.X 分鐘
3. 二次訪問: 直接流量 (XX%)
4. 訂閱/轉化: X.X%

### 3. 搜尋引擎表現

Top 10 關鍵字:
1. [關鍵字] - XXX impressions, X.X% CTR
2. [關鍵字] - XXX impressions, X.X% CTR
...

SEO 機會:
- 排名 11-20 的關鍵字（優化可快速提升）
- 高曝光低點擊字詞（優化標題和描述）

## 🎬 下月策略建議

### 內容策略

1. **主題規劃** (基於數據洞察)
   - 主推主題: [主題名稱] (預測流量: XX,XXX)
   - 次要主題: [主題名稱] (預測流量: XX,XXX)

2. **內容類型**
   - 實戰教學: XX% (當前表現最佳)
   - 工具評測: XX%
   - 案例分析: XX%

3. **發布節奏**
   - 週二、週四重點發布
   - 總篇數目標: XX 篇
   - 預期總流量: XX,XXX

### 平台優化

1. **Medium**
   - 加大投入（ROI 最高）
   - 目標: +XX% 流量

2. **LinkedIn**
   - 增加 B2B 內容
   - 參與度目標: +XX%

3. **Facebook**
   - 改善貼文品質
   - 測試 Reels 和短影音

### KPI 目標

| 指標 | 本月實際 | 下月目標 | 增長率 |
|------|---------|---------|--------|
| 總瀏覽數 | XX,XXX | XX,XXX | +XX% |
| 新訪客 | X,XXX | X,XXX | +XX% |
| 轉化率 | X.X% | X.X% | +X.X% |
| 停留時間 | Xm XXs | Xm XXs | +XX% |

## 📊 附錄

### 詳細數據檔案

- Excel 完整報表: `monthly_report_YYYYMM.xlsx`
- 圖表集: `monthly_charts_YYYYMM/`
- 原始數據: `raw_data_YYYYMM.csv`

### 數據說明

- 數據來源: Google Analytics 4
- 統計期間: YYYY-MM-01 ~ YYYY-MM-31
- 時區: GMT+8 (台北)
- 更新頻率: 每日

---

**報告生成時間**: YYYY-MM-DD HH:MM:SS
**分析者**: Analytics Reporter Skill
**報告版本**: v1.0
```

## Implementation Details

### Step 1: Query Google Analytics

```python
# 使用 Google Analytics MCP
# Claude Code 會自動調用已配置的 MCP

def fetch_ga_data(start_date, end_date, metrics, dimensions):
    """
    透過 GA MCP 查詢數據

    Parameters:
    - start_date: 'YYYY-MM-DD'
    - end_date: 'YYYY-MM-DD'
    - metrics: ['pageviews', 'users', 'sessions', 'bounceRate', ...]
    - dimensions: ['pagePath', 'pageTitle', 'source', 'medium', ...]

    Returns:
    - DataFrame with requested data
    """
    # MCP 會處理實際的 API 調用
    # 我們只需要構建查詢語句

    query = f"""
    請查詢 Google Analytics 資料:
    - 期間: {start_date} 到 {end_date}
    - 指標: {', '.join(metrics)}
    - 維度: {', '.join(dimensions)}
    """

    # Claude 會執行 MCP 調用並返回數據
    return query_result
```

### Step 2: Process and Analyze

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_article_performance(data):
    """分析文章表現"""

    # 計算關鍵指標
    top_articles = data.nlargest(10, 'pageviews')

    # 計算成長率
    previous_period = fetch_previous_period_data()
    growth = calculate_growth(data, previous_period)

    # 識別趨勢
    trends = identify_trends(data)

    return {
        'top_articles': top_articles,
        'growth': growth,
        'trends': trends
    }

def compare_platforms(data):
    """比較平台表現"""

    platform_stats = data.groupby('source').agg({
        'pageviews': 'sum',
        'users': 'sum',
        'avgSessionDuration': 'mean',
        'bounceRate': 'mean'
    })

    # 計算 ROI 評分
    platform_stats['roi_score'] = calculate_roi_score(platform_stats)

    return platform_stats.sort_values('pageviews', ascending=False)
```

### Step 3: Generate Visualizations

```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_traffic_trend_chart(data, output_path):
    """生成流量趨勢圖"""

    plt.figure(figsize=(12, 6))
    plt.plot(data['date'], data['pageviews'], marker='o')
    plt.title('7天瀏覽數趨勢')
    plt.xlabel('日期')
    plt.ylabel('瀏覽數')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_platform_comparison_chart(platform_data, output_path):
    """生成平台對比圖"""

    fig, ax = plt.subplots(figsize=(10, 6))
    platforms = platform_data.index
    x = np.arange(len(platforms))
    width = 0.35

    ax.bar(x - width/2, platform_data['pageviews'], width, label='瀏覽數')
    ax.bar(x + width/2, platform_data['users'], width, label='訪客數')

    ax.set_xlabel('平台')
    ax.set_ylabel('數量')
    ax.set_title('平台流量對比')
    ax.set_xticks(x)
    ax.set_xticklabels(platforms)
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
```

### Step 4: Generate Reports

```python
def generate_weekly_report(start_date, end_date):
    """生成週報"""

    # 1. 查詢數據
    data = fetch_ga_data(
        start_date,
        end_date,
        metrics=['pageviews', 'users', 'avgSessionDuration', 'bounceRate'],
        dimensions=['pagePath', 'pageTitle', 'source']
    )

    # 2. 分析數據
    analysis = analyze_article_performance(data)
    platform_comparison = compare_platforms(data)
    insights = generate_insights(analysis, platform_comparison)

    # 3. 創建圖表
    charts_dir = f'output/analytics/weekly_charts_{start_date}'
    os.makedirs(charts_dir, exist_ok=True)

    create_traffic_trend_chart(data, f'{charts_dir}/traffic_trend.png')
    create_platform_comparison_chart(platform_comparison, f'{charts_dir}/platform_comparison.png')

    # 4. 生成 Markdown 報告
    report = format_weekly_report(analysis, platform_comparison, insights)
    report_path = f'output/analytics/weekly_report_{start_date}.md'

    with open(report_path, 'w') as f:
        f.write(report)

    # 5. 生成 Excel 報告
    excel_path = f'output/analytics/weekly_report_{start_date}.xlsx'
    generate_excel_report(data, analysis, excel_path)

    return {
        'markdown': report_path,
        'excel': excel_path,
        'charts': charts_dir
    }
```

### Step 5: Generate Insights

```python
def generate_insights(analysis, platform_comparison):
    """生成可執行的洞察建議"""

    insights = []

    # 1. 標題類型分析
    if 'title_type_performance' in analysis:
        best_type = analysis['title_type_performance'].idxmax()
        insights.append({
            'category': '標題優化',
            'finding': f'{best_type}標題表現最佳',
            'recommendation': f'增加{best_type}標題使用比例至60%',
            'priority': 'high'
        })

    # 2. 發布時間優化
    if 'best_publishing_time' in analysis:
        best_time = analysis['best_publishing_time']
        insights.append({
            'category': '發布策略',
            'finding': f'{best_time}流量最高',
            'recommendation': f'重點文章安排在{best_time}發布',
            'priority': 'medium'
        })

    # 3. 平台優化
    top_platform = platform_comparison.index[0]
    insights.append({
        'category': '平台分配',
        'finding': f'{top_platform} ROI 最高',
        'recommendation': f'加強{top_platform}內容投入',
        'priority': 'high'
    })

    return insights
```

## Excel Report Format

**File**: `weekly_report_YYYYMMDD.xlsx`

**Sheets**:

### 1. Summary
```
整體表現概況
- 關鍵指標卡片
- 週對週變化
- 目標達成率
```

### 2. Top Articles
```
| 排名 | 標題 | URL | 瀏覽數 | 訪客數 | 停留時間 | 跳出率 | 分享數 |
```

### 3. Platform Comparison
```
| 平台 | 瀏覽數 | 佔比 | 訪客數 | CTR | 停留時間 | 跳出率 | ROI 評分 |
```

### 4. Daily Breakdown
```
| 日期 | 瀏覽數 | 訪客數 | 新訪客 | 停留時間 | 跳出率 | 轉化數 |
```

### 5. Traffic Sources
```
| 來源 | 媒介 | 瀏覽數 | 訪客數 | 新訪客比例 | 轉化率 |
```

### 6. Content Types
```
| 分類 | 文章數 | 總瀏覽 | 平均瀏覽 | 平均停留 | 平均 CTR |
```

## Best Practices

### 1. Data Quality

```yaml
確保數據準確性:
  - 驗證 GA4 Property ID 正確
  - 檢查時區設定一致
  - 排除內部流量（dev/staging）
  - 過濾 bot 流量
```

### 2. Report Timing

```yaml
最佳實踐:
  週報: 每週一早上 9:00 生成（涵蓋上週一~日）
  月報: 每月 1 號早上 9:00 生成（涵蓋上個月）

避免:
  - 週末生成（數據可能不完整）
  - 當日數據（GA4 有延遲）
```

### 3. Actionable Insights

```yaml
好的洞察必須包含:
  1. 數據發現（What）
  2. 原因分析（Why）
  3. 具體建議（How）
  4. 預期效果（Impact）

範例:
  發現: 數字型標題 CTR 高 30%
  原因: 讀者偏好具體、可量化的承諾
  建議: 下週發布 3 篇數字型標題文章
  預期: CTR 提升至 6.5%，流量增加 20%
```

### 4. Comparison Context

```yaml
總是提供對比:
  - WoW (Week over Week)
  - MoM (Month over Month)
  - YoY (Year over Year)
  - vs Target (實際 vs 目標)

不只說絕對值，要說相對變化
```

## Integration with Blog Manager

This skill fits into the workflow as **Phase 7**:

```
Phase 5.5: Multi-Platform Distributor → 文章發布到多平台
Phase 6: Community Manager → 社群互動管理
Phase 7: Analytics Reporter (this skill) → 週報/月報生成
Phase 7.5: Strategy Optimizer → 基於數據優化策略
```

## Automation Options

### Scheduled Reports

```yaml
週報自動化:
  觸發: 每週一 09:00
  指令: "生成上週的分析報告"
  輸出: output/analytics/weekly_report_YYYYMMDD.md

月報自動化:
  觸發: 每月 1 號 09:00
  指令: "生成上個月的月報"
  輸出: output/analytics/monthly_report_YYYYMM.md
```

### Alert Triggers

```yaml
異常警告:
  - 流量突降 >30%: 立即通知
  - 轉化率低於 0.5%: 每日檢查
  - Top 文章表現異常: 每週檢查
```

## Output Summary

After report generation:

```markdown
✅ Analytics Report Generated
━━━━━━━━━━━━━━━━━━━━━━━━

Report Type: Weekly
Period: 2025-11-04 ~ 2025-11-10
Generated: 2025-11-11 09:00:00

📊 Key Metrics:
  Total Pageviews: 12,450 (↑ 35%)
  Unique Visitors: 3,280 (↑ 28%)
  Avg Session: 3m 24s (↑ 18%)
  Bounce Rate: 45.2% (↓ 8%)

🏆 Top 3 Articles:
  1. "Claude Code 完整指南" - 4,230 views
  2. "AI 自動化實戰" - 3,180 views
  3. "WordPress 自動發布" - 2,340 views

📁 Output Files:
  - Markdown: output/analytics/weekly_report_20251104.md
  - Excel: output/analytics/weekly_report_20251104.xlsx
  - Charts: output/analytics/weekly_charts_20251104/

💡 Top Insights:
  1. 數字型標題 CTR 提升 42%
  2. 週二早上發布效果最佳
  3. Medium 平台 ROI 最高（4.5 星）

⏭️ Recommended Actions:
  1. 增加數字型標題比例至 70%
  2. 下週重點文章排在週二 08:00
  3. 加強 Medium 平台內容投入
```

## Troubleshooting

### GA MCP Connection Issues

**Problem**: Cannot fetch data from GA4

**Solutions**:
```bash
# 1. Verify MCP is running
/mcp list

# 2. Test GA connection
"請查詢過去 7 天的網站總瀏覽數"

# 3. Check credentials
cat ~/.claude/claude_desktop_config.json | grep google-analytics

# 4. Verify GA4 Property ID
echo $GA4_PROPERTY_ID
```

### Data Discrepancies

**Problem**: Numbers don't match GA4 UI

**Common Causes**:
- Timezone mismatch
- Date range interpretation
- Metric definition differences
- Sampling in large datasets

**Solution**:
```python
# Always specify timezone explicitly
query_params = {
    'start_date': '2025-11-04',
    'end_date': '2025-11-10',
    'timezone': 'Asia/Taipei'  # GMT+8
}
```

### Report Generation Fails

**Problem**: Script errors during generation

**Debug Steps**:
```bash
# 1. Check Python dependencies
pip list | grep pandas

# 2. Verify output directory exists
mkdir -p output/analytics

# 3. Check disk space
df -h

# 4. Run with verbose logging
python -v generate_report.py
```

---

**Skill Maintained By**: 喵哩文創 AI 寫手系統團隊
**Last Updated**: 2025-11-10
**Dependencies**: Google Analytics MCP, pandas, matplotlib
**Report Formats**: Markdown, Excel, PNG charts
