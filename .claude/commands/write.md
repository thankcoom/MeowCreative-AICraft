# AI 寫手工作流程 (v2.6.0)

啟動互動式寫作流程，從輿情分析開始，讓你選擇最佳主題。v2.6.0 新增 Search Everywhere 模式。

## 參數
- `$ARGUMENTS`: URL、關鍵字或選項 (可選)
  - URL → 直接改寫該文章
  - 關鍵字 → 搜尋該主題的熱門內容
  - `--quick` → 跳過選擇，快速執行
  - `--research` → 只做研究，不寫文章
  - `--search` → 🆕 v2.6.0 完整 AISO 優化
  - `--llmo` → 🆕 v2.6.0 專注 AI 引用優化
  - `--voice` → 🆕 v2.6.0 語音搜尋優化

---

## 執行流程

### Phase 0: 輿情分析與熱點發現 🔥

**如果沒有提供 URL，先執行市場研究：**

1. **詢問目標領域**：
   使用 AskUserQuestion 工具：
   ```
   questions:
     - question: "你想寫哪個領域的內容？"
       header: "領域"
       options:
         - label: "💰 投資理財"
           description: "股票、ETF、被動收入、財務自由"
         - label: "📚 自我成長"
           description: "閱讀、學習、生產力、習慣"
         - label: "💻 科技工具"
           description: "AI、軟體、效率工具"
         - label: "🏠 生活風格"
           description: "極簡、整理、生活哲學"
   ```

2. **執行熱點搜尋**：
   使用 WebSearch 搜尋：
   - `"{領域} 2025 熱門話題 site:matters.town OR site:medium.com"`
   - `"{領域} 討論 site:ptt.cc OR site:dcard.tw"`
   - `"{領域} trending site:twitter.com"`

3. **呈現熱門主題清單**：
   分析搜尋結果，整理成表格：
   ```
   ┌────┬──────────────────────────┬─────────┬────────┐
   │ #  │ 主題                     │ 熱度    │ 競爭度 │
   ├────┼──────────────────────────┼─────────┼────────┤
   │ 1  │ [主題名稱]               │ 🔥🔥🔥   │ 中     │
   │ 2  │ [主題名稱]               │ 🔥🔥     │ 低     │
   │ 3  │ [主題名稱]               │ 🔥🔥🔥🔥 │ 高     │
   └────┴──────────────────────────┴─────────┴────────┘
   ```

4. **讓用戶選擇主題**：
   使用 AskUserQuestion 工具：
   ```
   questions:
     - question: "選擇要寫的主題？"
       header: "主題"
       options:
         - label: "[熱門主題 1]"
           description: "熱度高、競爭中等"
         - label: "[熱門主題 2]"
           description: "熱度中、競爭低 (推薦)"
         - label: "[熱門主題 3]"
           description: "熱度極高、競爭激烈"
   ```

5. **搜尋參考素材**：
   找到選定主題的 3-5 篇優質參考文章，列出：
   ```
   參考素材：
   1. [標題] - [來源] - [URL]
   2. [標題] - [來源] - [URL]
   3. [標題] - [來源] - [URL]
   ```

---

### Phase 1: 確認寫作設定

使用 AskUserQuestion 確認：

```
questions:
  - question: "選擇創作類型？"
    header: "類型"
    options:
      - label: "📝 深度長文"
        description: "2000-3000字、SEO優化、適合部落格"
      - label: "⚡ 快速短文"
        description: "800-1200字、重點摘要"
      - label: "📱 社群貼文"
        description: "300-500字、適合FB/IG"
      - label: "🎯 改寫優化"
        description: "基於參考素材改寫"
```

```
questions:
  - question: "要使用品牌風格嗎？"
    header: "品牌"
    options:
      - label: "喵哩文創"
        description: "親和友善 | 真實經驗 | SEO優化"
      - label: "通用風格"
        description: "中性專業"
```

---

### Phase 2: 收集真實經驗

**重要：確保內容真實性**

詢問用戶：
```
questions:
  - question: "你有這個主題的真實經驗嗎？"
    header: "經驗"
    options:
      - label: "✅ 有實際經驗"
        description: "我會分享我的真實經歷"
      - label: "📖 研究整理"
        description: "基於研究，明確標註非親身經驗"
      - label: "🔄 混合型"
        description: "部分有經驗，部分需研究"
```

如果選「有實際經驗」，追問具體細節：
- 你什麼時候開始接觸這個主題？
- 有什麼具體的成果或數據？
- 遇過什麼困難？如何解決？

---

### Phase 3: 執行寫作流程

根據設定，依序執行：

1. **content-analyst** - 分析參考素材結構
2. **research-agent** - 補充市場研究 (並行)
3. **style-matcher** - 學習目標風格 (並行)
4. **writer-agent** - 撰寫初稿 (含 LLMO 格式優化)
5. **quality-predictor** - 品質預測 🆕 v2.4.0
6. **fact-checker** - 事實驗證
7. **humanizer-agent** - 人類化處理
8. **persuasion-agent** - 說服力優化
9. **editor-agent** - 品質審查
10. **seo-optimizer** - SEO 優化

### Phase 3b: Search Everywhere 優化 🆕 v2.6.0

如果使用 `--search` 模式，額外執行：

11. **llmo-optimizer** - AI 引用優化
12. **geo-optimizer** - 生成式搜尋優化
13. **vso-optimizer** - 語音搜尋優化
14. **cro-optimizer** - 轉換率優化
15. **aiso-scorer** - 統一評分 (目標: 70+)

---

### Phase 4: 輸出與確認

顯示完成結果：

```
✅ 文章完成！

📊 品質評分 (AISO v2.6.0)
├── 內容品質: 87/100
├── SEO 分數: 92/100 (傳統搜尋)
├── LLMO 分數: 85/100 (AI 引用) 🆕
├── GEO 分數: 83/100 (生成式搜尋) 🆕
├── E-E-A-T: 80/100
├── 人類化: 85/100
└── AISO 綜合: 88/100 🆕

📁 輸出檔案
├── output/session_YYYYMMDD_HHMMSS/
│   ├── final_article.md      ← 主文章
│   ├── seo_report.md         ← SEO 分析
│   ├── titles.md             ← 10個標題變體
│   └── social_posts.md       ← 社群貼文版本
```

詢問下一步：
```
questions:
  - question: "接下來要做什麼？"
    header: "下一步"
    options:
      - label: "📤 發布到 WordPress"
        description: "使用 publisher-agent 發布"
      - label: "✏️ 修改調整"
        description: "告訴我要改哪裡"
      - label: "📱 生成更多社群素材"
        description: "IG 輪播、Twitter Thread"
      - label: "✅ 完成"
        description: "結束本次工作"
```

---

## 快速模式

```
/write https://example.com --quick
```

跳過所有選擇，直接：
1. 抓取 URL 內容
2. 使用喵哩品牌風格
3. 執行完整寫作流程
4. 輸出結果

---

## 純研究模式

```
/write 投資理財 --research
```

只執行 Phase 0（輿情分析），不寫文章：
1. 搜尋熱門主題
2. 分析競爭程度
3. 推薦最佳切入點
4. 列出參考素材

---

## 範例

```bash
# 完整互動流程
/write

# 指定領域研究
/write AI工具

# 直接改寫文章
/write https://example.com/article

# 快速改寫
/write https://example.com/article --quick

# 只做研究
/write 被動收入 --research

# 🆕 v2.6.0 Search Everywhere 模式
/write https://example.com/article --search

# 🆕 v2.6.0 LLMO 優化 (被 AI 引用)
/write https://example.com/article --llmo

# 🆕 v2.6.0 語音搜尋優化
/write https://example.com/article --voice
```

---

## v2.6.0 新功能速覽

### AISO (AI Search Optimization) 評分權重

| 優化類型 | 權重 | 說明 |
|---------|------|------|
| SEO | 20% | Google/Bing 傳統搜尋 |
| GEO | 20% | 生成式 AI 搜尋 (Perplexity) |
| LLMO | 20% | 大語言模型引用 (ChatGPT) |
| AEO | 15% | Featured Snippet |
| E-E-A-T | 15% | 內容可信度 |
| VSO | 5% | 語音助理 |
| CRO | 5% | 轉換率 |

### 2025 關鍵數據
- AI 搜尋流量成長 **1,200%**
- AI 用戶轉換率是傳統的 **4.4 倍**
- **82.5%** 的 AI 引用來自深層頁面
- **65%** 搜尋以零點擊結束
