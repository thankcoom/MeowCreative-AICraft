# Persona Template Skill

## Skill Metadata
```yaml
name: persona-template
version: 1.0.0
description: 管理和應用讀者 Persona 模板，支援內容適配和多版本生成
author: 喵哩文創 AI 寫手系統
created: 2025-11-26
```

---

## 功能說明

此 Skill 提供 Persona 模板的管理和應用功能，支援 Persona Adapter Agent 進行內容適配。

### 主要功能

1. **模板管理** - 創建、編輯、刪除 Persona 模板
2. **內容適配** - 根據 Persona 調整內容風格
3. **多版本生成** - 一稿多版自動轉換
4. **適配驗證** - 驗證適配品質

---

## 使用方式

### 命令列使用

```bash
# 列出所有 Persona 模板
python3 .claude/skills/persona-template/adapt.py list

# 查看特定 Persona 詳情
python3 .claude/skills/persona-template/adapt.py show beginner

# 適配內容到特定 Persona
python3 .claude/skills/persona-template/adapt.py adapt \
    input_article.md \
    --persona beginner \
    --output adapted_beginner.md

# 生成多版本
python3 .claude/skills/persona-template/adapt.py multi-adapt \
    input_article.md \
    --personas beginner,intermediate,expert \
    --output-dir adapted_versions/

# 創建自定義 Persona
python3 .claude/skills/persona-template/adapt.py create \
    --id custom_persona \
    --name "自定義讀者" \
    --config custom_persona.yaml

# 驗證適配品質
python3 .claude/skills/persona-template/adapt.py verify \
    original.md \
    adapted.md \
    --persona beginner
```

### 參數說明

| 命令 | 參數 | 說明 |
|------|------|------|
| `list` | - | 列出所有可用 Persona |
| `show` | `persona_id` | 顯示 Persona 詳情 |
| `adapt` | `input`, `--persona`, `--output` | 適配內容 |
| `multi-adapt` | `input`, `--personas`, `--output-dir` | 多版本生成 |
| `create` | `--id`, `--name`, `--config` | 創建新 Persona |
| `verify` | `original`, `adapted`, `--persona` | 驗證適配品質 |

---

## 預設 Persona 模板

### 1. beginner (新手小白)

```yaml
id: beginner
name: "新手小白"
description: "剛接觸此領域的初學者"
icon: "🌱"

characteristics:
  knowledge_level: 1
  attention_span: "short"
  preferred_format: "visual_heavy"
  reading_purpose: "learning"

adaptation:
  vocabulary:
    complexity: "simple"
    explain_jargon: true
    use_analogies: true
    max_syllables_per_word: 3

  structure:
    paragraph_length: "short"
    sentence_length: "short"
    header_frequency: "dense"
    list_usage: "high"
    visual_ratio: 0.3

  content:
    include_basics: true
    example_frequency: "high"
    step_by_step: true
    faq_section: true
    next_steps: true

  tone:
    formality: 0.3
    encouragement: 0.9
    patience: 0.9
```

### 2. intermediate (進階使用者)

```yaml
id: intermediate
name: "進階使用者"
description: "有基礎知識，尋求深入理解"
icon: "📈"

characteristics:
  knowledge_level: 3
  attention_span: "medium"
  preferred_format: "balanced"
  reading_purpose: "improvement"

adaptation:
  vocabulary:
    complexity: "medium"
    explain_jargon: "briefly"
    technical_terms: true

  structure:
    paragraph_length: "medium"
    sentence_length: "medium"
    header_frequency: "normal"
    list_usage: "medium"

  content:
    skip_basics: true
    best_practices: true
    common_mistakes: true
    advanced_tips: true

  tone:
    formality: 0.5
    directness: 0.7
```

### 3. expert (專家讀者)

```yaml
id: expert
name: "專家讀者"
description: "領域專家，尋求新知和深度"
icon: "🎓"

characteristics:
  knowledge_level: 5
  attention_span: "long"
  preferred_format: "text_heavy"
  reading_purpose: "reference"

adaptation:
  vocabulary:
    complexity: "high"
    technical_terms: true
    no_explanations: true

  structure:
    paragraph_length: "long"
    sentence_length: "varied"
    header_frequency: "sparse"
    list_usage: "low"

  content:
    deep_dive: true
    edge_cases: true
    comparisons: true
    original_insights: true

  tone:
    formality: 0.8
    precision: 0.9
```

### 4. decision_maker (決策者)

```yaml
id: decision_maker
name: "決策者"
description: "需要做出決定的管理者"
icon: "💼"

characteristics:
  knowledge_level: "varies"
  attention_span: "short"
  preferred_format: "summary_first"
  reading_purpose: "decision"

adaptation:
  vocabulary:
    complexity: "medium"
    business_terms: true
    avoid_tech_jargon: true

  structure:
    executive_summary: true
    bullet_points: "high"
    key_takeaways: true
    action_items: true

  content:
    roi_focus: true
    risk_analysis: true
    competitive_comparison: true
    recommendations: true

  tone:
    formality: 0.7
    urgency: 0.6
    confidence: 0.8
```

### 5. gen_z (Z 世代)

```yaml
id: gen_z
name: "Z 世代"
description: "1997-2012 年出生的年輕讀者"
icon: "⚡"

characteristics:
  knowledge_level: "varies"
  attention_span: "very_short"
  preferred_format: "snackable"
  reading_purpose: "quick_info"

adaptation:
  vocabulary:
    complexity: "simple"
    slang_ok: true
    emoji_usage: "moderate"

  structure:
    paragraph_length: "very_short"
    sentence_length: "short"
    visual_breaks: true
    interactive_elements: true

  content:
    relevance_first: true
    social_proof: true
    trend_connections: true
    shareable_quotes: true

  tone:
    formality: 0.1
    authenticity: 0.9
    fun_factor: 0.8
```

### 6. professional (專業人士)

```yaml
id: professional
name: "專業人士"
description: "有工作經驗的職場人士"
icon: "👔"

characteristics:
  knowledge_level: 3
  attention_span: "medium"
  preferred_format: "practical"
  reading_purpose: "application"

adaptation:
  vocabulary:
    complexity: "medium"
    industry_terms: true

  structure:
    problem_solution: true
    case_studies: true
    checklists: true
    templates: true

  content:
    practical_focus: true
    time_saving: true
    efficiency_tips: true
    tool_recommendations: true

  tone:
    formality: 0.6
    practical: 0.9
    professional: 0.8
```

---

## 適配規則

### 詞彙轉換

```yaml
vocabulary_rules:
  simple:
    max_word_length: 4
    avoid_passive: true
    explain_every_term: true

  medium:
    allow_common_jargon: true
    brief_explanations: true

  complex:
    full_technical_terms: true
    assume_knowledge: true
```

### 結構調整

```yaml
structure_rules:
  short_paragraphs:
    max_sentences: 3
    max_chars: 200

  medium_paragraphs:
    max_sentences: 5
    max_chars: 400

  long_paragraphs:
    max_sentences: 8
    max_chars: 600
```

### 內容深度

```yaml
depth_rules:
  basics:
    include:
      - what_is
      - why_matters
      - how_to_start
    exclude:
      - edge_cases
      - advanced_config

  intermediate:
    include:
      - best_practices
      - common_mistakes
      - optimization
    exclude:
      - basics
      - trivial_examples

  expert:
    include:
      - edge_cases
      - performance
      - internals
    exclude:
      - basics
      - hand_holding
```

---

## 輸出格式

### 適配報告

```markdown
# Persona 適配報告

## 基本資訊
- **原始檔案**: input_article.md
- **目標 Persona**: beginner (新手小白)
- **適配時間**: 2025-11-26 12:00

## 適配統計

| 指標 | 原始 | 適配後 | 變化 |
|------|------|--------|------|
| 字數 | 2000 | 2800 | +40% |
| 平均句長 | 25字 | 15字 | -40% |
| 專業術語 | 45個 | 12個 | -73% |
| 解釋數量 | 5處 | 28處 | +460% |
| 範例數量 | 3個 | 12個 | +300% |

## 主要調整

### 詞彙調整
- 替換 23 個專業術語為簡單說法
- 新增 15 處類比解釋
- 移除 8 個非必要的縮寫

### 結構調整
- 長段落拆分: 12 處
- 新增小標題: 5 個
- 新增列表: 8 處

### 內容調整
- 新增基礎解釋: 10 處
- 新增實際範例: 9 個
- 新增 FAQ: 5 題

## 品質檢查

- ✅ 核心訊息保留: 100%
- ✅ 可讀性符合目標: Flesch 78 (目標 ≥70)
- ✅ 風格一致性: 92%
- ✅ 無事實錯誤

## 建議

1. 可考慮再增加 2-3 個視覺圖示
2. 第 3 節的範例可以更生活化
```

---

## 整合到工作流程

### Persona Adapter Agent 整合

此 Skill 由 Persona Adapter Agent 自動調用，用於：

1. **載入 Persona**: 獲取目標讀者設定
2. **執行適配**: 根據規則轉換內容
3. **品質驗證**: 確認適配結果

### 手動調用

```bash
# 快速適配
python3 .claude/skills/persona-template/adapt.py adapt \
    output/session_*/draft_final.md \
    --persona beginner \
    --output output/session_*/beginner_version.md

# 批量生成多版本
python3 .claude/skills/persona-template/adapt.py multi-adapt \
    output/session_*/draft_final.md \
    --personas beginner,intermediate,expert,decision_maker \
    --output-dir output/session_*/adapted_versions/
```

---

## 自定義 Persona

### 創建新模板

```yaml
# my_persona.yaml
id: startup_founder
name: "創業家"
description: "正在創業或計劃創業的人"
icon: "🚀"

characteristics:
  knowledge_level: 3
  attention_span: "short"
  preferred_format: "action_oriented"
  reading_purpose: "immediate_application"

adaptation:
  vocabulary:
    complexity: "medium"
    startup_terms: true
    no_corporate_jargon: true

  structure:
    actionable_first: true
    time_estimates: true
    resource_links: true
    quick_wins: true

  content:
    mvp_focus: true
    cost_conscious: true
    growth_hacking: true
    real_examples: true

  tone:
    formality: 0.4
    urgency: 0.7
    motivation: 0.9
```

### 註冊自定義 Persona

```bash
python3 .claude/skills/persona-template/adapt.py create \
    --id startup_founder \
    --name "創業家" \
    --config my_persona.yaml
```

---

## 評估指標

### 適配品質分數

```yaml
評分標準:
  核心訊息保留: 40%
  風格匹配度: 30%
  可讀性達標: 20%
  結構適當: 10%

通過閾值:
  總分: ≥80/100
  核心訊息: ≥95%
  可讀性: 在目標範圍內
```

---

**Persona Template Skill v1.0.0**
**發布日期**: 2025-11-26
