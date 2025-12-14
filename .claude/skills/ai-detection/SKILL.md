# AI Detection Skill

## Skill Metadata
```yaml
name: ai-detection
version: 1.0.0
description: AI 內容偵測工具，分析文章的 AI 生成特徵並提供人類化改進建議
author: 喵哩文創 AI 寫手系統
created: 2025-11-25
```

---

## 功能說明

此 Skill 提供 AI 內容偵測功能，模擬常見 AI 偵測工具的檢測邏輯，幫助識別文章中的 AI 特徵，並提供人類化改進建議。

### 主要功能

1. **AI 特徵掃描** - 識別典型的 AI 寫作模式
2. **困惑度分析** - 評估文字的「可預測性」
3. **爆發度分析** - 評估句子長度變化
4. **人類化建議** - 提供具體的改進建議
5. **偵測分數估算** - 模擬 AI 偵測工具的評分

---

## 使用方式

### 命令列使用

```bash
# 基本使用
python3 .claude/skills/ai-detection/detect.py \
    input_article.md \
    --output ai_detection_report.md

# 指定輸出格式
python3 .claude/skills/ai-detection/detect.py \
    input_article.md \
    --format json \
    --output ai_detection_report.json

# 詳細模式（包含所有分析細節）
python3 .claude/skills/ai-detection/detect.py \
    input_article.md \
    --verbose \
    --output ai_detection_report.md
```

### 參數說明

| 參數 | 必需 | 說明 |
|------|------|------|
| `input` | 是 | 待分析的文章路徑 |
| `--output`, `-o` | 否 | 輸出報告路徑（預設: ai_detection_report.md） |
| `--format`, `-f` | 否 | 輸出格式: `markdown`, `json`（預設: markdown） |
| `--verbose`, `-v` | 否 | 詳細模式，輸出更多分析細節 |
| `--threshold` | 否 | AI 偵測閾值 (0-100)，低於此值視為通過（預設: 40） |

---

## 檢測維度

### 1. 句式重複率

檢測相同句子開頭出現的頻率。

**AI 特徵**: 連續使用 "首先...其次...最後..." 或 "這個...這個...這個..."

**評分標準**:
- < 10%: 優秀 (像人類)
- 10-20%: 良好
- 20-30%: 需改進
- > 30%: AI 特徵明顯

### 2. 段落長度變異度

評估各段落字數的標準差。

**AI 特徵**: 所有段落長度幾乎相同

**評分標準**:
- 標準差 > 40: 優秀 (人類特徵)
- 30-40: 良好
- 20-30: 需改進
- < 20: AI 特徵明顯

### 3. 情感詞彙密度

計算情感詞彙佔總詞彙的比例。

**AI 特徵**: 情感詞彙很少或完全沒有

**評分標準**:
- > 3%: 優秀
- 2-3%: 良好
- 1-2%: 需改進
- < 1%: AI 特徵明顯

### 4. 困惑度 (Perplexity)

評估文字的「可預測性」。AI 生成的文字通常太過「順暢」。

**評分方法**: 基於詞彙選擇的意外度

### 5. 爆發度 (Burstiness)

評估句子長度的變化程度。人類寫作有長短交替的特徵。

**評分方法**: 句子長度的變異係數

---

## 輸出格式

### Markdown 格式

```markdown
# AI 偵測報告

## 整體評估
- **AI 偵測分數**: 35/100 (越低越像人類)
- **評級**: B (偏向人類)
- **建議**: 已接近人類寫作風格，可選擇性優化

## 各維度分析

| 維度 | 分數 | 狀態 |
|------|------|------|
| 句式重複率 | 12% | 良好 |
| 段落變異度 | 35 | 良好 |
| 情感詞密度 | 2.1% | 良好 |
| 困惑度 | 中 | 可接受 |
| 爆發度 | 中 | 可接受 |

## 發現的 AI 特徵
...

## 人類化建議
...
```

### JSON 格式

```json
{
  "ai_score": 35,
  "grade": "B",
  "dimensions": {
    "repetition_rate": 0.12,
    "paragraph_variance": 35,
    "emotion_density": 0.021,
    "perplexity": "medium",
    "burstiness": "medium"
  },
  "ai_features_found": [...],
  "humanization_suggestions": [...]
}
```

---

## 評級標準

| 分數 | 評級 | 說明 | 建議行動 |
|------|------|------|---------|
| 0-20 | A | 很像人類寫的 | 無需修改 |
| 21-40 | B | 偏向人類 | 可選優化 |
| 41-60 | C | 難以判斷 | 建議優化 |
| 61-80 | D | 偏向 AI | 需要修改 |
| 81-100 | F | 很像 AI 寫的 | 必須大幅修改 |

---

## AI 特徵庫

### 需要消除的特徵

```yaml
結構性特徵:
  - 過度使用序號 (首先、其次、最後)
  - 段落長度一致
  - 固定的開頭結尾模式

語言特徵:
  - 缺乏情感表達
  - 過度正式
  - 重複使用相同句式
  - 缺乏對話感

內容特徵:
  - 過度依賴清單
  - 觀點過於平衡
  - 缺乏個人經驗
  - 沒有不確定性表達
```

---

## 整合到工作流程

### 在 Blog Manager 中使用

此 Skill 由 Humanizer Agent 自動調用，用於評估人類化處理效果。

```
Phase 3.7: Humanizer Agent
    ├── 使用 AI Detection Skill 分析原文
    ├── 執行人類化處理
    └── 再次使用 AI Detection Skill 驗證效果
```

### 手動調用

```bash
# 在任何時候檢測文章的 AI 特徵
python3 .claude/skills/ai-detection/detect.py \
    output/session_*/draft_final.md \
    --output output/session_*/ai_detection_report.md
```

---

## 依賴

- Python 3.10+
- 無額外 Python 套件依賴

---

## 相關檔案

- `detect.py` - 主程式
- `patterns.yaml` - AI 特徵識別模式
- `emotion_words.txt` - 情感詞彙庫
- `transition_words.txt` - 過渡詞彙庫

---

**AI Detection Skill v1.0.0**
**發布日期**: 2025-11-25
