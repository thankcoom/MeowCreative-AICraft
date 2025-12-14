# Learning Database Skill

## Skill Metadata
```yaml
name: learning-database
version: 1.0.0
description: 管理和操作學習數據庫，支援模式存儲、用戶偏好管理和知識累積
author: 喵哩文創 AI 寫手系統
created: 2025-11-26
```

---

## 功能說明

此 Skill 提供學習數據庫的管理功能，支援 Memory Agent 進行知識累積和偏好管理。

### 主要功能

1. **模式管理** - 存儲和查詢成功/失敗模式
2. **偏好管理** - 管理用戶寫作偏好
3. **知識存儲** - 維護術語表和規則庫
4. **歷史追蹤** - 記錄 session 歷史和效能
5. **數據分析** - 生成學習洞察報告

---

## 使用方式

### 命令列使用

```bash
# 初始化學習數據庫
python3 .claude/skills/learning-database/manage.py init

# 添加成功模式
python3 .claude/skills/learning-database/manage.py add-pattern \
    --type success \
    --category opening \
    --pattern "問句開頭" \
    --example "你是否也曾經..." \
    --context how-to

# 查詢模式
python3 .claude/skills/learning-database/manage.py query-patterns \
    --category opening \
    --min-success-rate 0.7

# 更新用戶偏好
python3 .claude/skills/learning-database/manage.py update-preferences \
    --file user_preferences.yaml

# 記錄 session
python3 .claude/skills/learning-database/manage.py log-session \
    --session-dir output/session_20251126_120000 \
    --score 85 \
    --feedback "用戶滿意"

# 生成學習報告
python3 .claude/skills/learning-database/manage.py generate-report \
    --type weekly \
    --output learning_report.md

# 清理過期數據
python3 .claude/skills/learning-database/manage.py cleanup \
    --older-than 90
```

### 參數說明

| 命令 | 參數 | 說明 |
|------|------|------|
| `init` | - | 初始化數據庫結構 |
| `add-pattern` | `--type`, `--category`, `--pattern`, `--example`, `--context` | 添加模式 |
| `query-patterns` | `--category`, `--min-success-rate`, `--limit` | 查詢模式 |
| `update-preferences` | `--file` | 更新偏好設定 |
| `log-session` | `--session-dir`, `--score`, `--feedback` | 記錄 session |
| `generate-report` | `--type`, `--output` | 生成報告 |
| `cleanup` | `--older-than` | 清理舊數據 |

---

## 數據結構

### 目錄結構

```
.claude/memory/
├── config.yaml               # 配置檔案
├── user_preferences/
│   ├── style.yaml           # 風格偏好
│   ├── content.yaml         # 內容偏好
│   └── workflow.yaml        # 工作流程偏好
│
├── patterns/
│   ├── success.json         # 成功模式
│   ├── failed.json          # 失敗模式
│   └── index.json           # 模式索引
│
├── knowledge/
│   ├── terminology.yaml     # 術語表
│   ├── forbidden.yaml       # 禁用詞
│   └── rules.yaml           # 風格規則
│
├── history/
│   ├── sessions.jsonl       # Session 歷史
│   ├── feedback.jsonl       # 反饋記錄
│   └── metrics.jsonl        # 效能指標
│
└── cache/
    └── recent_patterns.json # 最近使用的模式快取
```

### 模式格式

```json
{
  "id": "pattern_001",
  "type": "success",
  "category": "opening",
  "pattern": "問句開頭 + 痛點描述",
  "description": "使用問句吸引注意，立即連結讀者痛點",
  "example": "你是否也曾經花了好幾個小時寫文章，卻發現沒人看？",
  "context": ["how-to", "problem-solving"],
  "metrics": {
    "usage_count": 23,
    "success_rate": 0.85,
    "avg_engagement": 4.2
  },
  "created_at": "2025-11-26T12:00:00Z",
  "updated_at": "2025-11-26T12:00:00Z"
}
```

### 偏好格式

```yaml
# style.yaml
tone:
  formality: 0.6      # 0-1, 越高越正式
  warmth: 0.8         # 0-1, 越高越溫暖
  humor: 0.3          # 0-1, 越高越幽默
  directness: 0.7     # 0-1, 越高越直接

vocabulary:
  complexity: "medium"  # simple/medium/complex
  jargon_level: "low"   # none/low/medium/high

structure:
  paragraph_length: "medium"  # short/medium/long
  header_frequency: "normal"  # sparse/normal/dense
  list_usage: "high"          # low/medium/high
```

---

## API 介面

### Python API

```python
from learning_database import LearningDB

# 初始化
db = LearningDB()

# 添加模式
db.add_pattern(
    pattern_type="success",
    category="opening",
    pattern="問句開頭",
    example="你是否...",
    context=["how-to"]
)

# 查詢模式
patterns = db.query_patterns(
    category="opening",
    min_success_rate=0.7,
    limit=10
)

# 更新偏好
db.update_preference("tone.formality", 0.7)

# 記錄反饋
db.log_feedback(
    session_id="session_20251126",
    feedback_type="positive",
    details="用戶喜歡開頭風格"
)

# 獲取建議
suggestions = db.get_suggestions(
    context="how-to",
    element="opening"
)
```

---

## 學習機制

### 模式學習

```yaml
學習流程:
  1. 收集:
     - 從 session 輸出收集數據
     - 記錄用戶修改
     - 追蹤發布後效能

  2. 分析:
     - 識別重複出現的模式
     - 計算成功率
     - 關聯上下文

  3. 存儲:
     - 超過閾值的模式納入數據庫
     - 更新現有模式統計
     - 清理低效模式

  4. 應用:
     - 在新 session 中推薦
     - 根據上下文過濾
     - 持續優化權重
```

### 成功率計算

```python
def calculate_success_rate(pattern):
    total_uses = pattern.metrics.usage_count
    positive_outcomes = count_positive_outcomes(pattern)

    # 貝葉斯估計 (避免小樣本偏差)
    prior_success = 0.5
    prior_weight = 10

    adjusted_rate = (
        positive_outcomes + prior_success * prior_weight
    ) / (total_uses + prior_weight)

    return adjusted_rate
```

---

## 報告格式

### 週報模板

```markdown
# 學習數據庫週報

**報告期間**: 2025-11-20 ~ 2025-11-26
**生成時間**: 2025-11-26 12:00

## 摘要統計

| 指標 | 本週 | 上週 | 變化 |
|------|------|------|------|
| Session 數量 | 15 | 12 | +25% |
| 平均品質分數 | 87 | 84 | +3.6% |
| 新增模式 | 8 | 5 | +60% |
| 用戶滿意度 | 4.5/5 | 4.3/5 | +4.7% |

## 新發現模式

### 高效模式 (成功率 >80%)
1. **開頭技巧**: 數據 + 問句組合
   - 成功率: 87%
   - 使用次數: 6

### 需避免模式
1. **過長導言**: 超過 200 字的開頭
   - 成功率: 35%
   - 建議: 控制在 100 字以內

## 用戶偏好趨勢

- 語調: 偏向更口語化 (formality: 0.6 → 0.5)
- 段落: 偏好更短段落 (medium → short)

## 建議優化

1. 增加「數據開頭」模式的使用
2. 減少導言長度
3. 增加互動元素

---
*自動生成 by Learning Database Skill*
```

---

## 配置選項

### config.yaml

```yaml
# 學習數據庫配置

database:
  location: ".claude/memory"
  backup_enabled: true
  backup_frequency: "daily"

learning:
  min_samples_for_pattern: 5     # 最少樣本數
  success_threshold: 0.6          # 成功率閾值
  decay_rate: 0.95               # 時間衰減率

storage:
  max_patterns: 1000
  max_history_days: 90
  compression: true

performance:
  cache_enabled: true
  cache_size: 100
  lazy_loading: true

privacy:
  anonymize_content: true
  retention_days: 365
```

---

## 整合到工作流程

### Memory Agent 整合

此 Skill 由 Memory Agent 自動調用，用於：

1. **Session 開始時**: 載入相關模式和偏好
2. **Session 進行中**: 即時學習用戶修改
3. **Session 結束時**: 存儲新學習到的知識

### 手動調用

```bash
# 查看當前學習狀態
python3 .claude/skills/learning-database/manage.py status

# 導出學習數據
python3 .claude/skills/learning-database/manage.py export \
    --format json \
    --output learning_export.json

# 導入學習數據
python3 .claude/skills/learning-database/manage.py import \
    --file learning_backup.json
```

---

## 數據保護

### 隱私原則

```yaml
數據保護:
  - 不存儲完整文章內容
  - 只保留模式和統計
  - 自動匿名化敏感資訊
  - 支援用戶刪除請求

用戶控制:
  - 可查看所有學習數據
  - 可刪除特定記錄
  - 可完全重置數據庫
  - 可禁用學習功能
```

---

**Learning Database Skill v1.0.0**
**發布日期**: 2025-11-26
