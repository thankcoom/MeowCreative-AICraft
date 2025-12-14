# Performance Monitor Skill v2.6.0

## Skill Metadata
```yaml
name: performance-monitor
version: 2.6.0
description: 即時追蹤 Session 執行效能，生成效能報告和優化建議（含 Search Everywhere 優化 Phases）
author: 喵哩文創 AI 寫手系統
created: 2025-11-26
updated: 2025-12-14
status: 完整實現 ✅
```

---

## v2.5.0 更新

### 新增功能

1. **效能追蹤器** (`tracker.py`) - 即時追蹤 Session 效能
2. **效能儀表板** (`dashboard/index.html`) - 可視化效能趨勢
3. **智慧瓶頸識別** - 自動識別效能瓶頸並生成建議
4. **趨勢分析** - 滾動平均和歷史比較

### 架構變更

```
.claude/skills/performance-monitor/
├── SKILL.md              # 本文件
├── monitor.py            # 原有監控工具
└── tracker.py            # 🆕 v2.5.0 效能追蹤器

.claude/performance/
├── benchmarks.json       # 效能基準
├── sessions.jsonl        # Session 效能記錄
├── trends.json           # 趨勢分析數據
└── dashboard/
    └── index.html        # 🆕 可視化儀表板
```

---

## 功能說明

### 核心功能

| 功能 | 說明 | 狀態 |
|------|------|------|
| Session 追蹤 | 追蹤完整 Session 執行 | ✅ |
| Phase 計時 | 記錄每個 Phase 的執行時間 | ✅ |
| 效能評級 | A+/A/B/C/D 評級計算 | ✅ |
| 瓶頸識別 | 自動識別耗時過長的 Phase | ✅ |
| 優化建議 | 生成可操作的優化建議 | ✅ |
| 趨勢分析 | 歷史效能趨勢和滾動平均 | ✅ |
| 可視化儀表板 | HTML 圖表展示 | ✅ |

---

## 使用方式

### tracker.py 命令列介面

```bash
# 查看效能狀態
python3 .claude/skills/performance-monitor/tracker.py status

# 開始追蹤 Session
python3 .claude/skills/performance-monitor/tracker.py start \
    --session-id session_20251211_120000

# 記錄 Phase 開始
python3 .claude/skills/performance-monitor/tracker.py phase-start --phase 3

# 記錄 Phase 結束
python3 .claude/skills/performance-monitor/tracker.py phase-end --phase 3

# 結束 Session 並生成報告
python3 .claude/skills/performance-monitor/tracker.py end

# 從歷史建立效能基準
python3 .claude/skills/performance-monitor/tracker.py calibrate \
    --from-sessions "output/session_*"

# 生成儀表板數據
python3 .claude/skills/performance-monitor/tracker.py dashboard \
    --output .claude/performance/dashboard/data.json
```

### 命令參考

| 命令 | 參數 | 說明 |
|------|------|------|
| `status` | - | 顯示追蹤狀態和統計 |
| `start` | `--session-id` | 開始追蹤 Session |
| `phase-start` | `--phase` | 記錄 Phase 開始 |
| `phase-end` | `--phase`, `--success/--failed` | 記錄 Phase 結束 |
| `end` | `--success/--failed` | 結束 Session |
| `calibrate` | `--from-sessions` | 從歷史建立基準 |
| `dashboard` | `--output` | 生成儀表板數據 |

### Python API

```python
from performance_monitor.tracker import PerformanceTracker

# 初始化
tracker = PerformanceTracker()

# 開始追蹤
tracker.start_session("session_20251211_120000")

# 記錄 Phase
tracker.phase_start("3")
# ... Phase 執行 ...
tracker.phase_end("3", success=True)

# 結束並獲取報告
report = tracker.end_session(success=True)

# 查看狀態
status = tracker.get_status()
```

---

## 效能評級標準

### 評級規則

```yaml
A+ (優秀):
  max_duration: 480   # < 8 分鐘
  description: "極佳效能，繼續保持"

A (良好):
  max_duration: 600   # < 10 分鐘
  description: "良好效能，符合預期"

B (可接受):
  max_duration: 900   # < 15 分鐘
  description: "可接受，有優化空間"

C (需改進):
  max_duration: 1200  # < 20 分鐘
  description: "需要優化"

D (待優化):
  max_duration: ∞     # > 20 分鐘
  description: "嚴重需要優化"
```

### Phase 基準時間

```yaml
Phase 基準 (秒):
  "0": 60       # Experience Collector
  "1": 45       # Content Analyst
  "2a": 90      # Research Agent
  "2b": 60      # Style Matcher
  "3": 180      # Writer Agent
  "3.4": 30     # Quality Predictor
  "3.5": 90     # Editor Agent
  "3.6": 60     # Fact Checker
  "3.7": 60     # Humanizer
  "3.8": 60     # Persuasion
  "3.9": 60     # Storyteller
  "4": 90       # SEO Optimizer
  "4d": 45      # LLMO Optimizer 🆕 v2.6.0
  "4e": 45      # GEO Optimizer 🆕 v2.6.0
  "4f": 30      # VSO Optimizer 🆕 v2.6.0
  "4g": 30      # CRO Optimizer 🆕 v2.6.0
  "4h": 30      # AISO Scorer 🆕 v2.6.0
  "5": 30       # Publisher
  "11": 30      # Memory Agent
  "12": 120     # Persona Adapter
  "13": 15      # Performance Optimizer
```

---

## 數據結構

### Session 效能記錄

```json
{
  "session_id": "session_20251211_120000",
  "start_time": "2025-12-11T12:00:00",
  "end_time": "2025-12-11T12:10:34",
  "total_duration": 634,
  "success": true,
  "phases": [
    {
      "phase": "3",
      "start": "2025-12-11T12:03:00",
      "end": "2025-12-11T12:06:00",
      "duration": 180,
      "success": true,
      "benchmark": 180,
      "efficiency": 1.0
    }
  ],
  "statistics": {
    "total_phases": 8,
    "successful_phases": 8,
    "failed_phases": 0,
    "avg_phase_duration": 79.25,
    "max_phase_duration": 180,
    "min_phase_duration": 30
  },
  "grade": "A",
  "bottlenecks": [],
  "suggestions": ["效能表現良好，繼續保持！"]
}
```

### 趨勢數據

```json
{
  "updated_at": "2025-12-11T12:00:00",
  "sessions": [
    {
      "session_id": "session_20251211_120000",
      "timestamp": "2025-12-11T12:10:34",
      "duration": 634,
      "grade": "A",
      "phase_count": 8
    }
  ],
  "averages": {
    "duration_5": 650.0,
    "phase_count_5": 8.2,
    "duration_20": 720.5
  }
}
```

---

## 效能儀表板

### 開啟方式

```bash
# 方法 1: 直接開啟
open .claude/performance/dashboard/index.html

# 方法 2: 本地伺服器
cd .claude/performance/dashboard
python3 -m http.server 8080
# 然後訪問 http://localhost:8080
```

### 儀表板功能

1. **系統狀態卡片**
   - 追蹤狀態
   - 已記錄 Session 數

2. **最新評級**
   - 最近 Session 評級
   - 執行時間

3. **平均效能**
   - 近 5 次平均時間
   - 進度條可視化

4. **評級分布圖**
   - A+/A/B/C/D 分布
   - 圓餅圖展示

5. **執行時間趨勢**
   - 最近 20 次趨勢線
   - 折線圖展示

6. **高效模式**
   - 來自 Memory 系統的成功模式
   - 成功率排序

7. **優化建議**
   - 並行執行機會
   - 智慧跳過建議
   - 快取策略

---

## 瓶頸識別

### 識別規則

當 Phase 執行時間超過基準的 150% 時，標記為瓶頸：

```python
if phase['duration'] > benchmark * 1.5:
    severity = 'high' if duration > benchmark * 2 else 'medium'
    bottlenecks.append({
        'phase': phase_id,
        'duration': duration,
        'benchmark': benchmark,
        'excess': duration - benchmark,
        'severity': severity
    })
```

### 優化建議生成

| 瓶頸 | 建議 |
|------|------|
| Phase 2a 過慢 | 使用快取或縮小研究範圍 |
| Phase 3 過慢 | 簡化大綱或使用範本 |
| Phase 4 過慢 | 減少關鍵字分析數量 |
| 總時間 > 15min | 啟用 Phase 2a/2b 並行 |
| Phase 數 > 10 | 使用 Quality Predictor 跳過 |

---

## 整合方式

### Blog Manager 整合

在 v2.5.0 中，效能追蹤器會自動整合到工作流程：

```
Session 開始
    ↓
tracker.start_session()  ← 自動啟動
    ↓
Phase 執行
    ↓
tracker.phase_start/end()  ← 每個 Phase
    ↓
Session 結束
    ↓
tracker.end_session()  ← 自動生成報告
    ↓
更新 trends.json  ← 自動更新趨勢
```

### 手動分析

適用於：
- 回顧分析歷史 Session
- 比較不同執行策略
- 調試效能問題

```bash
# 分析特定 Session
python3 tracker.py status

# 查看效能基準
cat .claude/performance/benchmarks.json

# 查看趨勢數據
cat .claude/performance/trends.json
```

---

## 最佳實踐

### 1. 定期校準基準

```bash
# 每週執行一次
python3 tracker.py calibrate --from-sessions "output/session_*"
```

### 2. 監控趨勢

定期查看儀表板，觀察：
- 執行時間是否穩定
- 評級分布是否健康
- 是否有新的瓶頸

### 3. 根據建議優化

當儀表板顯示優化建議時：
- 優先處理高嚴重性瓶頸
- 測試並行執行策略
- 調整快取配置

---

## 故障排除

### Q: 儀表板顯示空白？

```bash
# 確保有效能數據
ls .claude/performance/trends.json

# 如果沒有，執行至少一個 Session 或校準
python3 tracker.py calibrate --from-sessions "output/session_*"
```

### Q: 評級不準確？

```bash
# 重新校準基準
python3 tracker.py calibrate --from-sessions "output/session_*"

# 檢查基準數據
cat .claude/performance/benchmarks.json
```

### Q: 趨勢圖不更新？

```bash
# 手動更新儀表板數據
python3 tracker.py dashboard --output .claude/performance/dashboard/data.json

# 重新整理瀏覽器
```

---

**Performance Monitor Skill v2.6.0**
**發布日期**: 2025-12-14
**狀態**: 完整實現 ✅

---

## v2.6.0 變更

### 新增 Search Everywhere Phases

| Phase | 名稱 | 基準時間 |
|-------|------|----------|
| 4d | LLMO Optimizer | 45秒 |
| 4e | GEO Optimizer | 45秒 |
| 4f | VSO Optimizer | 30秒 |
| 4g | CRO Optimizer | 30秒 |
| 4h | AISO Scorer | 30秒 |

### 配合 Blog Manager v2.6.0

- 支援完整 AISO 優化流程追蹤
- 新增搜尋優化 Phase 效能監控
- 更新基準數據以包含新 Phases
