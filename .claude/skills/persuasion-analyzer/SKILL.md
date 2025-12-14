# Persuasion Analyzer Skill

## Skill Metadata
```yaml
name: persuasion-analyzer
version: 1.0.0
description: 分析文章的說服力結構，評估 AIDA、PAS、4Cs 等框架的應用程度，提供優化建議
author: 喵哩文創 AI 寫手系統
created: 2025-11-25
```

---

## 功能說明

此 Skill 提供說服力分析功能，幫助評估文章在各種說服力框架下的表現，並提供具體的優化建議。

### 主要功能

1. **框架檢測** - 識別文章使用的說服力框架
2. **維度評分** - 評估各說服力維度的表現
3. **心理觸發分析** - 檢測心理觸發元素的使用
4. **CTA 效果評估** - 分析行動呼籲的強度
5. **優化建議** - 提供具體的改進方向

---

## 使用方式

### 命令列使用

```bash
# 基本使用
python3 .claude/skills/persuasion-analyzer/analyze.py \
    input_article.md \
    --output persuasion_report.md

# 指定框架分析
python3 .claude/skills/persuasion-analyzer/analyze.py \
    input_article.md \
    --framework AIDA \
    --output persuasion_report.md

# JSON 輸出
python3 .claude/skills/persuasion-analyzer/analyze.py \
    input_article.md \
    --format json \
    --output persuasion_report.json
```

### 參數說明

| 參數 | 必需 | 說明 |
|------|------|------|
| `input` | 是 | 待分析的文章路徑 |
| `--output`, `-o` | 否 | 輸出報告路徑（預設: persuasion_report.md） |
| `--framework`, `-f` | 否 | 指定分析框架: `AIDA`, `PAS`, `4Cs`, `all`（預設: all） |
| `--format` | 否 | 輸出格式: `markdown`, `json`（預設: markdown） |

---

## 分析維度

### 1. AIDA 框架分析

| 階段 | 權重 | 評估標準 |
|------|------|---------|
| Attention | 20% | 開頭吸引力、震撼性陳述 |
| Interest | 25% | 好處展示、好奇心製造 |
| Desire | 30% | 社會證明、成果展示、情感連結 |
| Action | 25% | CTA 明確性、門檻降低、緊迫感 |

### 2. PAS 框架分析

| 階段 | 權重 | 評估標準 |
|------|------|---------|
| Problem | 35% | 痛點明確性、共鳴度 |
| Agitate | 30% | 問題激化、情感強度 |
| Solution | 35% | 解決方案清晰度、可行性 |

### 3. 4Cs 框架分析

| 元素 | 權重 | 評估標準 |
|------|------|---------|
| Clear | 25% | 訊息清晰度、易理解性 |
| Concise | 25% | 簡潔度、無冗餘 |
| Compelling | 25% | 吸引力、情感連結 |
| Credible | 25% | 可信度、證據支持 |

### 4. 心理觸發分析

| 觸發 | 檢測標準 |
|------|---------|
| 稀缺性 | "限時"、"獨家"、"僅剩" |
| 社會證明 | 數據、評價、案例 |
| 權威性 | 專業背景、成就、認證 |
| 互惠 | 免費提供、先給價值 |
| 一致性 | 小承諾、認同引導 |
| 喜好 | 相似性、共同經歷 |

---

## 評分標準

### 總體評分

- **90-100**: A+ - 卓越，說服力極強
- **80-89**: A - 優秀，高說服力
- **70-79**: B - 良好，有效說服
- **60-69**: C - 及格，基本說服力
- **<60**: D - 需改進，說服力不足

### 各維度評分

每個維度獨立評分 (0-100)，最終加權計算總分。

---

## 輸出格式

### Markdown 格式

```markdown
# 說服力分析報告

## 總體評估
- **說服力分數**: 72/100
- **評級**: B (良好)
- **主要框架**: AIDA (部分應用)

## AIDA 分析

| 階段 | 分數 | 狀態 | 說明 |
|------|------|------|------|
| Attention | 65/100 | 需改進 | 開頭缺乏衝擊力 |
| Interest | 78/100 | 良好 | 好處展示清楚 |
| Desire | 70/100 | 良好 | 缺少社會證明 |
| Action | 68/100 | 需改進 | CTA 不夠明確 |

## 心理觸發檢測

| 觸發 | 狀態 | 次數 |
|------|------|------|
| 社會證明 | ✅ 使用 | 2 |
| 權威性 | ✅ 使用 | 1 |
| 稀缺性 | ❌ 未使用 | 0 |
| 互惠 | ❌ 未使用 | 0 |

## 優化建議
...
```

---

## 整合到工作流程

### 在 Blog Manager 中使用

此 Skill 由 Persuasion Agent 自動調用。

### 手動調用

```bash
python3 .claude/skills/persuasion-analyzer/analyze.py \
    output/session_*/draft_final.md \
    --output output/session_*/persuasion_report.md
```

---

**Persuasion Analyzer Skill v1.0.0**
**發布日期**: 2025-11-25
