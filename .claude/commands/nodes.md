# 顯示可用 Phases

顯示 AI 寫手系統所有可用的處理 Phases。

---

## 執行動作

讀取 `.claude/agents/` 目錄中的 Agent 定義，並以下格式展示所有可用 Phases：

```
================================================================
喵哩文創 AI 寫手系統 - 可用 Phases
================================================================

⭐ Critical Phases (必須執行)
----------------------------------------
  Phase 0    | Experience Collector | 收集真實經驗
  Phase 1    | Content Analyst      | 分析原文結構
  Phase 3    | Writer Agent         | 撰寫文章
  Phase 3.5  | Editor Agent         | 品質審查

⚠️ Important Phases (建議執行)
----------------------------------------
  Phase 2a   | Research Agent       | 市場研究
  Phase 2b   | Style Matcher        | 風格學習
  Phase 3.6  | Fact Checker         | 事實驗證
  Phase 3.7  | Humanizer Agent      | 內容人類化
  Phase 3.8  | Persuasion Agent     | 說服力強化
  Phase 4    | SEO Optimizer        | SEO 優化

⭕ Optional Phases (可選)
----------------------------------------
  Phase 3.9  | Storyteller Agent    | 故事敘事
  Phase 5    | Publisher Agent      | WordPress 發布
  Phase 6    | Marketing Assets     | 行銷素材
  Phase 7    | Analytics Reporter   | 數據分析
  Phase 12   | Persona Adapter      | 多讀者版本

🔄 Background Phases (自動執行)
----------------------------------------
  Phase 11   | Memory Agent         | 跨 Session 學習
  Phase 13   | Performance Optimizer| 效能優化

================================================================
```

## 在 /write 命令中選擇 Phases

使用 `/write` 命令時，會透過 AskUserQuestion 互動選擇要執行的 Phases。

也可以透過參數直接指定：

```
/write https://example.com --quick
```

`--quick` 模式只執行 Critical Phases，跳過 Optional。
