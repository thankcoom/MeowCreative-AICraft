# Quality Prediction Skill

## Skill Metadata
```yaml
name: quality-prediction
version: 1.0.0
description: 預測文章品質分數，評估風險，提供改進建議
author: 喵哩文創 AI 寫手系統
created: 2025-11-26
```

---

## 功能說明

此 Skill 提供文章品質預測和風險評估功能，支援 Quality Predictor Agent 進行早期品質預測。

### 主要功能

1. **品質分數預測** - 預測 E-E-A-T、SEO、說服力等維度分數
2. **風險評估** - 識別事實錯誤、AI 偵測等風險
3. **趨勢分析** - 分析歷史品質趨勢
4. **改進建議** - 提供針對性的優化建議

---

## 使用方式

### 命令列使用

```bash
# 預測品質分數
python3 .claude/skills/quality-prediction/predict.py score \
    draft_final.md \
    --output prediction.json

# 評估風險
python3 .claude/skills/quality-prediction/predict.py risk \
    draft_final.md \
    --output risk_assessment.md

# 獲取改進建議
python3 .claude/skills/quality-prediction/predict.py suggest \
    draft_final.md \
    --target-score 90

# 分析歷史趨勢
python3 .claude/skills/quality-prediction/predict.py trend \
    --sessions 10 \
    --output trend_analysis.md

# 完整預測報告
python3 .claude/skills/quality-prediction/predict.py full \
    draft_final.md \
    --output quality_report.md
```

### 參數說明

| 命令 | 參數 | 說明 |
|------|------|------|
| `score` | `file`, `--output` | 預測品質分數 |
| `risk` | `file`, `--output` | 評估風險 |
| `suggest` | `file`, `--target-score` | 獲取改進建議 |
| `trend` | `--sessions`, `--output` | 歷史趨勢分析 |
| `full` | `file`, `--output` | 完整預測報告 |

---

## 預測維度

### E-E-A-T 評分

```yaml
Experience (經驗): 25%
  - 第一人稱使用
  - 個人經驗描述
  - 具體細節

Expertise (專業): 25%
  - 專業術語
  - 深度分析
  - 技術準確性

Authoritativeness (權威): 25%
  - 引用來源
  - 數據支持
  - 專家引言

Trustworthiness (可信): 25%
  - 平衡觀點
  - 限制說明
  - 更新標注
```

### SEO 評分

```yaml
關鍵字優化: 30%
  - 標題含關鍵字
  - 首段關鍵字
  - 關鍵字密度

結構品質: 30%
  - 標題層級
  - 段落長度
  - 列表使用

Meta 優化: 20%
  - Title 長度
  - Description
  - 關鍵字佈局

可讀性: 20%
  - 句子長度
  - 詞彙難度
  - 結構清晰
```

### 說服力評分

```yaml
AIDA 覆蓋: 40%
  - Attention
  - Interest
  - Desire
  - Action

心理觸發: 30%
  - 稀缺性
  - 社會證明
  - 權威性
  - 互惠

CTA 效果: 30%
  - 明確度
  - 出現頻率
  - 位置策略
```

---

## 風險類型

### Critical 風險

```yaml
fact_error_risk:
  description: "事實錯誤風險"
  threshold: 0.3
  indicators:
    - 未驗證數據
    - 絕對性陳述
    - 缺乏來源

ai_detection_risk:
  description: "AI 偵測風險"
  threshold: 0.4
  indicators:
    - 句式規律
    - 段落長度一致
    - 缺乏個人語氣
```

### High 風險

```yaml
credibility_risk:
  description: "可信度風險"
  threshold: 0.4
  indicators:
    - 缺乏專業支撐
    - 過度誇大
    - 來源不明
```

### Medium 風險

```yaml
seo_risk:
  description: "SEO 風險"
  threshold: 0.5
  indicators:
    - 關鍵字問題
    - 結構問題
    - Meta 缺失

engagement_risk:
  description: "參與度風險"
  threshold: 0.5
  indicators:
    - 開頭無吸引力
    - 內容枯燥
    - 缺乏互動
```

---

## 輸出格式

### 品質預測 (JSON)

```json
{
  "file": "draft_final.md",
  "timestamp": "2025-11-26T12:00:00Z",
  "predictions": {
    "eeat": {
      "score": 82,
      "confidence": 0.85,
      "components": {
        "experience": 80,
        "expertise": 85,
        "authoritativeness": 78,
        "trustworthiness": 84
      }
    },
    "seo": {
      "score": 85,
      "confidence": 0.88
    },
    "persuasion": {
      "score": 75,
      "confidence": 0.82
    },
    "engagement": {
      "score": 78,
      "confidence": 0.80
    },
    "overall": {
      "score": 80,
      "confidence": 0.84,
      "grade": "B+"
    }
  },
  "execution_recommendation": "standard_path"
}
```

### 風險評估 (Markdown)

```markdown
# 風險評估報告

## 風險摘要

| 風險類型 | 嚴重度 | 機率 | 狀態 |
|----------|--------|------|------|
| 說服力不足 | 高 | 65% | ⚠️ 需處理 |
| 開頭吸引力 | 中 | 45% | ⚠️ 建議改善 |
| AI 偵測 | 低 | 25% | ✅ 正常 |

## 詳細分析

### 高風險: 說服力不足
**原因**:
- CTA 僅出現 1 次
- 未檢測到心理觸發詞

**建議**:
- 執行 Phase 3.8 強化
- 增加 2-3 個 CTA
```

---

## 整合方式

### Quality Predictor Agent 整合

此 Skill 由 Quality Predictor Agent 在 Phase 3 後自動調用。

### 決策支援

根據預測結果提供執行建議：
- 高品質路徑 (≥85): 可跳過部分 Phase
- 標準路徑 (70-84): 完整執行
- 改進路徑 (<70): 需要額外強化

---

**Quality Prediction Skill v1.0.0**
**發布日期**: 2025-11-26
