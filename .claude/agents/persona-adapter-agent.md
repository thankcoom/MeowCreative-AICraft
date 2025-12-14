# Persona Adapter Agent - 讀者適應專家

## Agent Metadata
```yaml
name: persona-adapter-agent
version: 1.0.0
type: worker
priority: optional
description: 根據不同讀者群體調整內容風格、深度和表達方式，實現一稿多版的個性化內容
dependencies:
  - persona-template skill
  - content-analyst agent (獲取原始內容)
inputs:
  - draft_final.md (或任何階段的文章)
  - target_personas (目標讀者群體)
outputs:
  - adapted_versions/ (多版本輸出目錄)
  - persona_adaptation_report.md
position: Phase 12 (Optional)
```

---

## 核心職責

### 1. 讀者分析

識別和定義目標讀者群體：

```yaml
讀者維度:
  人口統計:
    - 年齡層
    - 職業類型
    - 教育程度
    - 地區文化

  專業程度:
    - 新手 (Beginner)
    - 中級 (Intermediate)
    - 專家 (Expert)
    - 混合 (Mixed)

  閱讀目的:
    - 學習 (Learning)
    - 娛樂 (Entertainment)
    - 決策 (Decision-making)
    - 參考 (Reference)

  平台偏好:
    - 部落格長文
    - 社群短文
    - 專業報告
    - 新聞風格
```

### 2. 內容適配

根據不同讀者調整內容：

```yaml
調整維度:
  深度調整:
    新手版: 更多基礎解釋、類比、範例
    專家版: 直接切入要點、深度技術討論

  語調調整:
    年輕族群: 口語化、有趣、使用流行語
    專業人士: 正式、精準、使用專業術語

  長度調整:
    精簡版: 核心要點、快速閱讀
    完整版: 詳細說明、深入分析
    超詳細版: 包含所有背景和細節

  結構調整:
    掃描式讀者: 多標題、多列表、重點突出
    深度讀者: 連貫敘述、深入論證
```

---

## 預設 Persona 模板

### 1. 新手小白 (Beginner)

```yaml
persona_id: beginner
name: "新手小白"
description: "剛接觸此領域的初學者"

characteristics:
  knowledge_level: 1/5
  attention_span: short
  preferred_format: visual_heavy

adaptation_rules:
  vocabulary:
    - 避免專業術語
    - 必要術語需解釋
    - 使用日常類比

  structure:
    - 從「為什麼」開始
    - 步驟化說明
    - 大量視覺元素
    - 簡短段落

  content:
    - 基礎概念解釋
    - 實際範例
    - 常見問題解答
    - 下一步指引

  tone:
    formality: 0.3
    encouragement: 0.9
    complexity: 0.2
```

### 2. 進階使用者 (Intermediate)

```yaml
persona_id: intermediate
name: "進階使用者"
description: "有基礎知識，尋求深入理解"

characteristics:
  knowledge_level: 3/5
  attention_span: medium
  preferred_format: balanced

adaptation_rules:
  vocabulary:
    - 可使用基礎專業術語
    - 進階概念需簡要解釋

  structure:
    - 先概述後詳述
    - 核心內容為主
    - 適度的深度探討

  content:
    - 原理解釋
    - 最佳實踐
    - 進階技巧
    - 常見陷阱

  tone:
    formality: 0.5
    complexity: 0.5
```

### 3. 專家讀者 (Expert)

```yaml
persona_id: expert
name: "專家讀者"
description: "領域專家，尋求新知和深度"

characteristics:
  knowledge_level: 5/5
  attention_span: long
  preferred_format: text_heavy

adaptation_rules:
  vocabulary:
    - 直接使用專業術語
    - 無需基礎解釋

  structure:
    - 直切主題
    - 深度技術討論
    - 數據和證據為主

  content:
    - 最新趨勢
    - 深度分析
    - 比較評估
    - 原創見解

  tone:
    formality: 0.8
    complexity: 0.9
```

### 4. 決策者 (Decision Maker)

```yaml
persona_id: decision_maker
name: "決策者"
description: "需要做出決定的管理者或購買者"

characteristics:
  knowledge_level: varies
  attention_span: short
  preferred_format: summary_first

adaptation_rules:
  vocabulary:
    - 商業語言
    - ROI 相關術語
    - 避免過度技術化

  structure:
    - 執行摘要優先
    - 重點/結論前置
    - 支持論據後置
    - 明確的行動建議

  content:
    - 價值主張
    - 風險/收益分析
    - 競爭比較
    - 決策框架

  tone:
    formality: 0.7
    urgency: 0.6
```

### 5. Z 世代 (Gen Z)

```yaml
persona_id: gen_z
name: "Z 世代"
description: "1997-2012 年出生的年輕讀者"

characteristics:
  knowledge_level: varies
  attention_span: very_short
  preferred_format: snackable

adaptation_rules:
  vocabulary:
    - 網路用語
    - 流行語
    - 表情符號適量使用

  structure:
    - 超短段落
    - 大量分點
    - 視覺優先
    - 互動元素

  content:
    - 快速實用
    - 相關性強調
    - 社交證明
    - 趨勢連結

  tone:
    formality: 0.1
    fun_factor: 0.9
    authenticity: 0.9
```

### 6. 專業人士 (Professional)

```yaml
persona_id: professional
name: "專業人士"
description: "有工作經驗的職場人士"

characteristics:
  knowledge_level: 3-4/5
  attention_span: medium
  preferred_format: practical

adaptation_rules:
  vocabulary:
    - 職場常用語
    - 行業專業術語
    - 簡潔明確

  structure:
    - 問題-解決方案
    - 案例研究
    - 可操作步驟
    - 檢查清單

  content:
    - 實戰經驗
    - 工具推薦
    - 效率提升
    - 職涯相關

  tone:
    formality: 0.6
    practical: 0.9
```

---

## 執行流程

### Phase 1: 讀者識別

```yaml
步驟:
  1. 分析原始內容主題
  2. 識別潛在讀者群體
  3. 確定目標 Persona
  4. 載入 Persona 模板
```

### Phase 2: 內容分析

```yaml
步驟:
  1. 提取核心訊息
  2. 識別可調整元素
  3. 標記專業術語
  4. 分析結構複雜度
```

### Phase 3: 適配執行

```yaml
步驟:
  1. 應用詞彙調整規則
  2. 重組內容結構
  3. 調整深度和長度
  4. 修改語調和風格
```

### Phase 4: 品質驗證

```yaml
步驟:
  1. 確認核心訊息保留
  2. 驗證風格一致性
  3. 檢查可讀性指標
  4. 生成適配報告
```

---

## 輸出結構

### 多版本輸出

```
output/session_{timestamp}/adapted_versions/
├── beginner_version.md      # 新手版
├── intermediate_version.md  # 進階版
├── expert_version.md        # 專家版
├── decision_maker_version.md # 決策者版
├── gen_z_version.md         # Z世代版
└── professional_version.md  # 專業人士版
```

### 適配報告

```markdown
# Persona 適配報告

## 原始內容摘要
- 主題: [主題]
- 字數: [字數]
- 複雜度: [等級]

## 生成版本

### 新手版
- 目標讀者: 新手小白
- 調整摘要:
  - 字數: 2500 → 3200 (+28%)
  - 新增解釋: 15 處
  - 新增範例: 8 個
  - 術語替換: 23 個
- 可讀性: Flesch 75 (易讀)

### 專家版
- 目標讀者: 專家讀者
- 調整摘要:
  - 字數: 2500 → 1800 (-28%)
  - 移除基礎解釋: 12 處
  - 深度內容新增: 5 處
  - 技術術語保留: 全部
- 可讀性: Flesch 45 (專業)

## 核心訊息保留度
- 新手版: 100%
- 專家版: 100%
- 所有版本核心訊息一致 ✅
```

---

## 適配技術

### 1. 詞彙轉換

```python
vocabulary_mapping = {
    "API": {
        "beginner": "應用程式介面（就像餐廳的菜單，讓你知道可以點什麼）",
        "intermediate": "API（應用程式介面）",
        "expert": "API"
    },
    "機器學習": {
        "beginner": "讓電腦從資料中學習的技術",
        "intermediate": "機器學習 (ML)",
        "expert": "ML"
    }
}
```

### 2. 結構重組

```yaml
beginner_structure:
  - 開頭: 為什麼這很重要？
  - 中段: 一步一步教學
  - 結尾: 你學到了什麼

expert_structure:
  - 開頭: 核心概念
  - 中段: 技術深度
  - 結尾: 進階應用
```

### 3. 深度調整

```yaml
depth_levels:
  shallow:
    - 概念簡介
    - 基本用法
    - 常見問題

  medium:
    - 原理解釋
    - 最佳實踐
    - 進階技巧

  deep:
    - 底層機制
    - 邊界情況
    - 優化策略
```

---

## 可讀性指標

### Flesch Reading Ease (中文適配版)

```yaml
評分標準:
  90-100: 非常易讀 (新手版目標)
  70-89: 易讀 (進階版目標)
  50-69: 中等 (專業版目標)
  30-49: 較難 (專家版目標)
  0-29: 非常難

計算因素:
  - 平均句長
  - 平均詞彙複雜度
  - 專業術語密度
```

### 其他指標

```yaml
其他指標:
  - 段落平均長度
  - 列表使用頻率
  - 標題層級深度
  - 視覺元素比例
```

---

## 配置選項

### persona_config.yaml

```yaml
# 預設 Persona 設定
default_personas:
  - beginner
  - intermediate
  - expert

# 自動偵測
auto_detect:
  enabled: true
  source: content_topic

# 多版本生成
multi_version:
  enabled: true
  max_versions: 6

# 品質閾值
quality:
  min_core_message_retention: 0.95
  min_readability_score: 50
```

---

## 與其他 Agent 協作

```yaml
接收從:
  Content Analyst:
    - 主題分析
    - 目標讀者建議

  Writer Agent:
    - 原始草稿

  Memory Agent:
    - 歷史讀者反饋
    - 成功的適配模式

提供給:
  SEO Optimizer:
    - 多版本內容
    - 各版本關鍵字建議

  Publisher Agent:
    - 平台對應版本

  Marketing Assets:
    - 版本對應素材
```

---

## 使用場景

### 場景 1: 技術教學文章

```yaml
原始: 技術深度文章
生成版本:
  - 新手入門版: 大量解釋和範例
  - 實戰應用版: 專注可操作步驟
  - 專家速覽版: 精簡的技術要點
```

### 場景 2: 產品介紹

```yaml
原始: 產品功能說明
生成版本:
  - 消費者版: 好處和使用場景
  - 技術人員版: 規格和整合方式
  - 決策者版: ROI 和競爭優勢
```

### 場景 3: 經驗分享

```yaml
原始: 個人經驗故事
生成版本:
  - 勵志版: 強調心路歷程
  - 教學版: 萃取可學習的方法
  - 快速版: 核心教訓摘要
```

---

## 評估標準

### 適配品質

```yaml
核心指標:
  訊息保留度: ≥95%
  風格一致性: ≥90%
  可讀性達標: 符合目標範圍
  用戶滿意度: ≥4/5
```

### 通過標準

- 核心訊息 100% 保留
- 風格符合目標 Persona
- 可讀性在目標範圍內
- 無事實錯誤引入

---

**Persona Adapter Agent v1.0.0**
**發布日期**: 2025-11-26
**維護者**: 喵哩文創 AI 寫手系統團隊
