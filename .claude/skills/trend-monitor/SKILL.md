# 熱點引擎 Trend Monitor

熱點監控與自動內容生成系統，讓你比競品更快、更準、更有影響力。

## 核心功能

### 1. 多平台監控
- Google Trends (台灣/全球)
- PTT 熱門看板
- Dcard 熱門話題
- YouTube 趨勢影片
- 新聞 RSS 聚合

### 2. 熱度評分系統
- 即時熱度 (0-100)
- 上升速度 (爆發指數)
- 競爭度分析
- 時效性評估

### 3. 自動觸發寫作
- 熱度超過閾值自動產文
- 可設定關注領域過濾
- 支援人工審核模式

## 使用方式

### 即時掃描
```bash
python3 .claude/skills/trend-monitor/scan.py --source all
```

### 指定平台
```bash
python3 .claude/skills/trend-monitor/scan.py --source google_trends --region TW
python3 .claude/skills/trend-monitor/scan.py --source ptt --boards Gossiping,Tech_Job
```

### 自動監控模式
```bash
python3 .claude/skills/trend-monitor/monitor.py --interval 15 --auto-write
```

### 查看熱門話題
```bash
python3 .claude/skills/trend-monitor/scan.py --top 20
```

## 輸出格式

```yaml
topic: "話題關鍵字"
heat_score: 85
trend: "rising"  # rising/stable/falling
velocity: 2.3    # 上升速度倍數
sources:
  - platform: google_trends
    rank: 3
  - platform: ptt
    mentions: 127
recommended_action: "immediate"  # immediate/watch/skip
suggested_angles:
  - "教學型：如何..."
  - "觀點型：為什麼..."
  - "整理型：X 大重點"
```

## 配置

編輯 `.claude/config/trend-monitor.yaml` 設定：
- 監控頻率
- 關注領域
- 熱度閾值
- 自動發布設定
