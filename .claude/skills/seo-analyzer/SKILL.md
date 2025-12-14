---
name: seo-analyzer
description: Perform comprehensive SEO analysis on articles. Use when you need to optimize content for search engines, check keyword density, analyze readability, validate meta tags, or generate SEO improvement recommendations. Provides actionable insights with scoring (0-100).
license: MIT
version: 1.0.0
allowed-tools:
  - read
  - write
  - bash
---

# SEO Analyzer Skill

Comprehensive SEO analysis tool that evaluates articles across multiple dimensions and provides actionable optimization recommendations with quantified scoring.

## When to Use This Skill

Activate this skill when you need to:
- Analyze article SEO before publication
- Audit existing content for SEO improvements
- Check keyword density and distribution
- Validate meta tags (title, description, OG tags)
- Assess content readability and structure
- Generate SEO optimization recommendations
- Compare article versions for SEO effectiveness
- Prepare SEO reports for stakeholders

## Key Features

### 1. **Multi-Dimensional Analysis**
- ✅ Keyword optimization (density, prominence, distribution)
- ✅ Content structure (headings, paragraphs, lists)
- ✅ Readability (Flesch score, sentence length, vocabulary)
- ✅ Meta tags (title, description, Open Graph)
- ✅ Internal/external links
- ✅ Image optimization (alt text, file names)
- ✅ Technical SEO (URL structure, canonical tags)

### 2. **Scoring System**
```
Overall SEO Score: 0-100
├── Keyword Optimization: 25 points
├── Content Quality: 25 points
├── Technical SEO: 25 points
└── User Experience: 25 points
```

### 3. **Actionable Recommendations**
- Prioritized improvements (High/Medium/Low)
- Specific action items
- Expected impact quantification
- Before/after comparisons

## Usage Workflow

### Basic SEO Analysis

```
User: "分析這篇文章的 SEO"

Skill Actions:
1. Read article content
2. Extract metadata
3. Analyze keywords
4. Check structure
5. Assess readability
6. Generate score
7. Create recommendations
8. Output seo_analysis.md
```

### Keyword-Focused Analysis

```
User: "檢查文章對「Claude Code」這個關鍵字的優化程度"

Skill Actions:
1. Focus on target keyword
2. Check density (optimal: 1-2%)
3. Verify prominence (H1, first paragraph, etc.)
4. Analyze related keywords
5. Suggest improvements
```

### Competitive Analysis

```
User: "比較我的文章和競品的 SEO 表現"

Skill Actions:
1. Analyze your article
2. Fetch competitor content
3. Compare metrics
4. Identify gaps
5. Recommend improvements
```

## Analysis Framework

### 1. Keyword Optimization (25 points)

#### Primary Keyword Analysis

**Evaluation Criteria**:
```yaml
Keyword Density:
  Optimal: 1-2%
  Acceptable: 0.5-3%
  Over-optimization: >3%
  Under-optimization: <0.5%

Keyword Prominence:
  ✅ In H1 title (5 points)
  ✅ In first paragraph (5 points)
  ✅ In H2/H3 headings (3 points)
  ✅ In meta description (3 points)
  ✅ In URL slug (2 points)
  ✅ In image alt text (2 points)

Keyword Distribution:
  - Appears throughout content (not clustered)
  - Natural language integration
  - Semantic variations used
```

#### LSI (Latent Semantic Indexing) Keywords

```yaml
Related Keywords Check:
  - Synonyms present: ✅/❌
  - Topic variations: ✅/❌
  - Question keywords: ✅/❌
  - Long-tail variations: ✅/❌

Example for "Claude Code":
  Primary: Claude Code
  LSI: AI coding assistant, automated development, code generation,
       Claude API, anthropic Claude, AI programmer
```

### 2. Content Quality (25 points)

#### Content Structure

**Heading Hierarchy** (5 points):
```yaml
✅ Single H1 (article title)
✅ Logical H2 structure (3-5 sections)
✅ H3 for subsections
❌ No heading level skipping (H1 → H3)
❌ Not all H2s

Scoring:
  Perfect hierarchy: 5 points
  Minor issues: 3 points
  Major issues: 1 point
```

**Paragraph Structure** (5 points):
```yaml
Optimal:
  - Length: 3-5 sentences
  - Word count: 50-100 words
  - Clear topic sentence
  - Supporting details
  - Transition to next paragraph

Readability:
  - Short sentences (avg 15-20 words)
  - Active voice >70%
  - Varied sentence structure
```

**Content Length** (5 points):
```yaml
Word Count Guidelines:
  Comprehensive guide: 2000-3000 words (5 points)
  Standard article: 1000-2000 words (4 points)
  Short-form: 500-1000 words (3 points)
  Too short: <500 words (1 point)

Context matters:
  Tutorial/How-to: Longer is better
  News/Update: Concise is better
```

#### Readability (10 points)

**Flesch Reading Ease Score**:
```yaml
Score Ranges:
  90-100: Very Easy (5th grade) - 10 points
  80-89: Easy (6th grade) - 9 points
  70-79: Fairly Easy (7th grade) - 8 points
  60-69: Standard (8-9th grade) - 7 points ← Target
  50-59: Fairly Difficult (10-12th grade) - 5 points
  30-49: Difficult (College) - 3 points
  0-29: Very Difficult (Professional) - 1 point

Target for blog: 60-70 (Standard)
```

**Additional Readability Factors**:
```yaml
Sentence Length:
  Ideal average: 15-20 words
  Too long: >25 words (readability penalty)

Vocabulary:
  Simple words ratio: >80%
  Jargon: Define on first use
  Technical terms: Provide context

Formatting:
  ✅ Bullet points for lists
  ✅ Bold for emphasis
  ✅ Code blocks for examples
  ✅ Tables for comparisons
```

### 3. Technical SEO (25 points)

#### Meta Tags (10 points)

**Title Tag** (5 points):
```yaml
Optimal Format:
  "Primary Keyword - Secondary Keyword | Brand Name"
  Example: "Claude Code 完整指南 - AI 自動化開發 | 喵哩文創"

Requirements:
  ✅ Contains primary keyword (2 points)
  ✅ Length: 50-60 characters (2 points)
  ✅ Compelling and click-worthy (1 point)
  ❌ Not generic or stuffed

Scoring:
  Meets all criteria: 5 points
  Minor issues: 3 points
  Major issues: 1 point
```

**Meta Description** (5 points):
```yaml
Optimal Format:
  - Length: 150-160 characters
  - Contains primary keyword
  - Includes call-to-action
  - Describes value proposition
  - Compelling to click

Example:
  "學習如何用 Claude Code 自動化開發流程。完整教學包含實戰範例、
   最佳實踐和常見問題解答。10 分鐘快速上手！"

Scoring:
  Perfect description: 5 points
  Good but improvable: 3 points
  Needs work: 1 point
  Missing: 0 points
```

#### URL Structure (5 points)

```yaml
SEO-Friendly URL:
  ✅ Short and descriptive
  ✅ Contains primary keyword
  ✅ Uses hyphens (not underscores)
  ✅ Lowercase only
  ❌ No special characters
  ❌ No dates (unless news site)
  ❌ No unnecessary words (the, and, of)

Good: /claude-code-complete-guide
Bad: /2025/11/10/this-is-a-guide-about-claude-code-ai-tool

Scoring:
  Optimal: 5 points
  Acceptable: 3 points
  Poor: 1 point
```

#### Internal/External Links (10 points)

**Internal Links** (5 points):
```yaml
Best Practices:
  - 3-5 internal links per 1000 words
  - Relevant anchor text (not "click here")
  - Links to related articles
  - Distributes page authority

Example:
  Good: "了解更多關於 [AI 自動化最佳實踐](internal-link)"
  Bad: "想知道更多嗎？[點這裡](internal-link)"

Scoring:
  Optimal quantity & quality: 5 points
  Good but improvable: 3 points
  Too few or poor quality: 1 point
```

**External Links** (5 points):
```yaml
Guidelines:
  - 1-3 authoritative external links
  - Links to reputable sources
  - Opens in new tab (optional)
  - Adds credibility

Quality Indicators:
  ✅ Government/Education (.gov, .edu)
  ✅ Industry authorities
  ✅ Recent publications
  ❌ Low-quality or spammy sites

Scoring:
  High-quality external links: 5 points
  Acceptable links: 3 points
  Poor or no links: 1 point
```

### 4. User Experience (25 points)

#### Mobile Optimization (10 points)

```yaml
Factors:
  - Responsive design
  - Fast loading (<3 seconds)
  - Readable font size (16px+)
  - Touch-friendly buttons
  - No horizontal scrolling

While this skill can't test directly,
it checks for UX-friendly content:
  ✅ Short paragraphs (mobile-friendly)
  ✅ Bullet points (scannable)
  ✅ Clear headings (easy navigation)
```

#### Visual Elements (10 points)

**Images** (5 points):
```yaml
SEO-Friendly Images:
  ✅ Descriptive file names (claude-code-guide.png, not IMG_1234.png)
  ✅ Alt text with keywords
  ✅ Appropriate size (<500KB)
  ✅ Compressed for web
  ✅ Relevant to content

Alt Text Example:
  Good: "Claude Code 開發流程圖示範，展示從需求到部署的完整步驟"
  Bad: "圖片" or missing

Scoring:
  All images optimized: 5 points
  Most optimized: 3 points
  Few optimized: 1 point
  No images or unoptimized: 0 points
```

**Multimedia** (5 points):
```yaml
Bonus for:
  ✅ Code blocks with syntax highlighting
  ✅ Tables for data comparison
  ✅ Diagrams/flowcharts
  ✅ Videos (embedded with transcript)
  ✅ Interactive examples

Accessibility:
  - Alt text for all media
  - Captions for videos
  - Transcripts available
```

#### Engagement Factors (5 points)

```yaml
Metrics:
  - Clear CTA (call-to-action)
  - Table of contents for long articles
  - Related articles section
  - Social sharing buttons
  - Comment section

Quality Signals:
  - Answer user questions thoroughly
  - Provide actionable takeaways
  - Include real-world examples
  - Update date visible
```

## Output Format

### SEO Analysis Report

**File**: `output/session_*/seo_analysis.md`

```markdown
# 🎯 SEO 分析報告

**文章**: [文章標題]
**分析時間**: YYYY-MM-DD HH:MM:SS
**字數**: X,XXX 字

## 總體評分

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    SEO 整體分數: 85/100 ⭐⭐⭐⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

關鍵字優化:  22/25 ⭐⭐⭐⭐⭐
內容品質:    23/25 ⭐⭐⭐⭐⭐
技術 SEO:    21/25 ⭐⭐⭐⭐
使用者體驗:  19/25 ⭐⭐⭐⭐
```

## 詳細分析

### 1. 關鍵字優化 (22/25) ⭐⭐⭐⭐⭐

#### 主要關鍵字: "Claude Code"

**密度分析**:
- 出現次數: 18 次
- 總字數: 2,450 字
- 關鍵字密度: 0.73% ⚠️ (建議: 1-2%)
- **建議**: 增加 13-25 次出現

**關鍵字分佈**:
- ✅ H1 標題中出現
- ✅ 首段第一句出現
- ✅ 3 個 H2 小標中出現
- ✅ Meta description 中出現
- ✅ URL slug 中出現
- ⚠️ 圖片 alt 中僅 1/5 出現

**語意相關詞**:
- ✅ "AI 自動化" (12 次)
- ✅ "程式碼生成" (8 次)
- ✅ "開發工具" (6 次)
- ❌ 缺少: "Claude API", "Anthropic Claude"

**改善建議**:
1. 🔴 高優先: 提升關鍵字密度至 1.5%
   - 預期: 增加自然排名機會 +25%
   - 方法: 在內容中自然添加 15 次

2. 🟡 中優先: 優化圖片 alt text
   - 目標: 5/5 圖片包含關鍵字
   - 方法: 更新 alt 為 "Claude Code [具體描述]"

3. 🟢 低優先: 添加更多語意相關詞
   - 建議: 加入 "Claude API", "Anthropic"
   - 預期: 擴大語意範圍，捕獲長尾關鍵字

### 2. 內容品質 (23/25) ⭐⭐⭐⭐⭐

#### 文章結構 (5/5) ✅

```
H1: Claude Code 完整開發指南 ✅
├── H2: 什麼是 Claude Code？ ✅
├── H2: 核心功能介紹 ✅
│   ├── H3: Agent 系統 ✅
│   ├── H3: Skills 功能 ✅
│   └── H3: MCP 整合 ✅
├── H2: 實戰範例 ✅
└── H2: 最佳實踐 ✅
```

**評估**: 完美的階層結構 ✅

#### 段落品質 (5/5) ✅

- 平均段落長度: 4.2 句 (理想: 3-5 句) ✅
- 平均每段字數: 85 字 (理想: 50-100 字) ✅
- 主題句清晰: 是 ✅
- 段落過渡: 流暢 ✅

#### 內容長度 (5/5) ✅

- 字數: 2,450 字
- 類型: 完整教學指南
- 評估: 長度充足，涵蓋主題全面 ✅

#### 可讀性 (8/10) ⭐⭐⭐⭐

**Flesch Reading Ease**: 65.3
- 等級: Standard (8-9年級程度)
- 評價: 適合一般讀者 ✅

**細項分析**:
- 平均句長: 17.8 字 (理想: 15-20 字) ✅
- 簡單詞彙比例: 78% (目標: >80%) ⚠️
- 主動語態: 82% (目標: >70%) ✅

**改善建議**:
- 🟡 簡化 3-5 個技術術語
- 🟡 在首次出現時解釋專有名詞

### 3. 技術 SEO (21/25) ⭐⭐⭐⭐

#### Meta Title (4/5) ⭐⭐⭐⭐

```
Current: "Claude Code 完整開發指南 | 喵哩文創"
Length: 23 characters ⚠️ (建議: 50-60 字元)
```

**分析**:
- ✅ 包含主要關鍵字
- ⚠️ 太短，未充分利用空間
- ❌ 缺少次要關鍵字

**建議標題**:
```
Optimized: "Claude Code 完整開發指南 - AI 自動化程式碼生成工具教學 | 喵哩文創"
Length: 38 characters (更佳)
改善: +15% 預期 CTR
```

#### Meta Description (5/5) ✅

```
Current: "學習如何使用 Claude Code 自動化開發流程。完整教學包含 Agent 系統、
         Skills 功能和 MCP 整合。附實戰範例，10 分鐘快速上手！"
Length: 78 characters ✅
```

**評估**: 優秀
- ✅ 長度適中
- ✅ 包含關鍵字
- ✅ 有 CTA ("10 分鐘快速上手")
- ✅ 描述價值主張

#### URL Structure (5/5) ✅

```
Current: /claude-code-complete-guide
```

**評估**: 完美
- ✅ 包含關鍵字
- ✅ 簡短易記
- ✅ 使用連字號
- ✅ 全小寫

#### 連結分析 (7/10) ⭐⭐⭐⭐

**內部連結** (4/5):
- 數量: 4 個 (理想: 5-7 個)
- 錨文本: 描述性 ✅
- 相關性: 高 ✅

**外部連結** (3/5):
- 數量: 2 個 ⚠️ (建議: 3-4 個)
- 品質: 中等
  - ✅ 官方文檔 (code.claude.com)
  - ⚠️ 缺少權威來源 (.edu, .gov)

**改善建議**:
1. 🟡 新增 2-3 個內部連結到相關文章
2. 🟡 新增 1-2 個高權威外部連結

### 4. 使用者體驗 (19/25) ⭐⭐⭐⭐

#### 視覺元素 (3/5) ⚠️

**圖片使用**:
- 數量: 5 張
- Alt text 完整: 1/5 ❌
- 檔案命名: 2/5 使用描述性名稱 ⚠️
- 檔案大小: 平均 280KB ✅

**多媒體**:
- ✅ 程式碼區塊（8 個，有語法高亮）
- ✅ 表格（3 個）
- ❌ 無圖表/流程圖
- ❌ 無影片

**改善建議**:
1. 🔴 高優先: 補完所有圖片 alt text
   ```
   Before: "image1.png" - alt=""
   After: "claude-code-agent-workflow.png" - alt="Claude Code Agent 工作流程圖"
   ```

2. 🟡 中優先: 添加系統架構圖
   - 建議: Mermaid 流程圖或系統架構圖
   - 預期: 提升理解度 +30%

#### 互動元素 (4/5) ⭐⭐⭐⭐

- ✅ 目錄（Table of Contents）
- ✅ 清楚的 CTA 按鈕
- ✅ 相關文章推薦
- ❌ 缺少社群分享按鈕

#### 行動裝置友善度 (5/5) ✅

基於內容結構評估:
- ✅ 短段落（行動閱讀友善）
- ✅ 清楚標題（易於掃描）
- ✅ 列表格式（結構化）
- ✅ 無過寬表格

#### 載入速度因素 (7/10) ⭐⭐⭐⭐

基於內容評估:
- ✅ 圖片大小適中 (<500KB)
- ⚠️ 5 張圖片未壓縮
- ✅ 無大型嵌入式內容
- ✅ 程式碼區塊已優化

**建議**:
- 🟡 壓縮所有圖片至 <200KB
- 🟡 使用 WebP 格式（節省 30% 大小）

## 優先改善清單

### 🔴 高優先級（立即處理）

1. **提升關鍵字密度**
   - 當前: 0.73%
   - 目標: 1.5%
   - 行動: 自然添加 15 次關鍵字
   - 預期影響: 排名提升 +20-30%
   - 耗時: 15 分鐘

2. **補完圖片 Alt Text**
   - 當前: 1/5 有 alt
   - 目標: 5/5
   - 行動: 為每張圖添加描述性 alt
   - 預期影響: 圖片搜尋排名 +50%
   - 耗時: 10 分鐘

3. **優化 Meta Title**
   - 當前長度: 23 字元
   - 目標長度: 50-55 字元
   - 行動: 加入次要關鍵字
   - 預期影響: CTR +15%
   - 耗時: 5 分鐘

### 🟡 中優先級（本週處理）

4. **增加內部連結**
   - 當前: 4 個
   - 目標: 7 個
   - 行動: 連結到 3 篇相關文章
   - 預期影響: 停留時間 +20%
   - 耗時: 10 分鐘

5. **添加系統架構圖**
   - 當前: 無
   - 目標: 1-2 張流程圖
   - 行動: 使用 Mermaid 或繪圖工具
   - 預期影響: 理解度 +30%
   - 耗時: 30 分鐘

6. **壓縮圖片**
   - 當前: 平均 280KB
   - 目標: <200KB
   - 行動: 使用 TinyPNG 或 ImageOptim
   - 預期影響: 載入速度 +15%
   - 耗時: 5 分鐘

### 🟢 低優先級（選擇性）

7. **添加更多 LSI 關鍵字**
   - 建議詞: "Claude API", "Anthropic"
   - 預期影響: 長尾關鍵字排名
   - 耗時: 10 分鐘

8. **新增外部權威連結**
   - 目標: 1-2 個 .edu 或產業權威
   - 預期影響: 可信度提升
   - 耗時: 15 分鐘

## 競品對比（可選）

| 指標 | 你的文章 | 競品 A | 競品 B | 差距 |
|------|---------|--------|--------|------|
| SEO 分數 | 85 | 78 | 82 | ✅ 領先 |
| 字數 | 2,450 | 1,800 | 2,100 | ✅ 更詳盡 |
| 關鍵字密度 | 0.73% | 1.2% | 1.5% | ⚠️ 偏低 |
| 內部連結 | 4 | 7 | 6 | ⚠️ 較少 |
| 圖片數量 | 5 | 3 | 8 | ✅ 適中 |

## 預期成效

實施所有建議後:

```
改善前 SEO 分數: 85/100 ⭐⭐⭐⭐
預期改善後:     92/100 ⭐⭐⭐⭐⭐

關鍵改善:
  關鍵字優化: 22 → 25 ✅
  技術 SEO:   21 → 24 ✅
  使用者體驗: 19 → 23 ✅

預期效果:
  - 自然搜尋排名: +2-5 位
  - 點擊率 (CTR): +15-20%
  - 有機流量: +30-40%
  - 實施時間: 約 1.5 小時
```

---

**分析引擎**: SEO Analyzer Skill v1.0
**基準**: Google SEO 最佳實踐 2025
**更新日期**: 2025-11-10
```

## Best Practices

### 1. Consistent Analysis

```yaml
Use the Same Standards:
  - Apply identical criteria to all articles
  - Maintain scoring consistency
  - Document any rule changes
  - Track score evolution over time
```

### 2. Actionable Over Academic

```yaml
Focus on:
  ✅ Specific, implementable actions
  ✅ Expected impact quantification
  ✅ Priority guidance (High/Medium/Low)
  ✅ Time estimates for fixes

Avoid:
  ❌ Vague suggestions ("improve SEO")
  ❌ No priority guidance
  ❌ Unquantified benefits
```

### 3. Context Awareness

```yaml
Consider:
  - Content type (tutorial vs news vs review)
  - Target audience (technical vs general)
  - Competition level (niche vs popular)
  - Business goals (traffic vs conversions)

Adjust recommendations accordingly
```

## Integration with Blog Manager

This skill integrates as **Phase 4**:

```
Phase 3: Writer Agent → draft_final.md
Phase 4: seo-analyzer (this skill) → seo_analysis.md
Phase 4.5: Marketing Optimizer → marketing_assets.md
Phase 5: WordPress Publisher → publish
```

## Automation

### Auto-Check Before Publishing

```yaml
Trigger: Before Phase 5 (Publishing)
Action: Run SEO analysis
Condition: SEO Score must be ≥80
  If score <80: Pause and show improvements needed
  If score ≥80: Proceed to publish
```

### Batch Analysis

```
User: "分析 output/ 目錄下所有文章的 SEO"

Skill Actions:
1. Find all .md files in output/session_*/
2. Run SEO analysis on each
3. Generate comparative report
4. Identify patterns and common issues
5. Provide batch optimization suggestions
```

## Output Files

```
output/session_YYYYMMDD_HHMMSS/
├── seo_analysis.md           # Detailed analysis report
├── seo_score_card.txt        # Quick reference score
└── seo_improvements.json     # Structured data for automation
```

## Troubleshooting

### Score Seems Too Low

**Check**:
- Is the content type appropriate? (tutorials need more depth)
- Are you comparing to the right benchmarks?
- Did you include all required elements?

**Adjust**:
- Review scoring criteria for your niche
- Consider audience (technical content may score lower on readability, but that's okay)

### Can't Improve Score Further

**Plateau Effect**:
- Scores 85-90 are excellent
- Beyond 90 requires diminishing returns effort
- Focus on actual traffic/conversions, not just score

**Reality Check**:
```yaml
Score 100: Theoretically perfect (unrealistic)
Score 90-95: Excellent (top 5%)
Score 80-90: Very Good (top 20%)
Score 70-80: Good (above average)
Score <70: Needs improvement
```

---

**Skill Maintained By**: 喵哩文創 AI 寫手系統團隊
**Last Updated**: 2025-11-10
**Scoring Method**: Multi-dimensional weighted analysis
**Based On**: Google SEO Best Practices 2025
