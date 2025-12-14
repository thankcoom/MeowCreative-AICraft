---
name: marketing-assets
description: Generate comprehensive marketing assets from articles including headline variations, hook openers, CTAs, thumbnail designs, and email subject lines. Use when you need to create marketing materials for content promotion across multiple channels. Optimizes for click-through rates and engagement.
license: MIT
version: 1.0.0
allowed-tools:
  - read
  - write
---

# Marketing Assets Generator Skill

Automatically generates a complete suite of marketing materials optimized for different platforms and objectives. Transforms technical content into compelling marketing copy that drives clicks and engagement.

## When to Use This Skill

Activate this skill when you need to:
- Generate multiple headline variations for A/B testing
- Create attention-grabbing hook openers
- Design call-to-action (CTA) variations
- Get thumbnail/featured image design recommendations
- Generate email marketing subject lines
- Create social media teaser copy
- Produce push notification messages
- Develop newsletter snippets

## Core Features

### 1. **Headline Variations** (3-5 types)
- Technical/SEO-optimized
- Number-driven (clickbait-resistant)
- Pain-point focused
- Curiosity-driven
- Benefit-oriented

### 2. **Hook Openers** (3-4 variations)
- Story-based opening
- Question-based opening
- Statistic-based opening
- Bold statement opening

### 3. **Call-to-Actions** (Multiple intensities)
- Soft CTA (informative)
- Medium CTA (encouraging)
- Strong CTA (urgent)
- Platform-specific CTAs

### 4. **Visual Design Guidance**
- Thumbnail design recommendations
- Color scheme suggestions
- Typography guidance
- Visual hierarchy tips

### 5. **Email Marketing**
- Subject line variations
- Preview text optimization
- Email body teasers

## Usage Workflow

### Standard Asset Generation

```
User: "生成這篇文章的所有行銷素材"

Skill Actions:
1. Read article content
2. Extract core value propositions
3. Identify pain points and solutions
4. Generate 5 headline variations
5. Create 4 hook opener versions
6. Develop CTA variations (soft/medium/strong)
7. Design thumbnail recommendations
8. Generate email subject lines
9. Create social teasers
10. Output marketing_assets.md
```

### Focused Generation

```
User: "我只需要標題變體和社群文案"

Skill Actions:
1. Generate 5 headline variations
2. Create platform-specific social copy
3. Skip other assets
4. Quick output
```

### A/B Testing Prep

```
User: "準備 A/B testing 用的標題和開頭"

Skill Actions:
1. Generate 3 distinctly different headlines
2. Create matching hook openers
3. Predict performance for each
4. Recommend testing strategy
```

## Asset Templates

### 1. Headline Variations

#### Type A: Technical/SEO-Optimized

**Format**:
```
[Primary Keyword] [Action Verb] [Benefit/Outcome]
```

**Examples**:
```
1. "Claude Code 完整開發指南：從零到專家的實戰教學"
2. "WordPress 自動發布系統：用 Python 打造高效內容流程"
3. "AI 自動化寫作：5個步驟提升內容產出效率400%"
```

**Characteristics**:
- ✅ Contains primary keyword
- ✅ Clear value proposition
- ✅ 50-60 characters optimal
- ✅ Descriptive and trustworthy

**Best For**: Google search, WordPress, Medium

---

#### Type B: Number-Driven

**Format**:
```
[Number] 個 [Noun] 讓你 [Desired Outcome]
```

**Examples**:
```
1. "7個 Claude Code 技巧讓你開發效率提升 10 倍"
2. "5個步驟完成 WordPress 自動化發布系統"
3. "3個關鍵設定讓 AI 寫作品質媲美專業編輯"
```

**Characteristics**:
- ✅ Specific number (odd numbers perform better)
- ✅ Clear promise
- ✅ Quantified benefit when possible
- ✅ Action-oriented

**Best For**: Medium, LinkedIn, Facebook

---

#### Type C: Pain-Point Focused

**Format**:
```
[Frustration] ？[Solution] [Benefit]
```

**Examples**:
```
1. "還在手動發文到 10 個平台？自動化工具幫你省下 90% 時間"
2. "每天花 3 小時寫文章卻沒流量？SEO 優化技巧立即見效"
3. "AI 寫的文章總是太機械化？這個方法讓內容更人性化"
```

**Characteristics**:
- ✅ Identifies relatable pain point
- ✅ Offers clear solution
- ✅ Quantifies improvement
- ✅ Creates urgency

**Best For**: Facebook groups, Email, Twitter

---

#### Type D: Curiosity-Driven

**Format**:
```
[Intriguing Statement] | [Why You Should Care]
```

**Examples**:
```
1. "90% 的開發者不知道的 Claude Code 秘密功能"
2. "我用這個方法讓文章流量增加 400% | 完整實戰分享"
3. "為什麼頂尖工程師都在用這個 AI 工具？深度解析"
```

**Characteristics**:
- ✅ Creates information gap
- ✅ Promises insider knowledge
- ✅ Uses social proof or statistics
- ✅ Hints at revelation

**Best For**: Twitter, Instagram, Threads

---

#### Type E: Benefit-Oriented

**Format**:
```
如何 [Achieve Desired Outcome] | [Timeframe/Ease Factor]
```

**Examples**:
```
1. "如何用 Claude Code 10 分鐘完成一天的工作 | 附完整程式碼"
2. "如何讓 AI 寫出 85 分以上的高品質文章 | 實測有效"
3. "如何打造自動化內容行銷系統 | 零程式基礎也能上手"
```

**Characteristics**:
- ✅ Clear "how-to" promise
- ✅ Includes timeframe or difficulty level
- ✅ Adds credibility marker
- ✅ Removes barriers ("零基礎也能")

**Best For**: YouTube, Email newsletters, LinkedIn

### 2. Hook Openers

#### Hook A: Story-Based

**Structure**:
```
[Time Marker] + [Situation] + [Transformation Tease]
```

**Template**:
```
三個月前，我還在 [painful situation]. 每天花 [X hours] 做 [tedious task]，
累得半死卻看不到成效。

直到我發現了 [solution]...

現在，同樣的工作只需要 [X minutes]，而且品質還提升了 [X%].

今天要分享的，就是這個改變我工作方式的完整流程。
```

**Example**:
```
三個月前，我還在手動發文章到 10 個不同平台。每天花 3 小時複製貼上、
調整格式，累得半死卻只能發 2 篇文章。

直到我建立了這個自動化系統...

現在，一篇文章 2 分鐘就能同步發布到所有平台，而且還會自動優化格式。
一個月省下 90 小時，文章產出量提升 5 倍。

今天要分享的，就是這個自動化發布系統的完整搭建流程。
```

**Why It Works**:
- ✅ Relatable struggle (reader sees themselves)
- ✅ Clear transformation (creates hope)
- ✅ Quantified results (builds credibility)
- ✅ Promise of revelation (hooks curiosity)

---

#### Hook B: Question-Based

**Structure**:
```
[Provocative Question] + [Common Wrong Answer] + [Hint at Truth]
```

**Template**:
```
[Target Outcome] 最大的障礙是什麼？

大部分人會說是 [common belief]. 但其實，真正的關鍵在於 [insight].

我花了 [time period] 測試，分析了 [X] 個案例，發現 [surprising finding].

接下來的 [X] 分鐘，我會告訴你 [promise].
```

**Example**:
```
讓 AI 寫出高品質文章最大的障礙是什麼？

大部分人會說是「AI 技術還不夠成熟」。但其實，真正的關鍵在於你給的
指令和工作流程。

我花了 3 個月測試，分析了 50+ 篇 AI 生成的文章，發現品質差異的核心
原因不是 AI 本身，而是使用方法。

接下來的 10 分鐘，我會告訴你如何讓 AI 寫出 85 分以上、媲美專業編輯
的文章。
```

**Why It Works**:
- ✅ Engages reader immediately (question)
- ✅ Challenges assumptions (intrigue)
- ✅ Shows expertise (research/testing)
- ✅ Clear value promise (what they'll learn)

---

#### Hook C: Statistic-Based

**Structure**:
```
[Shocking Statistic] + [Why It Matters] + [Your Unique Insight]
```

**Template**:
```
[X%] 的 [target audience] 正在 [doing something wrong].

這導致 [negative outcome], 每年浪費 [quantified loss].

但有一小群人（不到 [Y%]）知道 [secret/method], 他們的 [metric]
是一般人的 [X] 倍。

今天要揭露的，就是這 [Y%] 的人都在用的 [solution].
```

**Example**:
```
92% 的內容創作者正在用錯誤的方式使用 AI 寫作工具。

這導致生成的內容千篇一律、缺乏深度，每篇文章平均停留時間不到 1 分鐘。
每年浪費數百小時卻看不到流量成長。

但有一小群人（不到 5%）知道如何正確設計 AI 工作流程，他們的文章
停留時間是一般人的 3 倍，轉化率高出 5 倍。

今天要揭露的，就是這 5% 的人都在用的系統化寫作流程。
```

**Why It Works**:
- ✅ Attention-grabbing statistic (shock value)
- ✅ Creates urgency (you might be doing it wrong)
- ✅ Exclusivity angle (join the elite 5%)
- ✅ Promise of insider knowledge

---

#### Hook D: Bold Statement

**Structure**:
```
[Controversial Claim] + [Why Most Disagree] + [Your Proof]
```

**Template**:
```
[Controversial statement].

我知道這聽起來 [crazy/impossible/contradictory]. 大部分 [experts/people]
都會說 [common belief].

但我在過去 [time period] 親自驗證，結果顯示 [your finding].

現在我要分享 [how to replicate].
```

**Example**:
```
AI 寫的文章可以比人工寫的更好。

我知道這聽起來很狂妄。大部分內容創作者都會說「AI 缺乏創意」、
「讀起來很機械化」。

但我在過去 6 個月用 AI 寫了 100+ 篇文章，其中 23 篇的 Editor 評分
超過 90 分，比我之前人工寫的平均分數還高 15 分。

現在我要分享如何設計一個能持續產出高品質內容的 AI 系統。
```

**Why It Works**:
- ✅ Challenges conventional wisdom (memorable)
- ✅ Acknowledges skepticism (builds trust)
- ✅ Provides evidence (credibility)
- ✅ Clear learning promise

### 3. Call-to-Actions (CTAs)

#### Soft CTA (Informative)

**Tone**: Educational, helpful, low-pressure

**Templates**:
```
1. "想了解更多？完整教學在這裡 👉 [link]"
2. "有興趣深入學習的話，可以參考這篇 [link]"
3. "延伸閱讀：[related topic] [link]"
4. "相關資源：[link to resource]"
```

**Best For**:
- Blog post conclusions
- Educational content
- Building trust
- Top-of-funnel content

---

#### Medium CTA (Encouraging)

**Tone**: Motivational, action-oriented, benefits-focused

**Templates**:
```
1. "準備好提升效率了嗎？立即下載完整指南 👉 [link]"
2. "別讓這些技巧被埋沒！收藏這篇文章隨時回來查看 🔖"
3. "想親手試試看？跟著這個教學開始你的第一個專案 🚀 [link]"
4. "覺得有幫助嗎？分享給同樣需要的朋友 ➡️"
```

**Best For**:
- Tutorial endings
- How-to guides
- Mid-funnel content
- Social media posts

---

#### Strong CTA (Urgent)

**Tone**: Urgent, exclusive, FOMO-inducing

**Templates**:
```
1. "⏰ 限時優惠：前 100 名免費領取完整模板 [link]"
2. "🎁 現在訂閱，立即獲得價值 $97 的資源包（僅限本週）"
3. "❌ 不要再浪費時間手動操作！現在就自動化你的工作流程 [link]"
4. "🔥 已有 1,247 人開始使用，你還在等什麼？[link]"
```

**Best For**:
- Product launches
- Limited offers
- Bottom-of-funnel
- Conversion-focused campaigns

---

#### Platform-Specific CTAs

**For Instagram**:
```
"💾 儲存這篇貼文，下次需要時立刻找到
🔗 完整教學在我的 Bio 連結
📩 有問題？留言或 DM 我"
```

**For Twitter/X**:
```
"🧵 這個 thread 有幫助嗎？

❤️ Like 讓我知道
🔁 Retweet 分享給需要的人
💬 留言你最大的收穫"
```

**For LinkedIn**:
```
"這個方法幫助我的團隊節省 40% 的時間。

如果你也面臨類似挑戰，歡迎：
• 在留言區分享你的經驗
• 連結我討論更多細節
• 追蹤我了解更多自動化技巧"
```

**For YouTube**:
```
"如果這個教學對你有幫助：
👍 請按讚支持
🔔 訂閱頻道不錯過新影片
💬 留言告訴我你最想學什麼
📥 完整程式碼在描述欄"
```

### 4. Thumbnail Design Recommendations

#### Design Framework

**Hero Image Composition**:
```yaml
Layout: Rule of Thirds
  - Main subject: Left or right third
  - Text overlay: Opposite side
  - Negative space: Allow room to breathe

Contrast: High
  - Subject vs Background: 70%+ contrast
  - Text vs Background: 90%+ contrast
  - Use complementary colors

Focus: Single Main Element
  - One clear focal point
  - Supporting elements subordinate
  - No clutter or confusion
```

#### Color Schemes

**Scheme A: Tech/Professional**
```
Primary: #2563EB (Blue)
Secondary: #10B981 (Green)
Accent: #F59E0B (Amber)
Background: #F9FAFB (Light Gray)

Mood: Trustworthy, modern, professional
Best For: Tutorials, technical content, B2B
```

**Scheme B: Creative/Energetic**
```
Primary: #EC4899 (Pink)
Secondary: #8B5CF6 (Purple)
Accent: #F97316 (Orange)
Background: #FFFFFF (White)

Mood: Creative, dynamic, engaging
Best For: Social media, creative content, lifestyle
```

**Scheme C: Minimal/Elegant**
```
Primary: #000000 (Black)
Secondary: #6B7280 (Gray)
Accent: #EF4444 (Red)
Background: #FFFFFF (White)

Mood: Clean, sophisticated, timeless
Best For: Design content, portfolios, premium offerings
```

#### Typography Guidelines

**Headline Text**:
```yaml
Font Family: Sans-serif (bold, high-impact)
  Recommended: Inter Black, Montserrat Bold, Poppins ExtraBold
Size: 72-96pt (for 1200x630 image)
Weight: 700-900 (Bold to Black)
Line Height: 1.1-1.2 (tight for impact)
Max Characters: 40-50 (2-3 lines)
Contrast: White on dark or Black on light with shadow
```

**Supporting Text**:
```yaml
Font Family: Same as headline or complementary sans-serif
Size: 24-36pt
Weight: 400-600 (Regular to SemiBold)
Purpose: Subtitle, author name, or key stat
```

#### Visual Elements

**Icons/Illustrations**:
```
Purpose: Reinforce topic at a glance
Style: Match overall aesthetic (flat, 3D, line art)
Size: 30-40% of canvas
Position: Left or right third
Color: Accent color from palette
```

**Badges/Labels**:
```
Types:
  - "NEW" badge for fresh content
  - "GUIDE" for comprehensive tutorials
  - "FREE" for gated content offers
  - Time indicator ("10 MIN READ")

Style:
  - Small, non-intrusive (top-right corner)
  - High contrast for visibility
  - Rounded corners for modern feel
```

#### Platform-Specific Specs

**WordPress Featured Image**:
```
Dimensions: 1200 x 630 px
Aspect Ratio: 1.91:1
File Format: JPG (optimized) or WebP
Max Size: 500 KB
Text: Large, easily readable at thumbnail size
```

**Instagram Square Post**:
```
Dimensions: 1080 x 1080 px
Aspect Ratio: 1:1
File Format: JPG
Max Size: 10 MB (but aim for <1 MB)
Text: Centered, bold, high contrast
```

**LinkedIn Article Header**:
```
Dimensions: 1200 x 627 px
Aspect Ratio: 1.91:1
File Format: PNG or JPG
Style: Professional, text-light (LinkedIn adds overlay)
```

**YouTube Thumbnail**:
```
Dimensions: 1280 x 720 px
Aspect Ratio: 16:9
File Format: JPG or PNG
Max Size: 2 MB
Text: Large, bold (readable at small sizes)
Faces: Close-up with expressive emotion works well
```

### 5. Email Marketing Assets

#### Subject Lines

**Type A: Benefit-Driven**
```
1. "節省 90% 時間的內容發布秘訣"
2. "讓文章流量提升 3 倍的 SEO 技巧"
3. "10 分鐘學會自動化你的工作流程"
```

**Type B: Curiosity-Gap**
```
1. "這個工具讓我每天多出 3 小時......"
2. "為什麼 92% 的人都用錯 AI 寫作工具？"
3. "我測試了 30 個自動化工具，只推薦這 3 個"
```

**Type C: Personalized**
```
1. "{{Name}}，你的工作流程可以更高效"
2. "還記得你問的 {{Topic}} 嗎？答案在這裡"
3. "專屬於 {{Segment}} 的自動化指南"
```

**Type D: Urgency/Scarcity**
```
1. "⏰ 限時：免費領取自動化模板（剩 48 小時）"
2. "最後機會：100 個免費名額即將額滿"
3. "本週限定：價值 $97 的資源包免費送"
```

#### Preview Text (Preheader)

**Purpose**: Complement subject line, provide additional context

**Examples**:
```
Subject: "節省 90% 時間的內容發布秘訣"
Preview: "我測試了 6 個月，這是最有效的方法 →"

Subject: "為什麼 92% 的人都用錯 AI 寫作工具？"
Preview: "避免這 5 個常見錯誤，讓 AI 成為你的得力助手"

Subject: "10 分鐘學會自動化你的工作流程"
Preview: "附完整程式碼和逐步教學，新手也能立即上手"
```

**Best Practices**:
- Length: 40-100 characters
- Complements (doesn't repeat) subject
- Adds urgency or benefit
- Includes CTA hint ("→", "立即查看")

### 6. Social Media Teasers

#### Twitter Thread Opener

```
🧵 分享一個讓我工作效率提升 10 倍的系統

不需要學新工具
不需要寫程式
只要 3 個步驟

以下是完整流程 👇
```

#### LinkedIn Teaser

```
過去 3 個月，我用 AI 寫了 50+ 篇文章

其中 23 篇評分超過 90 分，比我之前人工寫的還好。

今天分享完整的 AI 內容生產系統。

包含：
✅ 工作流程設計
✅ 品質控制機制
✅ 實際案例分析

完整內容在文章連結 👉 [link]

#AI #內容行銷 #自動化
```

#### Facebook Group Post

```
【實戰分享】用 Claude Code 打造自動化發布系統

大家好，我花了 2 週時間搭建了一個自動化內容發布系統，
現在一篇文章可以同步發到 10 個平台，只需要 2 分鐘。

詳細記錄了完整過程，包括：
• 系統架構設計
• 遇到的坑和解決方法
• 完整程式碼（開源）

希望對同樣想自動化流程的朋友有幫助！

文章連結：[link]
```

## Output Format

### Marketing Assets Report

**File**: `output/session_*/marketing_assets.md`

```markdown
# 🎯 行銷素材包

**文章**: [文章標題]
**生成時間**: YYYY-MM-DD HH:MM:SS

---

## 📋 素材清單

- ✅ 5 種標題變體
- ✅ 4 種開頭鉤子
- ✅ CTA 變體（軟/中/強）
- ✅ 縮圖設計指南
- ✅ Email 主旨行
- ✅ 社群媒體文案

---

## 1. 標題變體（Headline Variations）

### A. 技術型（SEO 優化）

**標題**: "Claude Code Skills 完整開發指南：從基礎到進階實戰"
- **長度**: 28 字元 ✅
- **關鍵字**: ✅ "Claude Code", "Skills", "開發指南"
- **適用平台**: WordPress, Medium, Google Search
- **預期 CTR**: 4.5-5.5%

### B. 數字型

**標題**: "7 個 Claude Code Skills 技巧讓你開發效率提升 300%"
- **長度**: 31 字元 ✅
- **數字**: 7 (奇數, 優)
- **量化**: 300% (具體成效)
- **適用平台**: Medium, LinkedIn, Facebook
- **預期 CTR**: 6.5-8.0%

### C. 痛點型

**標題**: "還在手動寫重複代碼？Claude Code Skills 幫你自動化 90% 工作"
- **長度**: 36 字元 ✅
- **痛點**: "手動寫重複代碼" (明確)
- **解決**: "自動化 90%" (量化)
- **適用平台**: Facebook 社團, Twitter, Email
- **預期 CTR**: 7.0-9.0%

### D. 好奇型

**標題**: "95% 開發者不知道的 Claude Code 進階功能｜深度解析"
- **長度**: 31 字元 ✅
- **吸引點**: "95% 不知道" (稀缺性)
- **承諾**: "深度解析" (價值)
- **適用平台**: Twitter, Instagram, Threads
- **預期 CTR**: 5.5-7.0%

### E. 效益型

**標題**: "如何用 Claude Code 10 分鐘完成 8 小時的工作｜附完整程式碼"
- **長度**: 34 字元 ✅
- **時間對比**: "10分鐘 vs 8小時" (強烈)
- **附加價值**: "附完整程式碼" (可信)
- **適用平台**: YouTube, LinkedIn, Email
- **預期 CTR**: 8.0-10.0%

---

## 2. 開頭鉤子（Hook Openers）

### Hook A: 故事型

兩個月前，我還在用傳統方式寫程式。每次遇到重複任務，就複製舊代碼、
手動修改、測試、除錯......一個簡單的 CRUD API 就要花 3 小時。

直到我開始用 Claude Code Skills...

現在，同樣的任務 10 分鐘就能完成，而且代碼品質比我手寫的還好。
錯誤率降低 80%，開發速度提升 5 倍。

今天要分享的，就是這套讓我工作方式徹底改變的 Skills 系統。

**為什麼有效**:
- ✅ 可感同身受的痛點
- ✅ 具體的轉變數據
- ✅ 清楚的價值承諾

**適合平台**: Blog, Medium, LinkedIn

---

### Hook B: 問題型

開發效率的最大瓶頸是什麼？

大部分人會說「寫代碼太慢」。但其實，真正的問題在於你一直在重複造輪子。

我花了 1 個月分析自己的工作流程，發現 65% 的時間都在做重複性任務：
寫 CRUD、處理錯誤、寫測試、更新文檔......

接下來 10 分鐘，我會告訴你如何用 Claude Code Skills 自動化這 65% 的工作。

**為什麼有效**:
- ✅ 引發思考
- ✅ 挑戰常見認知
- ✅ 提供數據支持

**適合平台**: Email, YouTube, Twitter Thread

---

### Hook C: 數據型

87% 的開發者正在浪費時間寫重複代碼。

這導致平均每週損失 12 小時生產力，一年累積超過 600 小時。

但有一小群人（不到 8%）知道如何用 AI 工具自動化這些任務，
他們的開發速度是普通開發者的 3-5 倍。

今天要揭露的，就是這 8% 的人都在用的 Skills 系統。

**為什麼有效**:
- ✅ 震撼數據
- ✅ 量化損失 (緊迫感)
- ✅ 精英群體 (渴望歸屬)

**適合平台**: LinkedIn, Facebook, Medium

---

### Hook D: 宣言型

AI 開發工具可以比傳統 IDE 更強大。

我知道這聽起來很誇張。很多資深開發者都會說「AI 只是輔助」、
「還是要靠人工審查」。

但我在過去 3 個月用 Claude Code 完成了 30+ 個專案，其中代碼品質
評分平均 92 分，比我之前手寫的高出 18 分。

現在我要分享如何設計一個能持續產出高品質代碼的 AI 工作流程。

**為什麼有效**:
- ✅ 挑戰主流觀點
- ✅ 承認質疑 (誠實)
- ✅ 提供實證

**適合平台**: Blog, Twitter, YouTube

---

## 3. CTA 變體（Call-to-Actions）

### 軟 CTA（資訊型）

**CTA 1**:
```
想了解更多 Claude Code Skills 的進階用法？
完整教學文章在這裡 👉 [連結]
```

**CTA 2**:
```
延伸閱讀：
• 如何建立第一個 Claude Code Skill
• Skills vs Agents 的選擇策略
• 最佳實踐和常見錯誤
```

**適用**: Blog 文章結尾, 教育內容

---

### 中 CTA（鼓勵型）

**CTA 1**:
```
準備好提升開發效率了嗎？

🚀 立即下載 Skills 開發模板
📚 查看完整範例程式碼
💬 加入開發者社群討論

開始你的自動化之旅 👉 [連結]
```

**CTA 2**:
```
覺得這篇教學有幫助？

👍 按讚讓我知道
💾 收藏起來隨時查閱
📤 分享給同樣需要的開發者

你的支持是我持續分享的動力！
```

**適用**: Tutorial 結尾, How-to 指南

---

### 強 CTA（急迫型）

**CTA 1**:
```
⏰ 限時優惠：前 100 名免費領取

✅ Skills 開發完整模板包
✅ 20+ 實戰範例程式碼
✅ 獨家進階技巧文檔

價值 $97，現在免費領取 👉 [連結]

僅限本週，不要錯過！
```

**CTA 2**:
```
❌ 不要再浪費時間手動寫重複代碼！

現在就下載自動化工具包：
• 10 分鐘完成設定
• 立即提升效率 300%
• 1,247 位開發者已在使用

立即開始 👉 [連結]
```

**適用**: 產品發布, 限時優惠, 轉化導向

---

## 4. 縮圖設計指南（Thumbnail Design）

### 主視覺概念

**配色方案**: Tech Professional
```
主色: #2563EB (藍色) - 科技感
輔色: #10B981 (綠色) - 成功/成長
強調色: #F59E0B (琥珀色) - 重點標記
背景: #F9FAFB (淺灰) - 乾淨、專業
```

### 排版建議

```
┌────────────────────────────────────┐
│                                    │
│  [LOGO]              [BADGE: NEW]  │
│                                    │
│         Claude Code                │
│         SKILLS                     │
│         完整指南                   │
│                                    │
│  [Icon:                            │
│   代碼圖示]     • 從零到專家       │
│                • 實戰教學          │
│                • 附完整程式碼      │
│                                    │
│                    喵哩文創 ───────│
└────────────────────────────────────┘

尺寸: 1200 x 630 px
字體: Inter Bold (標題) + Inter Regular (副標)
對比: 高對比確保可讀性
```

### 文字層次

**主標題**:
- 字體: Inter Black, 84pt
- 顏色: #1F2937 (深灰，幾乎黑)
- 行高: 1.1
- 最多 3 行

**副標題/要點**:
- 字體: Inter Medium, 32pt
- 顏色: #6B7280 (中灰)
- Bullet points 用 "•" 或 checkmark

### 視覺元素

**圖示選擇**:
- 風格: Line art 或 Flat design
- 大小: 約佔畫面 30%
- 位置: 左側或右側三分之一處
- 顏色: 使用輔色 (#10B981)

**Badge/標籤**:
```
NEW | GUIDE | FREE | 10 MIN
位置: 右上角
樣式: 圓角矩形，強調色背景
```

### 工具推薦

1. **Canva**
   - 模板: 選擇「Blog Banner」或「LinkedIn Post」
   - 尺寸: 自訂為 1200 x 630 px
   - 匯出: JPG, 品質 85%

2. **Figma**
   - 更專業，完全自訂
   - 可建立設計系統
   - 團隊協作方便

3. **DALL-E 3** (若需要自訂插圖)
   - Prompt: "Modern flat design illustration of [topic],
              clean lines, tech style, blue and green color scheme"

---

## 5. Email 行銷素材（Email Marketing Assets）

### 主旨行變體

**變體 1（效益型）**:
```
Subject: 節省 90% 開發時間的 Skills 系統
Preview: 我測試了 3 個月，這是最有效的方法 →
預期開信率: 28-32%
```

**變體 2（好奇型）**:
```
Subject: 這個工具讓我每天多出 3 小時......
Preview: 而且完全不需要寫額外的代碼
預期開信率: 25-30%
```

**變體 3（個人化）**:
```
Subject: {{Name}}，你的開發流程可以更高效
Preview: 專屬於 {{JobTitle}} 的自動化指南
預期開信率: 32-38%
```

**變體 4（急迫型）**:
```
Subject: ⏰ 限時：免費 Skills 模板（剩 48 小時）
Preview: 價值 $97，現在免費領取 →
預期開信率: 35-42%
```

### Email 正文片段

**開頭段落**:
```
Hi {{Name}},

還記得上週你問我如何提升開發效率嗎？

我花了整整一週整理，把過去 3 個月使用 Claude Code Skills
的經驗濃縮成這份完整指南。

包含：
✅ 完整開發流程
✅ 20+ 實戰範例
✅ 常見錯誤和解決方法

讓我們開始吧 👇
```

**正文結構**:
```
1. 簡短問候和背景 (上面的開頭段落)
2. 主要內容摘要（3-5 個重點）
3. 具體價值主張
4. 強烈 CTA
5. P.S. 附加價值或緊迫性提醒
```

---

## 6. 社群媒體文案（Social Media Copy）

### Instagram 貼文

```
【開發者必看】Claude Code Skills 完整指南 ⚡

還在手動寫重複代碼？
這套系統幫你自動化 90% 工作！

📌 重點整理：
• 從零開始建立 Skills
• 10+ 實戰範例
• 避開常見錯誤
• 提升效率 300%+

完整教學在 Bio 連結 🔗

---

你目前用哪些自動化工具？
留言告訴我！👇

#AI開發 #自動化 #Claude #程式設計 #開發工具
#Productivity #CodingLife #DevTools
```

### Twitter/X Thread 開頭

```
🧵 分享一個讓開發效率提升 10 倍的系統

不需要學新語言
不需要改變工作習慣
只要 3 個步驟

這是我過去 3 個月實測的完整流程 👇

(1/15)
```

### LinkedIn 貼文

```
過去 3 個月，我用 Claude Code Skills 完成了 30+ 個專案。

代碼品質評分平均 92 分，比之前手寫的高出 18 分。
開發時間減少 65%。

今天分享完整的 Skills 開發系統。

重點包含：
✅ 系統架構設計
✅ 最佳實踐和反模式
✅ 20+ 實戰範例
✅ 完整開發流程

對 AI 輔助開發有興趣的朋友，這篇文章應該能幫助你建立
一套高效的自動化工作流程。

完整文章 👉 [連結]

你對 AI 開發工具有什麼想法？歡迎在留言區討論。

#AI #軟體開發 #自動化 #生產力
```

---

## 📊 素材使用建議

### A/B Testing 計畫

**測試組合 1**:
- 標題: 數字型 ("7 個技巧提升 300%")
- 縮圖: 高對比，數字突出
- 平台: Medium, Facebook
- 預期: CTR 6.5-8.0%

**測試組合 2**:
- 標題: 痛點型 ("還在手動...？")
- 縮圖: 對比 before/after
- 平台: Twitter, Email
- 預期: CTR 7.0-9.0%

**測試組合 3**:
- 標題: 效益型 ("10 分鐘完成 8 小時工作")
- 縮圖: 時間對比視覺
- 平台: LinkedIn, YouTube
- 預期: CTR 8.0-10.0%

### 平台優先級

根據 Analytics 數據建議:

1. **Medium** (ROI 最高)
   - 使用: 技術型標題 + 詳細縮圖
   - 發布時間: 週二早上 8:00

2. **LinkedIn** (專業受眾)
   - 使用: 效益型標題 + 專業配色
   - 發布時間: 週四上午 9:00

3. **Twitter** (快速傳播)
   - 使用: 好奇型標題 + Thread opener
   - 發布時間: 週二晚上 9:00

### 30 天發布計畫

```
Week 1:
  Day 1: WordPress 主站發布（技術型標題）
  Day 2: Medium（數字型標題）
  Day 3: LinkedIn（效益型標題）

Week 2:
  Day 8: Email Newsletter（個人化主旨）
  Day 10: Twitter Thread（好奇型開頭）

Week 3:
  Day 15: Facebook 社團（痛點型）
  Day 17: Instagram Carousel

Week 4:
  Day 22: 再分享 Top 表現平台
  Day 28: A/B Testing 結果分析
```

---

## 📈 預期表現

基於歷史數據和行業標準:

| 素材類型 | 預期 CTR | 最佳平台 | 優化後 CTR |
|---------|---------|---------|-----------|
| 技術型標題 | 4.5-5.5% | WordPress, Google | 5.0-6.0% |
| 數字型標題 | 6.5-8.0% | Medium, LinkedIn | 7.5-9.0% |
| 痛點型標題 | 7.0-9.0% | Facebook, Email | 8.0-10.0% |
| 好奇型標題 | 5.5-7.0% | Twitter, Instagram | 6.5-8.0% |
| 效益型標題 | 8.0-10.0% | YouTube, LinkedIn | 9.0-12.0% |

**整體預期**:
- 平均 CTR 提升: 35-50%
- 社群分享增加: 60-80%
- Email 開信率: 25-40%
- 轉化率改善: 15-25%

---

**素材包版本**: 1.0
**生成時間**: YYYY-MM-DD HH:MM:SS
**有效期**: 建議 30 天內使用（趨勢變化）
**下次更新**: 基於 A/B Testing 結果
```

## Best Practices

### 1. Authenticity First

```yaml
真實性檢查:
  ❌ 不要誇大數據
  ❌ 不要虛構案例
  ✅ 使用真實測試結果
  ✅ 承認限制和挑戰
  ✅ 提供可驗證的證據
```

### 2. Platform Optimization

```yaml
平台差異:
  Blog: 詳細、SEO 優化、教育性
  LinkedIn: 專業、B2B 導向、數據支持
  Twitter: 簡潔、吸睛、快速消費
  Instagram: 視覺優先、情緒連結
  Email: 個人化、價值明確、強 CTA
```

### 3. A/B Testing Discipline

```yaml
測試方法:
  - 一次只改變一個變數
  - 足夠樣本量（最少 100 次曝光）
  - 記錄完整數據
  - 迭代優化，不要「設定後遺忘」
```

## Integration with Blog Manager

Fits as **Phase 4.5**:

```
Phase 4: SEO Optimizer → seo_report.md
Phase 4.5: marketing-assets (this skill) → marketing_assets.md
Phase 5: WordPress Publisher → publish
Phase 5.2: Content Repurposer → social variations
```

## Output Files

```
output/session_YYYYMMDD_HHMMSS/
├── marketing_assets.md           # Main report
├── headlines.txt                 # Quick reference headlines
├── thumbnail_specs.json          # Design specifications
└── ab_testing_plan.md            # Testing recommendations
```

---

**Skill Maintained By**: 喵哩文創 AI 寫手系統團隊
**Last Updated**: 2025-11-10
**Based On**: Marketing best practices & conversion optimization
**Optimization Focus**: Click-through rates, engagement, conversions
