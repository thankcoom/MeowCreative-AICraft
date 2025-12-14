---
name: content-repurposer
description: Transform long-form articles into multiple content formats for social media. Use when you need to repurpose blog posts into Twitter threads, Instagram carousels, short posts, video scripts, or LinkedIn articles. Maximizes content reach by creating 20-30 platform-optimized variations from a single source.
license: MIT
version: 1.0.0
allowed-tools:
  - read
  - write
  - bash
---

# Content Repurposer Skill

Automatically transforms long-form articles into multiple content formats optimized for different social media platforms. Converts one article into 20-30 reusable content pieces.

## When to Use This Skill

Activate this skill when you need to:
- Generate Twitter/X thread from blog post (10-15 tweets)
- Create Instagram carousel content (5-8 slides)
- Extract key quotes for social media (8-10 quote cards)
- Write LinkedIn article (simplified version)
- Produce short posts for Facebook/社團 (5-10 posts)
- Generate short-form video scripts (TikTok/YouTube Shorts)
- Create email newsletter content

## Input Requirements

**Primary Input**: A completed long-form article (1500-3000 words)
- Preferred format: Markdown
- Location: `output/session_*/final_article.md`
- Should include clear sections, headings, and key points

**Optional Metadata**:
- `seo_report.md` - for keywords and focus
- `marketing_assets.md` - for tone and platform preferences

## Output Structure

Skill generates organized content in:
```
output/session_YYYYMMDD_HHMMSS/repurposed_content/
├── twitter_thread.md
├── instagram_carousel.md
├── linkedin_article.md
├── short_posts/
│   ├── post_01.md
│   ├── post_02.md
│   ├── ...
│   └── post_10.md
├── quote_cards/
│   ├── quote_01.txt
│   ├── ...
│   └── quote_08.txt
├── video_scripts/
│   ├── short_1.md (60s)
│   ├── short_2.md (60s)
│   └── short_3.md (60s)
└── email_newsletter.md
```

## Repurposing Strategy

### Content Hierarchy

1. **Identify Core Message** (1 sentence)
   - The central thesis of the article
   - Used as foundation for all variations

2. **Extract Key Points** (3-5 main ideas)
   - Each becomes a standalone piece
   - Forms section breaks in longer formats

3. **Find Supporting Details**
   - Statistics, examples, quotes
   - Used for quote cards and engagement hooks

4. **Isolate Actionable Takeaways** (5-10 items)
   - Practical tips readers can apply
   - Perfect for numbered lists and social posts

## Platform-Specific Formatting

### Twitter/X Thread

**Structure**:
```
Tweet 1 (Hook):
  - Attention-grabbing opener
  - Problem statement or bold claim
  - Max 280 characters

Tweet 2-3 (Context):
  - Why this matters
  - Background information

Tweet 4-12 (Main Content):
  - One key point per tweet
  - Use line breaks for readability
  - Include emojis sparingly

Tweet 13-14 (Conclusion):
  - Summary
  - Call-to-action

Tweet 15 (Bonus):
  - Thread recap with numbers
  - "If you found this useful, retweet the first tweet"
```

**Best Practices**:
- Each tweet should standalone
- Use numbered format (1/15, 2/15...)
- Include visual breaks (━━━━━)
- Add engagement prompts every 4-5 tweets
- End with CTA and thread link

**Example Tweet Format**:
```markdown
1/15 還在手動寫 CRUD？

用 Claude Code Agent 10 分鐘完成 API 開發 ↓

今天分享完整實戰流程 🧵

---

2/15 問題：手寫 API 的 3 大痛點

❌ 重複性代碼寫到手軟
❌ 一個 bug 查半天
❌ 文檔永遠過期

有更好的方法 👇
```

### Instagram Carousel

**Structure (6-8 slides)**:

**Slide 1 (Cover)**:
```
━━━━━━━━━━━━━━━━━
   主標題
   (大字, 吸睛)
━━━━━━━━━━━━━━━━━
   副標題說明
   (小字)
```

**Slide 2 (Problem)**:
```
你是不是也遇到...

問題 1 ❌
問題 2 ❌
問題 3 ❌

[圖示: 困擾的表情]
```

**Slide 3-6 (Solutions)**:
```
解決方案 #1

━━━━━━━━━━━

具體做法:
• 步驟 1
• 步驟 2
• 步驟 3

[圖示: 相關 icon]
```

**Slide 7 (Results)**:
```
實際成果 📊

效率提升 ↑ 400%
時間節省 ↓ 90%
品質提升 ↑ 85%

[圖示: 統計圖表]
```

**Slide 8 (CTA)**:
```
想學更多？

👆 追蹤我的帳號
💾 儲存這篇貼文
🔗 完整教學在 Bio

[圖示: Follow icon]
```

**Design Guidance**:
- Consistent color scheme (3 colors max)
- Large, readable font (min 36pt)
- Adequate white space
- Icon/emoji for visual interest
- Branded footer on each slide

### LinkedIn Article

**Optimized Length**: 60% of original (900-1800 words)

**Structure**:
```markdown
# 專業標題（關鍵字優化）

**開場白** (2-3 句)
- 直切問題
- 建立可信度
- 引發好奇

## 背景脈絡

[簡化版原文背景，商業導向]

## 核心洞察 #1

[詳細展開主要論點]

💡 **實務建議**: [可立即應用的技巧]

## 核心洞察 #2

[第二個主要論點]

📊 **數據支持**: [統計或案例]

## 核心洞察 #3

[第三個主要論點]

✅ **行動步驟**: [清楚的下一步]

## 結論

[總結價值主張]

---

**你的經驗是什麼？**
在留言區分享你的想法 👇

#標籤1 #標籤2 #標籤3
```

**Tone Adjustments**:
- More formal than Twitter
- Data-driven and professional
- Business value emphasis
- Include personal insights
- Encourage discussion

### Short Posts (FB/社團)

**5-10 Variations** - Each 150-300 words

**Format Types**:

**Type 1: Problem-Solution**
```markdown
【痛點解決】你是不是也遇到這個問題？

很多人都在用手動方式 [XXX]，結果：
❌ 浪費時間
❌ 容易出錯
❌ 無法規模化

其實有更好的方法 👇

[簡短解決方案 3-5 點]

想知道完整做法嗎？
👉 [連結]

#標籤 #相關主題
```

**Type 2: Numbered List**
```markdown
【實用技巧】7 個 Claude Code 省時技巧

1️⃣ [技巧 1 + 一句說明]
2️⃣ [技巧 2 + 一句說明]
3️⃣ [技巧 3 + 一句說明]
...

每個都能立即使用 ⚡

你最常用哪一個？留言告訴我 👇
```

**Type 3: Story Format**
```markdown
【真實案例】我用 Claude Code 把工作效率提升 400%

一個月前，我還在 [描述痛苦現狀]...

直到我發現了 [解決方案]

結果：
✅ 成果 1
✅ 成果 2
✅ 成果 3

最驚訝的是...[關鍵轉折]

完整分享在這裡 👉 [連結]
```

**Type 4: Question Hook**
```markdown
你知道 90% 的開發者都不知道的秘密嗎？

[提出反直覺的觀點]

我測試了 30 天，發現：
• 發現 1
• 發現 2
• 發現 3

詳細實驗結果 👉 [連結]

你有試過嗎？
```

**Type 5: Myth-Busting**
```markdown
【打破迷思】關於 AI 自動化的 3 個誤解

❌ 迷思 1: [常見誤解]
✅ 事實: [正確認知]

❌ 迷思 2: [常見誤解]
✅ 事實: [正確認知]

❌ 迷思 3: [常見誤解]
✅ 事實: [正確認知]

完整解析 👉 [連結]
```

### Quote Cards

**8-10 Impactful Quotes**

**Format**:
```
"[簡潔有力的金句]"

— 來源/作者
```

**Selection Criteria**:
- Standalone value (no context needed)
- Shareable and memorable
- 10-25 words ideal
- Emotionally resonant or intellectually provocative

**Visual Design Guidance**:
```yaml
Dimensions: 1080 x 1080px (Instagram)
Background: Solid color or subtle gradient
Font: Bold, sans-serif, min 48pt
Text Color: High contrast
Attribution: Small, bottom-right
Brand Element: Logo/watermark, subtle
```

**Examples**:
```
"AI 不會取代你，
但懂 AI 的人會。"

━━━━━━━━━━━
@你的帳號名稱
```

### Video Scripts (Short-Form)

**3 Scripts** - Each 45-60 seconds

**Structure**:

**Second 0-3 (Hook)**:
```
[視覺: 特寫鏡頭]
旁白: "還在手動寫 CRUD？"

[畫面: 展示痛苦場景]
旁白: "我也是，直到我發現這個..."
```

**Second 4-45 (Content)**:
```
[視覺: 分割畫面展示 before/after]

旁白: "用 Claude Code，只需要 3 個步驟："

[畫面: 步驟 1 演示]
旁白: "第一，[簡短說明]"

[畫面: 步驟 2 演示]
旁白: "第二，[簡短說明]"

[畫面: 步驟 3 演示]
旁白: "第三，[簡短說明]"

[畫面: 展示結果]
旁白: "就這樣，10 分鐘完成！"
```

**Second 46-60 (CTA)**:
```
[視覺: 回到主持人]
旁白: "想學完整教學？"

[畫面: 文字浮現 + 指向 Bio]
旁白: "連結在我的個人簡介"

[畫面: 結尾卡]
文字: "追蹤 @你的帳號 學更多"
```

**B-Roll Suggestions**:
- Screen recording of actual workflow
- Side-by-side comparisons
- Progress indicators
- Minimal text overlays (3-5 words max)

### Email Newsletter

**Length**: 40-50% of original (600-1500 words)

**Structure**:

**Subject Line Options** (3 variations):
```
1. [數字導向] "7 個 Claude Code 技巧讓你效率提升 400%"
2. [好奇心] "90% 開發者不知道的自動化秘密"
3. [個人化] "{名字}，你還在手動寫代碼嗎？"
```

**Email Body**:
```markdown
Hi {名字},

[個人化開場 - 1-2 句]

今天想分享一個讓我工作效率提升 400% 的方法...

━━━━━━━━━━━━━━━━━

## 🎯 核心問題

[簡述痛點，讀者立刻共鳴]

## 💡 解決方案

[精簡版主要內容，3-5 個要點]

**要點 1: [標題]**
[2-3 句說明]

**要點 2: [標題]**
[2-3 句說明]

**要點 3: [標題]**
[2-3 句說明]

## 📊 實際成果

[展示數據或案例]

## ⚡ 立即行動

想深入了解完整做法？

👉 [閱讀完整文章](連結)

━━━━━━━━━━━━━━━━━

下週預告: [teaser 下一期內容]

有問題隨時回信告訴我！

Best,
[署名]

P.S. [額外價值或限時優惠]
```

## Processing Workflow

### Step 1: Analyze Source Article

```python
def analyze_article(article_path):
    """Extract key components from source article"""

    with open(article_path) as f:
        content = f.read()

    analysis = {
        'core_message': extract_core_message(content),
        'key_points': extract_key_points(content),
        'statistics': extract_statistics(content),
        'examples': extract_examples(content),
        'quotes': extract_quotable_lines(content),
        'actionable_items': extract_actionables(content),
        'word_count': len(content.split())
    }

    return analysis
```

### Step 2: Generate Platform-Specific Content

```python
def generate_all_formats(analysis):
    """Create all repurposed content"""

    outputs = {}

    # Twitter Thread
    outputs['twitter'] = generate_twitter_thread(
        core_message=analysis['core_message'],
        key_points=analysis['key_points'],
        target_tweets=12-15
    )

    # Instagram Carousel
    outputs['instagram'] = generate_instagram_carousel(
        key_points=analysis['key_points'],
        statistics=analysis['statistics'],
        slides=6-8
    )

    # Short Posts
    outputs['short_posts'] = generate_short_posts(
        key_points=analysis['key_points'],
        examples=analysis['examples'],
        count=5-10
    )

    # Quote Cards
    outputs['quotes'] = select_quote_cards(
        quotes=analysis['quotes'],
        count=8-10
    )

    # Video Scripts
    outputs['videos'] = generate_video_scripts(
        key_points=analysis['key_points'][0:3],
        duration=60  # seconds
    )

    # LinkedIn Article
    outputs['linkedin'] = generate_linkedin_article(
        analysis=analysis,
        length_ratio=0.6
    )

    # Email Newsletter
    outputs['newsletter'] = generate_newsletter(
        analysis=analysis,
        length_ratio=0.4-0.5
    )

    return outputs
```

### Step 3: Write Output Files

```python
def save_repurposed_content(outputs, session_path):
    """Save all variations to organized structure"""

    base_path = Path(session_path) / 'repurposed_content'
    base_path.mkdir(exist_ok=True)

    # Save each format
    (base_path / 'twitter_thread.md').write_text(outputs['twitter'])
    (base_path / 'instagram_carousel.md').write_text(outputs['instagram'])
    (base_path / 'linkedin_article.md').write_text(outputs['linkedin'])
    (base_path / 'email_newsletter.md').write_text(outputs['newsletter'])

    # Save collections
    short_posts_dir = base_path / 'short_posts'
    short_posts_dir.mkdir(exist_ok=True)
    for i, post in enumerate(outputs['short_posts'], 1):
        (short_posts_dir / f'post_{i:02d}.md').write_text(post)

    # ... similar for quotes and videos
```

## Best Practices

### Content Quality Standards

1. **Maintain Authenticity**
   - Don't fabricate new information
   - Use only facts from source article
   - Preserve original voice and tone

2. **Optimize for Each Platform**
   - Respect character limits
   - Use platform-specific formatting
   - Include appropriate hashtags/mentions

3. **Ensure Standalone Value**
   - Each piece should work independently
   - No need to read source article
   - Complete thought in each variation

4. **Maximize Engagement**
   - Start with strong hooks
   - Use pattern interrupts
   - Include clear CTAs

### SEO and Discoverability

**Keyword Integration**:
- Read `seo_report.md` for primary keywords
- Naturally incorporate into repurposed content
- Use variations to avoid repetition

**Hashtag Strategy**:
- Twitter: 2-3 hashtags max
- Instagram: 10-15 hashtags (mix of sizes)
- LinkedIn: 3-5 professional hashtags

### Publishing Schedule

**Recommended Distribution** (30-day plan):

```yaml
Week 1:
  Day 1: Publish original article
  Day 2: Twitter thread
  Day 3: LinkedIn article
  Day 5: Instagram carousel

Week 2:
  Day 8-12: Short posts (1 per day)
  Day 14: Email newsletter

Week 3:
  Day 15-21: Quote cards (1 per day)

Week 4:
  Day 22-24: Video scripts (1 per day)
  Day 28: Twitter thread recap
```

## Integration with Blog Manager

Fits into workflow as **Phase 5.2**:

```
Phase 4.5: Marketing Optimizer → marketing_assets.md
Phase 5: Publisher Agent → WordPress publish
Phase 5.2: Content Repurposer (this skill) → 30+ social variations
Phase 5.5: Multi-Platform Distributor → auto-post to social
```

## Output Report

After processing, skill generates summary:

```markdown
✅ Content Repurposing Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: "Claude Code 完整開發指南" (2,450 words)

📦 Generated Content:
  ✓ Twitter Thread (15 tweets)
  ✓ Instagram Carousel (7 slides)
  ✓ LinkedIn Article (1,470 words)
  ✓ Short Posts (10 variations)
  ✓ Quote Cards (8 quotes)
  ✓ Video Scripts (3 x 60s)
  ✓ Email Newsletter (920 words)

📊 Content Stats:
  Total Pieces: 44
  Reach Multiplier: 30x
  Estimated Engagement: +400%

📁 Output Location:
  output/session_20251110_143022/repurposed_content/

⏭️ Next Steps:
  1. Review generated content
  2. Customize as needed
  3. Schedule with Multi-Platform Distributor
  4. Track performance in Analytics Reporter
```

---

**Skill Maintained By**: 喵哩文創 AI 寫手系統團隊
**Last Updated**: 2025-11-10
**Content Leverage**: 1 article → 30+ social posts
