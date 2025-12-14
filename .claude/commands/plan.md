# 顯示執行計劃 (v2.6.0)

顯示指定模式的執行計劃。v2.6.0 新增 Search Everywhere 優化流程。

## 參數

- `$ARGUMENTS`: 模式名稱 (quick/standard/full/publish/story/seo/search/llmo/voice)，預設 standard

---

## 執行動作

根據指定模式，展示執行計劃：

### quick 模式

```
================================================================
執行計劃: ⚡ 快速模式 (quick)
================================================================

快速完成核心內容，跳過可選步驟
適用場景: 時間緊迫、簡單內容

總 Phases: 4
預估時間: ~5 分鐘

執行步驟:
----------------------------------------
  Step 1: Experience Collector (Phase 0)
  Step 2: Content Analyst (Phase 1)
  Step 3: Writer Agent (Phase 3)
  Step 4: Editor Agent (Phase 3.5)
================================================================
```

### standard 模式

```
================================================================
執行計劃: 📝 標準模式 (standard)
================================================================

完整品質流程，適合大部分情況
適用場景: 一般部落格文章

總 Phases: 10
預估時間: ~15 分鐘

執行步驟:
----------------------------------------
  Step 1: Experience Collector (Phase 0)
  Step 2: Content Analyst (Phase 1)
  Step 3: [Research Agent | Style Matcher] (並行)
  Step 4: Writer Agent (Phase 3)
  Step 5: Fact Checker (Phase 3.6)
  Step 6: Humanizer Agent (Phase 3.7)
  Step 7: Persuasion Agent (Phase 3.8)
  Step 8: Editor Agent (Phase 3.5)
  Step 9: SEO Optimizer (Phase 4)
================================================================
```

### full 模式

```
================================================================
執行計劃: 🔥 完整模式 (full)
================================================================

執行所有 Phases，生成完整行銷素材
適用場景: 重要內容、完整行銷素材

總 Phases: 17
預估時間: ~30 分鐘

執行步驟:
----------------------------------------
  Step 1: Performance Optimizer (Phase 13) [背景]
  Step 2: Memory Agent (Phase 11) [背景]
  Step 3: Experience Collector (Phase 0)
  Step 4: Content Analyst (Phase 1)
  Step 5: [Research Agent | Style Matcher] (並行)
  Step 6: Writer Agent (Phase 3)
  Step 7: Quality Predictor (Phase 3.4)
  Step 8: Fact Checker (Phase 3.6)
  Step 9: Humanizer Agent (Phase 3.7)
  Step 10: Persuasion Agent (Phase 3.8)
  Step 11: Storyteller Agent (Phase 3.9)
  Step 12: Editor Agent (Phase 3.5)
  Step 13: SEO Optimizer (Phase 4)
  Step 14: Persona Adapter (Phase 12)
  Step 15: Publisher Agent (Phase 5)
  Step 16: Marketing Assets (Phase 6)
  Step 17: Analytics Reporter (Phase 7)
================================================================
```

### search 模式 🆕 v2.6.0

```
================================================================
執行計劃: 🌐 Search Everywhere 模式 (search)
================================================================

完整 AISO 優化，最大化跨平台搜尋能見度
適用場景: 重要內容需要被 Google、AI、語音全面覆蓋

總 Phases: 19
預估時間: ~25 分鐘

執行步驟:
----------------------------------------
  Step 1: Experience Collector (Phase 0)
  Step 2: Content Analyst (Phase 1)
  Step 3: [Research Agent | Style Matcher] (並行)
  Step 4: Writer Agent (Phase 3) + LLMO 格式優化
  Step 5: Quality Predictor (Phase 3.4)
  Step 6: Fact Checker (Phase 3.6)
  Step 7: Humanizer Agent (Phase 3.7)
  Step 8: Persuasion Agent (Phase 3.8) + CRO 優化
  Step 9: Editor Agent (Phase 3.5)
  Step 10: SEO Optimizer (Phase 4a) - 傳統 SEO
  Step 11: LLMO Optimizer (Phase 4d) - AI 引用優化 🆕
  Step 12: GEO Optimizer (Phase 4e) - 生成式搜尋 🆕
  Step 13: VSO Optimizer (Phase 4f) - 語音搜尋 🆕
  Step 14: CRO Optimizer (Phase 4g) - 轉換率 🆕
  Step 15: AISO Scorer (Phase 4h) - 統一評分 🆕
================================================================

AISO 評分權重 (2025):
  SEO: 20% | GEO: 20% | LLMO: 20%
  AEO: 15% | E-E-A-T: 15% | VSO: 5% | CRO: 5%
================================================================
```

### llmo 模式 🆕 v2.6.0

```
================================================================
執行計劃: 🤖 LLMO 模式 (llmo)
================================================================

專注 AI 搜尋優化，讓內容被 ChatGPT/Perplexity 引用
適用場景: 希望在 AI 回答中被引用

總 Phases: 12
預估時間: ~20 分鐘

執行步驟:
----------------------------------------
  Step 1: Experience Collector (Phase 0)
  Step 2: Content Analyst (Phase 1)
  Step 3: Writer Agent (Phase 3) + LLMO 格式
  Step 4: Fact Checker (Phase 3.6) - 確保可引用
  Step 5: Editor Agent (Phase 3.5)
  Step 6: LLMO Optimizer (Phase 4d) ⭐ 重點
  Step 7: GEO Optimizer (Phase 4e) ⭐ 重點
  Step 8: AISO Scorer (Phase 4h)
================================================================

LLMO 優化重點:
  • 結構化標題 (H1 > H2 > H3)
  • 明確術語定義
  • 數據來源引用
  • FAQ 問答格式
================================================================
```

## 使用方式

```
/plan quick
/plan standard
/plan full
/plan search    # 🆕 v2.6.0
/plan llmo      # 🆕 v2.6.0
/plan voice     # 🆕 v2.6.0
```

會自動展示對應模式的執行計劃。
