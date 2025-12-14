# WordPress 部落格 AI 寫手系統 v2.6.0

這是一個使用 Claude Code 打造的全自動部落格文章創作與發布系統，採用 Multi-Agent 協作架構和 MCP 整合。v2.6.0 **"Search Everywhere"** 新增完整的 AI 搜尋優化支援，包含 LLMO、GEO、AEO、VSO、CRO 等 2025 年最新優化策略。

## 🎯 專案目標

自動化高品質部落格文章的創作流程，從內容分析、市場研究、風格學習到 SEO 優化、多平台發布和數據分析，確保每篇文章都具有真實性、可讀性和搜尋引擎友好性。

**版本演進**:
- v2.0.0: MCP 整合 + 自動化發布
- v2.1.0: 品質強化 (Fact Checker + Humanizer)
- v2.2.0: 說服力提升 (Persuasion + Storyteller)
- v2.3.0: 智慧進化 (Memory + Persona Adapter)
- v2.4.0: 效能優化 (Performance + Quality Predictor)
- v2.5.0: Reality Check (真實化 + 工程化 + Wisdom Database)
- **v2.6.0: Search Everywhere (LLMO + GEO + AEO + VSO + CRO)** 🆕

---

## 🏗️ 系統架構 v2.6.0

### Multi-Agent 系統（Orchestrator-Worker Pattern）

```text
Blog Manager v2.5.0 (協調者) - Reality Check
├── Phase 13: Performance Optimizer (效能優化) [Background] ← 真正啟用
├── Phase 11: Memory Agent (跨 Session 學習) [Background] ← 自動學習
├── Phase 0: Experience Collector (收集真實經驗)
├── Phase 1: Content Analyst (分析原文)
├── Phase 2a: Research Agent (市場研究)
├── Phase 2b: Style Matcher (風格學習)
├── Phase 3: Writer Agent (撰寫文章)
├── Phase 3.4: Quality Predictor (品質預測) 🆕 v2.4.0
├── Phase 3.6: Fact Checker Agent (事實驗證) v2.1.0
├── Phase 3.7: Humanizer Agent (內容人類化) v2.1.0
├── Phase 3.8: Persuasion Agent (說服力強化) v2.2.0
├── Phase 3.9: Storyteller Agent (故事敘事) v2.2.0
├── Phase 3.5: Editor Agent (品質審查)
├── Phase 4: SEO Optimizer (SEO 優化)
├── Phase 12: Persona Adapter Agent (多讀者適配) v2.3.0
├── Phase 5: WordPress Publisher (WordPress 發布)
├── Phase 6: Marketing Assets (行銷素材)
├── Phase 7: Analytics Reporter (數據分析)
├── Phase 8: Multi-Platform Publishing (多平台發布)
├── Phase 9: A/B Testing (A/B 測試)
└── Phase 10: Data Dashboard (數據儀表板)
```

### 優先級系統

- ⭐ **Critical**: 必須完成，失敗會停止流程
- ⚠️ **Important**: 建議完成，失敗僅警告
- ⭕ **Optional**: 可選功能，可跳過

---

## 🚀 常用工作流程

### 標準流程：文章改寫 (完整 v2.4.0 流程)

```text
輸入：請將這篇文章改寫並執行完整 v2.4.0 流程：https://example.com/article

自動執行順序：
0. Phase 13: Performance Optimizer 背景啟動 🆕 v2.4.0
1. Phase 11: Memory Agent 背景啟動，載入學習數據
2. Phase 0: 收集用戶真實經驗 (Critical)
3. Phase 1: 分析原文結構 (Critical)
4. Phase 2a/2b: 市場研究和風格學習 (並行)
5. Phase 3: 撰寫文章初稿 (Critical)
6. Phase 3.4: 品質預測和風險評估 🆕 v2.4.0
7. Phase 3.6-3.9: 根據預測結果動態調整執行
8. Phase 3.5: 品質審查和評分 (Critical)
9. Phase 4: SEO 優化 (Important)
10. Phase 12: 多讀者版本生成 (Optional)
11. Phase 5-10: 發布和行銷 (Optional)
12. Phase 13: 生成效能報告 🆕 v2.4.0
```

### 效能優先流程 🆕 v2.4.0

```text
輸入：請快速改寫這篇文章，優先考慮執行效率

執行調整：
- Phase 13: Performance Optimizer 監控效能 ✅
- Phase 2a/2b 並行執行 ✅
- Phase 3.4: 根據品質預測跳過低優先級 Phase ✅
- 目標: 執行時間 < 10 分鐘
```

### 品質優先流程 🆕 v2.4.0

```text
輸入：請改寫這篇文章，確保最高品質，不計時間

執行調整：
- 執行所有 Phase (不跳過) ✅
- Phase 3.4 作為參考，不作為跳過依據 ✅
- 目標: 綜合分數 ≥ 90/100
```

### 多讀者版本生成流程 v2.3.0

```text
輸入：請將這篇文章生成新手、進階和專家三個版本

重點執行：
- Phase 12: Persona Adapter Agent ✅
- 新手版: 大量解釋和範例
- 進階版: 去除基礎，強調最佳實踐
- 專家版: 直切主題，深度技術
```

### 利用學習洞察優化流程 v2.3.0

```text
輸入：請根據過去的寫作偏好，快速改寫這篇文章

重點執行：
- Phase 11: Memory Agent ✅ 載入用戶偏好
- 自動應用成功的開頭模式
- 符合用戶偏好的語調和結構
```

### 說服力優化流程

```text
輸入：請改寫這篇文章，強化說服力，目標是提高轉換率

重點執行：
- Phase 3.8: Persuasion Agent ✅ (AIDA/PAS/4Cs 框架)
- 心理觸發設計 ✅
- CTA 優化 ✅
```

### 故事化內容流程

```text
輸入：這是一篇個人經驗分享，請用故事的方式改寫

重點執行：
- Phase 3.9: Storyteller Agent ✅ (Hero's Journey)
- 情感曲線設計 ✅
- 轉折點設計 ✅
```

---

## 📁 重要目錄結構 v2.4.0

```text
.claude/
├── agents/                    # 17 個 AI Agents 定義
│   ├── blog-manager-v2.4.0.md # v2.4.0 主協調 Agent 🆕
│   ├── performance-optimizer-agent.md # 效能優化 Agent 🆕 v2.4.0
│   ├── quality-predictor-agent.md # 品質預測 Agent 🆕 v2.4.0
│   ├── memory-agent.md        # 跨 Session 學習 Agent v2.3.0
│   ├── persona-adapter-agent.md # 多讀者適配 Agent v2.3.0
│   ├── persuasion-agent.md    # 說服力寫作 Agent v2.2.0
│   ├── storyteller-agent.md   # 故事敘事 Agent v2.2.0
│   ├── fact-checker-agent.md  # 事實驗證 Agent v2.1.0
│   ├── humanizer-agent.md     # 內容人類化 Agent v2.1.0
│   ├── experience-collector.md
│   ├── content-analyst.md
│   ├── research-agent.md
│   ├── style-matcher.md
│   ├── writer-agent.md
│   ├── editor-agent.md
│   ├── seo-optimizer.md
│   └── publisher-agent.md
│
├── config/                    # 配置檔案
│   ├── writing-style.yaml    # 寫作風格設定
│   ├── wordpress-credentials.yaml
│   ├── workflow-validation.yaml
│   ├── market-research.yaml
│   ├── reference-authors-db.yaml
│   ├── eeat-config.yaml      # E-E-A-T 評估標準
│   ├── llmo-config.yaml      # LLMO 大語言模型優化 🆕 v2.6.0
│   ├── aiso-config.yaml      # AISO 跨 AI 平台策略 🆕 v2.6.0
│   ├── vso-config.yaml       # VSO 語音搜尋優化 🆕 v2.6.0
│   └── cro-config.yaml       # CRO 轉換率優化 🆕 v2.6.0
│
├── memory/                    # 學習數據庫 v2.3.0
│   ├── user_preferences/     # 用戶偏好
│   ├── patterns/             # 成功/失敗模式
│   ├── knowledge/            # 術語和規則
│   └── history/              # 歷史記錄
│
├── performance/               # 效能數據 🆕 v2.4.0
│   ├── sessions.jsonl        # Session 效能記錄
│   ├── benchmarks.json       # 基準效能指標
│   ├── trends.json           # 趨勢分析數據
│   └── dashboard/            # 效能儀表板 🆕 v2.5.0
│
├── wisdom/                    # 寫作智慧庫 🆕 v2.5.0
│   ├── masters/              # 大師原則
│   │   ├── schwartz.yaml     # Eugene Schwartz 5階段認知
│   │   ├── cialdini.yaml     # Cialdini 6大說服原理
│   │   ├── ogilvy.yaml       # David Ogilvy 5大原則
│   │   └── patel.yaml        # Neil Patel 2024-2025洞察
│   ├── frameworks/           # 核心框架
│   │   ├── awareness_stages.yaml       # 讀者認知階段
│   │   ├── success_framework.yaml      # SUCCESs 記憶框架
│   │   └── search_optimization_matrix.yaml # 搜尋優化矩陣 🆕 v2.6.0
│   ├── psychology/           # 心理學原理
│   ├── examples/             # 頂級範例庫
│   └── anti-patterns/        # 反模式庫
│       └── logic_fallacies.yaml # 邏輯謬誤檢測
│
├── logs/                      # 日誌目錄 🆕 v2.5.0
│   ├── skills.log            # Skill 執行日誌
│   └── errors.log            # 錯誤日誌
│
└── skills/                    # Skills 和工具
    ├── performance-monitor/   # 效能監控 Skill 🆕 v2.4.0
    ├── quality-prediction/    # 品質預測 Skill 🆕 v2.4.0
    ├── learning-database/     # 學習數據庫 Skill v2.3.0
    ├── persona-template/      # 讀者模板 Skill v2.3.0
    ├── persuasion-analyzer/   # 說服力分析 Skill v2.2.0
    ├── story-arc-generator/   # 故事弧線生成 Skill v2.2.0
    ├── fact-verification/     # 事實驗證 Skill v2.1.0
    ├── ai-detection/          # AI 偵測 Skill v2.1.0
    ├── wordpress-publisher/   # WordPress 發布 Skill
    ├── seo-analyzer/          # SEO 分析 Skill
    ├── analytics-reporter/    # Analytics 報告 Skill
    ├── content-repurposer/    # 內容改寫 Skill
    ├── marketing-assets/      # 行銷素材 Skill
    ├── brand-guidelines/      # Anthropic 官方品牌風格 Skill
    ├── miaoli-brand/          # 喵哩文創客製化品牌 Skill
    ├── workflow-validator/    # 工作流程驗證
    ├── web-scraper/           # 網頁抓取
    ├── image-generator/       # 圖片生成
    └── research-cache/        # 研究快取

output/                        # 輸出目錄
└── session_YYYYMMDD_HHMMSS/
    ├── workflow_progress.json     # 即時進度
    ├── validation_report.json     # 驗證報告
    ├── experience_profile.md      # Phase 0
    ├── analysis_report.md         # Phase 1
    ├── research_report.md         # Phase 2a
    ├── style_guide.md             # Phase 2b
    ├── draft_final.md             # Phase 3
    ├── fact_check_report.md       # Phase 3.6
    ├── humanized_draft.md         # Phase 3.7
    ├── humanization_report.md     # Phase 3.7
    ├── persuasive_draft.md        # Phase 3.8
    ├── persuasion_report.md       # Phase 3.8
    ├── story_enhanced_draft.md    # Phase 3.9
    ├── story_arc_report.md        # Phase 3.9
    ├── editor_review.md           # Phase 3.5
    ├── final_article.md           # Phase 4
    ├── seo_report.md              # Phase 4
    ├── adapted_versions/          # Phase 12 🆕 v2.3.0
    │   ├── beginner_version.md
    │   ├── intermediate_version.md
    │   ├── expert_version.md
    │   └── decision_maker_version.md
    ├── persona_adaptation_report.md # Phase 12 🆕 v2.3.0
    ├── publish_report.md          # Phase 5
    ├── marketing_assets/          # Phase 6
    ├── analytics_report/          # Phase 7
    └── dashboard/                 # Phase 10
```

---

## 🛠️ 常用命令

### 系統驗證

```bash
# 測試系統配置
python3 test_setup.py

# 檢查最新 session 是否完整
./scripts/check_workflow.sh

# 驗證特定 session
python .claude/skills/workflow-validator/workflow_validator.py validate output/session_20251111_123456
```

### v2.4.0 新增命令 🆕

```bash
# 查看效能狀態
python3 .claude/skills/performance-monitor/monitor.py status

# 分析特定 session 效能
python3 .claude/skills/performance-monitor/monitor.py analyze \
    --session output/session_20251126_120000

# 生成效能週報
python3 .claude/skills/performance-monitor/monitor.py report \
    --type weekly \
    --output performance_weekly.md

# 獲取優化建議
python3 .claude/skills/performance-monitor/monitor.py suggest \
    --session output/session_20251126_120000

# 預測品質分數
python3 .claude/skills/quality-prediction/predict.py score \
    draft_final.md

# 評估風險
python3 .claude/skills/quality-prediction/predict.py risk \
    draft_final.md \
    --output risk_assessment.md

# 獲取改進建議
python3 .claude/skills/quality-prediction/predict.py suggest \
    draft_final.md \
    --target-score 90

# 完整預測報告
python3 .claude/skills/quality-prediction/predict.py full \
    draft_final.md \
    --output quality_report.md
```

### v2.3.0 命令

```bash
# 初始化學習數據庫
python3 .claude/skills/learning-database/manage.py init

# 查看學習數據庫狀態
python3 .claude/skills/learning-database/manage.py status

# 添加成功模式
python3 .claude/skills/learning-database/manage.py add-pattern \
    --type success \
    --category opening \
    --pattern "問句開頭" \
    --example "你是否也曾經..."

# 查詢高效模式
python3 .claude/skills/learning-database/manage.py query-patterns \
    --category opening \
    --min-success-rate 0.7

# 記錄 session 結果
python3 .claude/skills/learning-database/manage.py log-session \
    --session-dir output/session_20251126_120000 \
    --score 85 \
    --feedback "用戶滿意"

# 生成學習報告
python3 .claude/skills/learning-database/manage.py generate-report \
    --type weekly \
    --output learning_report.md

# 列出所有 Persona 模板
python3 .claude/skills/persona-template/adapt.py list

# 查看特定 Persona 詳情
python3 .claude/skills/persona-template/adapt.py show beginner

# 適配內容到特定讀者
python3 .claude/skills/persona-template/adapt.py adapt \
    draft_final.md \
    --persona beginner \
    --output beginner_version.md

# 生成多版本 (一稿多版)
python3 .claude/skills/persona-template/adapt.py multi-adapt \
    draft_final.md \
    --personas beginner,intermediate,expert \
    --output-dir adapted_versions/

# 創建自定義 Persona
python3 .claude/skills/persona-template/adapt.py create \
    --id startup_founder \
    --name "創業家" \
    --config custom_persona.yaml

# 驗證適配品質
python3 .claude/skills/persona-template/adapt.py verify \
    original.md \
    adapted.md \
    --persona beginner
```

### v2.2.0 命令

```bash
# 分析文章說服力
python3 .claude/skills/persuasion-analyzer/analyze.py \
    input_article.md \
    --output persuasion_report.md

# 分析故事結構
python3 .claude/skills/story-arc-generator/generate.py \
    input_article.md \
    --mode analyze \
    --output story_analysis.md

# 生成故事弧線建議
python3 .claude/skills/story-arc-generator/generate.py \
    input_article.md \
    --mode generate \
    --structure hero_journey \
    --output story_arc.md

# 生成情感曲線設計
python3 .claude/skills/story-arc-generator/generate.py \
    input_article.md \
    --mode emotion \
    --pattern man_in_hole \
    --output emotion_curve.md
```

### v2.1.0 命令

```bash
# 事實驗證
python3 .claude/skills/fact-verification/verify.py \
    draft_final.md \
    --experience experience_profile.md \
    --output fact_check_report.md

# AI 偵測
python3 .claude/skills/ai-detection/detect.py \
    draft_final.md \
    --output ai_detection_report.md
```

---

## 📋 Agent 執行原則

### 調用 Agent 時的最佳實踐

1. **並行執行獨立任務**

   ```text
   ✅ 正確：如果 Phase 2a 和 Phase 2b 互不依賴，在單一訊息中同時調用兩個 Task 工具
   ❌ 錯誤：順序執行獨立的 Phase
   ```

2. **使用 Extended Thinking**

   ```text
   對於複雜任務（如市場研究、文章規劃），使用 "think hard" 啟動擴展思考模式
   ```

3. **工具調用後反思**

   ```text
   在每個重要 Phase 完成後，評估結果質量並確定最佳下一步
   ```

4. **狀態更新及時性**

   ```text
   每個 Phase 開始時：更新為 in_progress
   每個 Phase 完成時：立即更新為 completed
   每個 Phase 失敗時：更新為 failed 並記錄原因
   ```

---

## ✍️ 寫作風格規範

### 核心原則

1. **真實性第一**
   - 絕對不可虛構個人經驗、數據或案例
   - 必須先執行 Experience Collector 收集真實經驗
   - 引用他人經驗時必須明確標註來源

2. **語調一致性**
   - 對話式、親和但專業
   - 使用「我」「你」而非「本文」「讀者」
   - 避免過度正式或學術化

3. **結構清晰**
   - 使用明確的標題階層（H1 → H2 → H3）
   - 每段 3-5 句話
   - 每句平均 15-20 字

4. **SEO 友好**
   - 主要關鍵字出現在標題、首段、小標題
   - 關鍵字密度 1-2%
   - Meta description 150-160 字

---

## 🆕 v2.4.0 新功能

### 1. Performance Optimizer Agent (效能優化)

**智慧效能監控系統**:

**監控項目**:
- 執行時間追蹤 (每個 Phase)
- Token 使用量分析
- API 調用統計
- 快取命中率

**效能評級**:
| 評級 | 條件 |
|------|------|
| A+ | < 8 分鐘, 快取 > 85% |
| A | < 10 分鐘, 快取 > 75% |
| B | < 15 分鐘, 快取 > 65% |
| C | < 20 分鐘, 快取 > 50% |

**優化建議**:
- 並行執行機會識別
- 智慧 Phase 跳過建議
- 快取策略優化
- 資源使用優化

### 2. Quality Predictor Agent (品質預測)

**早期品質預測系統**:

**預測維度**:
| 維度 | 權重 | 說明 |
|------|------|------|
| E-E-A-T | 30% | 經驗、專業、權威、可信 |
| SEO | 25% | 關鍵字、結構、Meta |
| 說服力 | 25% | AIDA、觸發詞、CTA |
| 參與度 | 20% | 開頭、互動、連結 |

**執行路徑決策**:
- **高品質路徑** (≥85): 可跳過部分 Phase，節省 ~2 分鐘
- **標準路徑** (70-84): 完整執行，根據風險加強
- **改進路徑** (<70): 需要額外強化或返回修改

**風險評估**:
- 事實錯誤風險
- AI 偵測風險
- SEO 風險
- 參與度風險

### 3. 新增 2 個 Skills

1. **performance-monitor** - 效能監控和報告工具
   - 執行時間追蹤
   - 資源使用分析
   - 效能報告生成
   - 優化建議

2. **quality-prediction** - 品質預測和風險評估工具
   - 多維度分數預測
   - 風險識別
   - 改進建議生成
   - 執行路徑決策

### 4. 新增 2 個 Phases

**Phase 13**: Performance Optimizer - 效能優化 (Background)
- 在 Session 開始時背景啟動
- 持續監控執行效能
- Session 結束時生成報告

**Phase 3.4**: Quality Predictor - 品質預測 (Important)
- 在 Writer Agent (Phase 3) 後執行
- 預測最終品質分數
- 決定後續執行路徑

---

## 🆕 v2.3.0 新功能

### 1. Memory Agent (跨 Session 學習)

**智慧記憶系統**:

**記憶類型**:
- **短期記憶**: 當前 Session 上下文和決策
- **長期記憶**: 用戶偏好、成功模式、知識庫
- **工作記憶**: 執行中的任務狀態

**學習機制**:
- **模式識別**: 從成功案例中學習有效模式
- **反饋學習**: 根據用戶修改調整策略
- **知識整合**: 建立和更新術語表與規則

**存儲結構**:
```text
.claude/memory/
├── user_preferences/   # 風格、內容、工作流程偏好
├── patterns/           # 成功和失敗模式
├── knowledge/          # 術語表、禁用詞、規則
├── history/            # Session 歷史和效能
└── cache/              # 最近使用的模式快取
```

**運作方式**:
- Phase 11 在背景持續運行
- Session 開始時載入相關學習數據
- Session 過程中即時學習用戶修改
- Session 結束時存儲新發現

### 2. Persona Adapter Agent (多讀者適配)

**一稿多版功能**:
一篇文章自動生成多個版本，針對不同讀者群調整

**預設 Persona 模板**:

| Persona | 說明 | 適配重點 |
|---------|------|----------|
| 🌱 beginner | 新手小白 | 大量解釋、類比、範例 |
| 📈 intermediate | 進階使用者 | 跳過基礎、最佳實踐 |
| 🎓 expert | 專家讀者 | 深度技術、邊緣案例 |
| 💼 decision_maker | 決策者 | 摘要優先、ROI 分析 |
| ⚡ gen_z | Z 世代 | 短段落、互動、趨勢 |
| 👔 professional | 專業人士 | 實用導向、案例、模板 |

**適配維度**:
- **詞彙**: 複雜度、術語解釋、類比使用
- **結構**: 段落長度、標題密度、列表使用
- **內容**: 深度、範例頻率、實用性
- **語調**: 正式度、親和度、直接度

**品質驗證**:
- 核心訊息保留 ≥ 95%
- 可讀性符合目標 Persona
- 風格一致性 ≥ 90%

### 3. 新增 2 個 Skills

1. **learning-database** - 學習數據庫管理工具
   - 模式存儲和查詢
   - 偏好管理
   - Session 歷史追蹤
   - 學習報告生成

2. **persona-template** - Persona 模板管理工具
   - 6 個預設模板
   - 自定義 Persona 創建
   - 內容適配引擎
   - 品質驗證功能

### 4. 新增 2 個 Phases

**Phase 11**: Memory Agent - 跨 Session 學習 (Background)
- 在整個 Session 生命週期背景運行
- 自動載入和應用學習洞察

**Phase 12**: Persona Adapter - 多讀者版本生成 (Optional)
- 在 Phase 4 (SEO 優化) 後執行
- 可選擇生成 1-6 個不同版本

---

## 🆕 v2.2.0 新功能

### 1. Persuasion Agent (說服力寫作)

**整合說服力框架**:

**AIDA 框架**:
- Attention (注意): 開頭吸引力
- Interest (興趣): 好處展示
- Desire (慾望): 社會證明和情感連結
- Action (行動): CTA 優化

**PAS 框架**:
- Problem (問題): 痛點明確化
- Agitate (激化): 問題放大
- Solution (解決): 方案呈現

**4Cs 框架**:
- Clear (清楚): 訊息清晰度
- Concise (簡潔): 無冗餘
- Compelling (吸引): 情感連結
- Credible (可信): 證據支持

**心理觸發設計**:
- 稀缺性 (限時、獨家)
- 社會證明 (數據、評價)
- 權威性 (專家、認證)
- 互惠 (免費提供)

**驗證標準**:
- 說服力評分 ≥ 70/100
- CTA 出現 ≥ 2 次
- 心理觸發 ≥ 3 種

### 2. Storyteller Agent (故事敘事)

**故事結構模板**:

**Hero's Journey (英雄之旅)**:
平凡世界 → 冒險召喚 → 試煉 → 獲得寶物 → 歸來
適合：轉型故事、學習歷程

**Three-Act Structure (三幕劇)**:
第一幕 (25%): 設定
第二幕 (50%): 對抗
第三幕 (25%): 解決

**Story Spine (Pixar 故事骨架)**:
從前有... → 每天... → 直到有一天... → 因為這樣... → 直到最後... → 從那之後...

**情感曲線模式**:
- Rags to Riches (鹹魚翻身)
- Man in a Hole (穴中人)
- Cinderella (灰姑娘)

**驗證標準**:
- 敘事強度 ≥ 70/100
- 有明確的開頭、中段、結尾
- 至少包含 1 個轉折點

### 3. 新增 2 個 Skills

1. **persuasion-analyzer** - 說服力分析和評估工具
2. **story-arc-generator** - 故事弧線生成和分析工具

### 4. 新增 2 個 Phases

**Phase 3.8**: Persuasion Agent - 說服力強化 (Important)
**Phase 3.9**: Storyteller Agent - 故事敘事增強 (Optional)

---

## 🆕 v2.1.0 新功能

### 1. Fact Checker Agent (事實驗證)

**防止 LLM 幻覺**:
- 自動識別文章中的事實陳述
- 數據型、聲明型、引用型、技術型分類驗證
- 語義熵分析識別高風險幻覺
- 可信度評分 (0-100)

**驗證標準**:
- 可信度評分 ≥ 70 才能通過
- 高風險項目必須修改
- 所有數據需有來源

### 2. Humanizer Agent (內容人類化)

**消除 AI 特徵**:
- 句式重複率檢測
- 段落長度變異度分析
- 情感詞彙密度評估
- 困惑度和爆發度分析

**人類化處理**:
- 句式變化優化
- 情感注入
- 對話感增強
- 節奏調整

---

## 🧪 測試和驗證

### 品質檢查清單 (v2.3.0)

執行完整工作流程後，必須通過以下檢查：

**Critical 檢查**:
- [ ] Experience Collector 已執行，experience_profile.md 存在
- [ ] 文章字數符合要求（通常 1500-3000 字）
- [ ] Fact Checker 可信度評分 ≥ 70/100
- [ ] Editor Agent 評分 ≥ 85/100
- [ ] 沒有虛構的個人經驗
- [ ] 所有引用都有來源

**Important 檢查**:
- [ ] AI 偵測分數 ≤ 40/100
- [ ] 說服力評分 ≥ 70/100
- [ ] CTA 出現 ≥ 2 次
- [ ] 心理觸發 ≥ 3 種
- [ ] SEO Optimizer 評分 ≥ 80/100
- [ ] **Memory Agent 已載入學習數據** 🆕 v2.3.0
- [ ] **Session 結果已記錄到學習數據庫** 🆕 v2.3.0

**Optional 檢查**:
- [ ] 敘事強度 ≥ 70/100
- [ ] 有明確轉折點
- [ ] 行銷素材已生成
- [ ] **多讀者版本已生成 (如需要)** 🆕 v2.3.0
- [ ] **Persona 適配品質 ≥ 90%** 🆕 v2.3.0

---

## 🔧 故障排除

### 常見問題

#### Q: Memory Agent 沒有載入學習數據？ 🆕 v2.3.0

```text
1. 檢查學習數據庫是否已初始化
   python3 .claude/skills/learning-database/manage.py status

2. 如果未初始化，執行初始化
   python3 .claude/skills/learning-database/manage.py init

3. 確認 .claude/memory/ 目錄結構存在
4. 檢查是否有足夠的歷史數據供學習
```

#### Q: Persona 適配品質不佳？ 🆕 v2.3.0

```text
1. 確認選擇了正確的目標 Persona
2. 驗證原文內容是否足夠完整
3. 檢查適配報告中的品質指標
4. 可以嘗試調整 Persona 參數
5. 使用 verify 命令檢查適配品質：
   python3 .claude/skills/persona-template/adapt.py verify \
       original.md adapted.md --persona beginner
```

#### Q: 如何查看系統學到了什麼？ 🆕 v2.3.0

```text
# 生成週報查看學習洞察
python3 .claude/skills/learning-database/manage.py generate-report \
    --type weekly \
    --output learning_insights.md

# 查詢特定類別的成功模式
python3 .claude/skills/learning-database/manage.py query-patterns \
    --category opening \
    --min-success-rate 0.7
```

#### Q: 說服力評分太低怎麼辦？

```text
1. 檢查 AIDA 框架各階段是否完整
2. 確認是否有足夠的心理觸發
3. 優化 CTA 的位置和措辭
4. 增加社會證明和權威性元素
```

#### Q: 敘事強度不足怎麼辦？ 🆕

```text
1. 選擇適合的故事結構 (Hero's Journey / Three-Act)
2. 設計明確的轉折點
3. 加入情感曲線的高低起伏
4. 增加衝突和解決的對比
```

#### Q: MCP 連接失敗怎麼辦？

系統會自動降級：
- Phase 7: 使用模擬數據並標註 "⚠️ 非真實數據"
- Phase 8: 保存內容到本地，提供手動發布說明

**解決方案**:
1. 檢查 MCP 配置: `~/.config/claude-code/mcp.json`
2. 驗證 API 憑證是否正確
3. 參考 `docs/MCP_CONFIGURATION_GUIDE.md` 重新配置

---

## 📊 系統版本

**當前版本**: v2.4.0
**最後更新**: 2025-11-26

### 主要版本歷史

- **v2.4.0** (2025-11-26): 效能優化版 - Performance Optimizer + Quality Predictor 🆕
- **v2.3.0** (2025-11-26): 智慧進化版 - Memory Agent + Persona Adapter
- **v2.2.0** (2025-11-26): 說服力提升版 - Persuasion + Storyteller Agent
- **v2.1.0** (2025-11-25): 品質強化版 - Fact Checker + Humanizer Agent
- **v2.0.0** (2025-11-11): MCP 整合 + 5 個 Skills + 10 Phases
- **v1.8.0** (2025-11-11): Skills 整合測試
- **v1.7.0** (2025-11-10): 支援腳本開發
- **v1.6.0** (2025-11-10): Skills 開發
- **v1.4.0** (2025-10-27): 工作流程驗證系統
- **v1.3.0** (2025-10-26): Experience Collector + 品質審查
- **v1.2.0** (2025-10-24): 動態參考作者 + 研究快取
- **v1.1.0** (2025-10-24): SEO 搜尋意圖分析
- **v1.0.0** (2025-10-22): 初始版本

---

## 💡 使用提示

### 給 Claude 的指示

當用戶請求撰寫或改寫文章時：

1. **自動啟動 Blog Manager Agent**（使用 Task 工具）
2. **Phase 11 Memory Agent 自動背景運行** 🆕 v2.3.0
3. **檢查用戶需求**:
   - 如提到 "多版本"、"不同讀者" → 使用 Phase 12 🆕 v2.3.0
   - 如提到 "學習"、"偏好" → 確保 Memory Agent 載入數據 🆕 v2.3.0
   - 如提到 "說服力"、"轉換率" → 強調 Phase 3.8
   - 如提到 "故事"、"敘事" → 強調 Phase 3.9
   - 如提到 "完整流程" → 使用 v2.3.0 完整功能
   - 如提到 "快速" → 跳過 Optional 功能
4. **按照 Phase 順序執行**，不要跳過 Critical 步驟
5. **即時更新 workflow_progress.json**
6. **在關鍵決策點使用 Extended Thinking**
7. **並行執行獨立的 Phase**
8. **每個 Phase 完成後驗證輸出**
9. **Session 結束時記錄學習結果** 🆕 v2.3.0
10. **最終執行完整性驗證**

### 給開發者的提示

- 使用 `./scripts/check_workflow.sh` 快速檢查最新 session
- 定期清理 research cache 避免過期資料
- 調整 `.claude/config/workflow-validation.yaml` 自訂驗證規則
- 查看 `output/session_*/validation_report.json` 了解系統執行品質
- **使用 learning-database 查看系統學習洞察** 🆕 v2.3.0
- **使用 persona-template 生成多讀者版本** 🆕 v2.3.0
- 使用 persuasion-analyzer 優化文章說服力
- 使用 story-arc-generator 設計故事結構

---

## 📚 參考資料

### 官方文件

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)
- [Notion API](https://developers.notion.com/)

### 專案文件

- `README.md` - 系統概述
- `CLAUDE.md` - 系統使用指南（本文件）
- `RELEASE_NOTES_v2.5.0.md` - v2.5.0 發布說明 🆕
- `RELEASE_NOTES_v2.4.0.md` - v2.4.0 發布說明
- `RELEASE_NOTES_v2.3.0.md` - v2.3.0 發布說明
- `RELEASE_NOTES_v2.2.0.md` - v2.2.0 發布說明
- `RELEASE_NOTES_v2.1.0.md` - v2.1.0 發布說明
- `RELEASE_NOTES_v2.0.0.md` - v2.0.0 發布說明
- `docs/MCP_CONFIGURATION_GUIDE.md` - MCP Servers 詳細配置指南
- `docs/learning/` - 學習資源
- `docs/versions/` - 版本歷史

---

## 🆕 v2.6.0 新功能 - Search Everywhere

### 完整搜尋優化支援

v2.6.0 新增 2025 年最新的 AI 搜尋優化策略，讓內容在所有搜尋場景都有能見度。

### 1. 新增優化配置檔案

| 配置檔案 | 說明 | 核心功能 |
|---------|------|---------|
| `llmo-config.yaml` | 大語言模型優化 | 被 ChatGPT/Perplexity 引用 |
| `aiso-config.yaml` | 跨 AI 平台策略 | 統一優化框架 |
| `vso-config.yaml` | 語音搜尋優化 | 被 Siri/Alexa 選為回答 |
| `cro-config.yaml` | 轉換率優化 | 提升訪客轉換 |

### 2. 搜尋優化類型總覽

| 類型 | 目標 | 2025 權重 |
|------|------|----------|
| **SEO** | Google/Bing 排名 | 20% |
| **GEO** | AI 引用 (ChatGPT, Perplexity) | 20% |
| **LLMO** | LLM 選為回答素材 | 20% |
| **AEO** | Featured Snippet | 15% |
| **E-E-A-T** | 內容可信度 | 15% |
| **VSO** | 語音助理回答 | 5% |
| **CRO** | 轉換率 | 5% |

### 3. LLMO 核心策略

**讓內容被 AI 引用的關鍵**:
- 結構化內容 (清晰標題、列表、表格)
- 明確術語定義
- 數據和權威來源引用
- 問答格式 (FAQ)
- 獨特觀點和第一手經驗
- 完整實體覆蓋 (人物、方法論)

**2025 關鍵數據**:
- AI 搜尋流量成長 1,200%
- AI 用戶轉換率是傳統的 4.4 倍
- 82.5% AI 引用來自深層頁面

### 4. VSO 核心策略

**語音搜尋優化關鍵**:
- 問句標題 (5W1H)
- 直接回答 (30 字內)
- 對話式長尾關鍵字
- 適合朗讀的句子

**2025 關鍵數據**:
- 60%+ 搜尋來自語音/行動
- 語音搜尋只提供 1 個答案

### 5. Wisdom Database 擴充

新增搜尋優化矩陣：
```
.claude/wisdom/frameworks/search_optimization_matrix.yaml
```

包含：
- 10+ 優化類型完整定義
- 平台 × 優化類型對照
- 2025 權重建議
- 內容類型優化指南

---

## 🆕 v2.5.0 新功能

### 1. 真實化學習系統

**自動 Session 記錄器**:
- Session 完成後自動提取學習數據
- 識別開頭模式、結構模式、CTA 模式
- 批次學習歷史 Session

```bash
# 批次學習
python3 .claude/skills/learning-database/auto_logger.py batch-learn \
    --from-sessions "output/session_*"

# 生成報告
python3 .claude/skills/learning-database/auto_logger.py report --type weekly
```

### 2. 效能監控上線

**效能追蹤器**:
- Phase 級別執行時間追蹤
- 效能評級 (A+/A/B/C/D)
- 瓶頸識別和優化建議

**效能儀表板**:
```bash
open .claude/performance/dashboard/index.html
```

### 3. 工程化基礎設施

**Skill 基類** (`.claude/skills/base/__init__.py`):
- 統一錯誤處理
- 自動日誌記錄
- 重試機制

**日誌系統** (`.claude/logs/`):
- skills.log - Skill 執行日誌
- errors.log - 錯誤日誌
- performance.log - 效能日誌

### 4. 補齊 Skills 實現

| Skill | 狀態 | 功能 |
|-------|------|------|
| content-repurposer | ✅ 完整 | 多平台內容改寫 |
| marketing-assets | ✅ 完整 | 行銷素材生成 |

```bash
# 生成行銷素材
python3 .claude/skills/marketing-assets/generate.py all \
    --input final_article.md --output-dir marketing/

# 多平台改寫
python3 .claude/skills/content-repurposer/repurpose.py all \
    --input final_article.md --output-dir repurposed/
```

---

## 🔮 v2.6.0 預覽: Writing Wisdom (世界級寫作智慧)

### 新增: Writing Wisdom Database

**解決的問題**: 系統過去只參考台灣部落格，缺乏世界級寫作標準對標。

**新增知識庫** (`.claude/wisdom/`):

| 類別 | 內容 | 用途 |
|------|------|------|
| **masters/** | Eugene Schwartz, Cialdini | 文案大師原則 |
| **frameworks/** | 5階段認知, SUCCESs | 核心寫作框架 |
| **anti-patterns/** | 邏輯謬誤檢測 | 驗證論證正確性 |

### 核心框架

**1. Schwartz 讀者認知 5 階段**:
```
Stage 1: Unaware (不知道) → 教育內容
Stage 2: Problem-Aware (知道問題) → 同理心開頭
Stage 3: Solution-Aware (知道有方案) → 差異化
Stage 4: Product-Aware (知道你的方法) → 證據案例
Stage 5: Most-Aware (已經相信) → 行動號召
```

**2. Cialdini 6 大說服原理**:
- 互惠 (Reciprocity)
- 承諾一致 (Commitment)
- 社會證明 (Social Proof)
- 喜好 (Liking)
- 權威 (Authority)
- 稀缺 (Scarcity)

**3. SUCCESs 記憶框架**:
- Simple (簡單)
- Unexpected (出乎意料)
- Concrete (具體)
- Credible (可信)
- Emotional (情感)
- Stories (故事)

**4. 邏輯謬誤檢測**:
- 因果謬誤 (後此謬誤, 相關≠因果)
- 過度概括 (倉促概括, 摘櫻桃)
- 論證結構 (循環論證, 假兩難, 滑坡)

### 使用方式

```bash
# Writer Agent 參考
Read: .claude/wisdom/frameworks/awareness_stages.yaml

# Editor Agent 驗證邏輯
Read: .claude/wisdom/anti-patterns/logic_fallacies.yaml

# 說服力檢查
Read: .claude/wisdom/masters/cialdini.yaml
```

---

## 👥 貢獻者

**開發團隊**: 喵哩文創 AI 寫手系統團隊
**技術架構**: Multi-Agent System + MCP Integration (v2.5.0)
**核心技術**: Claude Code + Python + WordPress + Google Analytics + Twitter

---

**最後更新**: 2025-12-11
**系統版本**: v2.5.0 "Reality Check" (17 Agents, 15 Skills 全部實現, 17 Phases)
**下次更新**: v2.6.0 Writing Wisdom (世界級寫作智慧) - 進行中
