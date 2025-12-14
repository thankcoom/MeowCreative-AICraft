# Fact Verification Skill

## Skill Metadata
```yaml
name: fact-verification
version: 1.0.0
description: 事實驗證工具，用於檢測和驗證文章中的事實陳述、數據來源和專業聲明
author: 喵哩文創 AI 寫手系統
created: 2025-11-25
```

---

## 功能說明

此 Skill 提供自動化的事實驗證功能，幫助識別文章中需要驗證的事實陳述，並提供驗證建議。

### 主要功能

1. **事實陳述提取** - 自動識別文章中的事實性陳述
2. **數據來源檢查** - 檢查數據是否有可追溯來源
3. **幻覺風險評估** - 評估陳述的 LLM 幻覺風險
4. **驗證報告生成** - 生成詳細的驗證報告

---

## 使用方式

### 命令列使用

```bash
# 基本使用
python3 .claude/skills/fact-verification/verify.py \
    input_article.md \
    --output fact_check_report.md

# 指定驗證級別
python3 .claude/skills/fact-verification/verify.py \
    input_article.md \
    --level strict \
    --output fact_check_report.md

# 包含經驗檔案（用於區分真實經驗）
python3 .claude/skills/fact-verification/verify.py \
    input_article.md \
    --experience experience_profile.md \
    --output fact_check_report.md
```

### 參數說明

| 參數 | 必需 | 說明 |
|------|------|------|
| `input_article` | 是 | 待驗證的文章路徑 |
| `--output` | 否 | 輸出報告路徑（預設: fact_check_report.md） |
| `--level` | 否 | 驗證級別: `basic`, `standard`, `strict`（預設: standard） |
| `--experience` | 否 | 經驗檔案路徑（用於區分真實經驗） |
| `--format` | 否 | 輸出格式: `markdown`, `json`（預設: markdown） |

---

## 驗證級別

### Basic (基本)
- 只檢查明顯的數據和引用
- 適用於快速驗證
- 處理時間: ~1 分鐘

### Standard (標準) - 預設
- 檢查所有事實陳述
- 評估幻覺風險
- 適用於一般文章
- 處理時間: ~3 分鐘

### Strict (嚴格)
- 深度驗證所有陳述
- 交叉比對多個來源
- 適用於高可信度要求的內容
- 處理時間: ~5 分鐘

---

## 輸出格式

### Markdown 格式

```markdown
# 事實驗證報告

## 摘要
- 總事實陳述: 15
- 已驗證: 10 (66.7%)
- 部分驗證: 3 (20%)
- 無法驗證: 2 (13.3%)
- 可信度評分: 78/100

## 高風險項目
...

## 驗證詳情
...
```

### JSON 格式

```json
{
  "summary": {
    "total_statements": 15,
    "verified": 10,
    "partial": 3,
    "unverified": 2,
    "credibility_score": 78
  },
  "high_risk_items": [...],
  "verification_details": [...]
}
```

---

## 整合到工作流程

### 在 Blog Manager 中使用

此 Skill 由 Fact Checker Agent 自動調用，位於工作流程的 Phase 3.6。

```
Phase 3: Writer Agent
    ↓
Phase 3.6: Fact Checker Agent (使用此 Skill)
    ↓
Phase 3.7: Humanizer Agent
```

### 手動調用

也可以在任何時候手動調用進行事實檢查：

```bash
python3 .claude/skills/fact-verification/verify.py \
    output/session_*/draft_final.md \
    --output output/session_*/fact_check_report.md
```

---

## 事實類型識別

### 支援的事實類型

| 類型 | 說明 | 範例模式 |
|------|------|---------|
| 數據型 | 統計數據、百分比、數字 | `[0-9]+%`, `\$[0-9]+` |
| 聲明型 | 因果關係、比較、絕對性陳述 | `導致`, `最佳`, `唯一` |
| 引用型 | 研究、專家、官方來源 | `根據.*研究`, `專家表示` |
| 技術型 | 技術規格、功能描述 | `支援`, `兼容`, `API` |
| 時間型 | 日期、時間、年份 | `\d{4}年`, `最近` |

---

## 幻覺風險評估

### 風險指標

```yaml
高風險特徵:
  - 精確數據無來源
  - 無法找到的研究引用
  - 過度自信的絕對陳述
  - 虛構的專家或機構

中風險特徵:
  - 模糊的來源描述
  - 概括性統計
  - 未標註的比較

低風險特徵:
  - 有明確來源的數據
  - 可驗證的事實
  - 個人經驗（來自 experience_profile.md）
```

### 風險評分

- **0-20**: 低風險 - 有明確可靠來源
- **21-50**: 中風險 - 來源模糊但可驗證
- **51-80**: 高風險 - 無來源或模糊聲明
- **81-100**: 極高風險 - 可能是虛構

---

## 依賴

- Python 3.10+
- 無額外 Python 套件依賴

---

## 相關檔案

- `verify.py` - 主程式
- `patterns.yaml` - 事實類型識別模式
- `risk_calculator.py` - 風險計算模組

---

**Fact Verification Skill v1.0.0**
**發布日期**: 2025-11-25
