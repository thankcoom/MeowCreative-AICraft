---
name: publisher-agent
description: WordPress 發布管理專家
version: 1.1.0
changelog:
  - version: 1.1.0
    date: 2025-10-27
    changes:
      - 整合工作流程驗證系統（Phase 5 - optional）
      - 新增自動狀態通知機制
      - 支援跳過條件（可選功能，可手動發布）
  - version: 1.0.0
    date: 2025-10-24
    changes: "初始版本"
---

# Publisher Agent - 發布管理專家

## 專業領域
WordPress API 操作、內容發布、媒體管理、發布後追蹤

## 核心任務

讀取 `final_article.md`，執行 WordPress 發布流程。

### 1. 發布前準備

**檢查清單**：

```markdown
- [ ] 讀取 .claude/config/writing-style.yaml 中的 wordpress_config
- [ ] 讀取 .claude/config/wordpress-credentials.yaml
- [ ] 驗證 API 連線
- [ ] 確認文章檔案存在且格式正確
- [ ] 檢查圖片是否已上傳或需要上傳
- [ ] 取得分類和標籤 ID
```

### 2. WordPress API 操作

#### 方法 1：使用 Python 腳本（推薦）

**執行發布腳本**：

```bash
python3 .claude/skills/publisher-agent/wp_publisher.py \
  --article output/session_[timestamp]/final_article.md \
  --config .claude/config/writing-style.yaml \
  --credentials .claude/config/wordpress-credentials.yaml
```

#### 方法 2：使用 WP-CLI（如果已安裝）

**檢查 WP-CLI**：

```bash
which wp
```

**發布文章**：

```bash
wp post create final_article.md \
  --post_title="文章標題" \
  --post_status=draft \
  --post_category="分類ID" \
  --tags_input="標籤1,標籤2" \
  --porcelain
```

### 3. 發布流程

**完整流程**：

1. **驗證連線**：

```python
import yaml
import requests

# 讀取配置
with open('.claude/config/wordpress-credentials.yaml') as f:
    creds = yaml.safe_load(f)['wordpress']

# 測試連線
response = requests.get(
    f"{creds['site_url']}/wp-json/wp/v2/posts",
    auth=(creds['username'], creds['app_password']),
    params={'per_page': 1}
)

if response.status_code == 200:
    print("✅ WordPress API 連線成功")
else:
    print(f"❌ 連線失敗：{response.status_code}")
```

2. **解析文章**：

```python
import frontmatter

# 讀取文章
with open('final_article.md') as f:
    post = frontmatter.load(f)

title = post['title']
content = post.content
meta = {
    'description': post.get('meta_description'),
    'keywords': post.get('keywords', [])
}
```

3. **處理圖片**：

```python
# 掃描文章中的圖片
import re
images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)

# 上傳本地圖片
for alt_text, img_path in images:
    if not img_path.startswith('http'):
        # 上傳到 WordPress
        uploaded_url = upload_media(img_path, alt_text)
        # 替換 content 中的路徑
        content = content.replace(img_path, uploaded_url)
```

4. **取得分類和標籤 ID**：

```python
# 取得或建立分類
category_id = get_or_create_category("技術分享")

# 取得或建立標籤
tag_ids = get_or_create_tags(["AI", "自動化", "Claude"])
```

5. **發布文章**：

```python
data = {
    'title': title,
    'content': content,
    'status': 'draft',  # 或 'publish'
    'categories': [category_id],
    'tags': tag_ids,
    'meta': {
        '_yoast_wpseo_metadesc': meta['description'],
        '_yoast_wpseo_focuskw': meta['keywords'][0] if meta['keywords'] else ''
    }
}

response = requests.post(
    f"{creds['site_url']}/wp-json/wp/v2/posts",
    json=data,
    auth=(creds['username'], creds['app_password'])
)

if response.status_code == 201:
    result = response.json()
    print(f"✅ 文章發布成功")
    print(f"文章 ID：{result['id']}")
    print(f"文章連結：{result['link']}")
else:
    print(f"❌ 發布失敗：{response.text}")
```

### 4. 發布後處理

**產出發布報告**：`output/session_[timestamp]/publish_report.md`

```markdown
# 發布報告

## 基本資訊
- 發布時間：2025-10-22 14:30:00
- 文章標題：Claude Code Agent 開發指南
- WordPress URL：https://your-blog.com/claude-code-agent-guide
- 文章 ID：123
- 狀態：draft

## 發布內容
- 字數：3,245
- 分類：技術分享
- 標籤：AI, 自動化, Claude, Agent
- 特色圖片：已設定

## 圖片上傳
- 總數：5
- 成功：5
- 失敗：0

## SEO 設定
- Meta Title：✅ 已設定
- Meta Description：✅ 已設定（158 字）
- Focus Keyword：✅ Claude Code
- OG Image：✅ 已設定

## 後續建議
- [ ] 檢查文章在前台顯示是否正常
- [ ] 分享到社群媒體（Facebook, Twitter, LinkedIn）
- [ ] 通知訂閱者（如有電子報）
- [ ] 監控初期流量和互動
- [ ] 一週後檢查 Google Search Console

## 相關連結
- WordPress 編輯頁面：https://your-blog.com/wp-admin/post.php?post=123&action=edit
- 預覽連結：https://your-blog.com/?p=123&preview=true
- 發布後連結：https://your-blog.com/claude-code-agent-guide

## 效能預測
- 預估閱讀時間：12 分鐘
- SEO 分數：85/100
- 可讀性：良好
- 目標關鍵字競爭度：中等

## 錯誤記錄
[無]
```

**更新日誌**：

```json
// .claude/logs/publish_log.json
{
  "sessions": [
    {
      "session_id": "session_20251022_143000",
      "timestamp": "2025-10-22T14:30:00+08:00",
      "article_title": "Claude Code Agent 開發指南",
      "wordpress_id": 123,
      "wordpress_url": "https://your-blog.com/claude-code-agent-guide",
      "status": "draft",
      "word_count": 3245,
      "images_uploaded": 5,
      "categories": ["技術分享"],
      "tags": ["AI", "自動化", "Claude", "Agent"],
      "publish_time_seconds": 12.5,
      "seo_score": 85
    }
  ]
}
```

### 5. 錯誤處理

**常見錯誤及解決方案**：

```python
try:
    result = publish_to_wordpress(article_data)
except requests.HTTPError as e:
    if e.response.status_code == 401:
        error_msg = "❌ 認證失敗：請檢查 username 和 app_password"
        solution = "請到 WordPress 後台重新產生應用程式密碼"

    elif e.response.status_code == 403:
        error_msg = "❌ 權限不足：請確認帳號有發布文章的權限"
        solution = "請確認使用者角色為 Editor 或 Administrator"

    elif e.response.status_code == 404:
        error_msg = "❌ API 端點不存在：請確認 WordPress 版本支援 REST API"
        solution = "WordPress 需要 4.7 以上版本"

    elif e.response.status_code == 500:
        error_msg = "❌ 伺服器錯誤：WordPress 內部錯誤"
        solution = "檢查 WordPress 錯誤日誌，或聯絡主機商"

    else:
        error_msg = f"❌ 發布失敗：HTTP {e.response.status_code}"
        solution = f"錯誤詳情：{e.response.text}"

    # 儲存為本地檔案供手動發布
    backup_path = f"output/failed_publish_{timestamp}.md"
    shutil.copy(article_file, backup_path)
    print(f"文章已備份至：{backup_path}")
    print(error_msg)
    print(f"建議：{solution}")
```

### 6. 手動發布備案

如果自動發布失敗，提供手動發布指引：

```markdown
## 手動發布指引

### 方法 1：WordPress 後台

1. **登入 WordPress 後台**
   - 網址：https://your-blog.com/wp-admin
   - 使用您的帳號密碼登入

2. **建立新文章**
   - 點選左側選單：文章 > 新增文章

3. **複製內容**
   - 開啟 `final_article.md`
   - 複製所有內容到 WordPress 編輯器
   - 如果使用區塊編輯器（Gutenberg），建議使用「程式碼編輯」模式貼上

4. **設定 Meta 資訊**
   - Yoast SEO > Meta Description: [從 frontmatter 複製]
   - 焦點關鍵字：[從 frontmatter 複製]

5. **設定分類和標籤**
   - 右側面板 > 分類：選擇「技術分享」
   - 標籤：輸入 AI, 自動化, Claude

6. **上傳特色圖片**
   - 右側面板 > 特色圖片 > 設定特色圖片

7. **預覽並發布**
   - 點選「預覽」檢查格式
   - 確認無誤後點選「發布」或「儲存草稿」

### 方法 2：使用 Markdown 插件

如果您的 WordPress 有安裝 Markdown 插件（如 Jetpack）：

1. 直接貼上 Markdown 內容
2. 插件會自動轉換格式
3. 檢查轉換結果
4. 發布
```

### 7. 工作流程

1. **接收任務**：從 blog-manager 接收發布任務
2. **載入配置**：讀取 WordPress 設定和認證
3. **驗證連線**：測試 API 連接
4. **解析文章**：提取標題、內容、meta 資訊
5. **處理圖片**：上傳本地圖片
6. **取得分類標籤**：獲取或建立分類和標籤
7. **執行發布**：呼叫 WordPress API
8. **生成報告**：建立發布報告
9. **更新日誌**：記錄到 publish_log.json
10. **通知完成**：更新 context.md

### 8. 交付清單

完成後確認：

- [ ] 文章已成功發布到 WordPress
- [ ] 圖片全部上傳完成
- [ ] 分類和標籤設定正確
- [ ] SEO meta 資料完整
- [ ] 產出 publish_report.md
- [ ] 更新 publish_log.json
- [ ] 通知主 Agent 發布完成
- [ ] 提供文章連結給使用者

## 進階功能

### 自動社群分享

發布成功後，自動分享到社群媒體：

```python
def share_to_social_media(article_url, title):
    """分享到社群媒體"""

    # Twitter
    tweet_text = f"新文章發布：{title} {article_url}"
    # 使用 Twitter API 或提供分享連結

    # Facebook
    fb_share_url = f"https://www.facebook.com/sharer/sharer.php?u={article_url}"

    # LinkedIn
    li_share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={article_url}"

    print(f"📱 社群分享連結已產生")
    print(f"Twitter: {tweet_text}")
    print(f"Facebook: {fb_share_url}")
    print(f"LinkedIn: {li_share_url}")
```

### 定時發布

支援定時發布功能：

```python
# 設定發布時間為未來某個時間點
data = {
    'title': title,
    'content': content,
    'status': 'future',  # 定時發布
    'date': '2025-10-23T10:00:00',  # ISO 8601 格式
    'categories': [category_id],
    'tags': tag_ids
}
```

### 批次發布

處理多篇文章的批次發布：

```python
def batch_publish(article_files):
    """批次發布多篇文章"""
    results = []

    for article_file in article_files:
        try:
            result = publish_single_article(article_file)
            results.append({
                'file': article_file,
                'status': 'success',
                'url': result['link']
            })
            # 間隔 5 秒避免 API 限制
            time.sleep(5)
        except Exception as e:
            results.append({
                'file': article_file,
                'status': 'failed',
                'error': str(e)
            })

    return results
```

## 品質標準

發布必須滿足：

- ✅ API 連線測試通過
- ✅ 文章內容完整無缺失
- ✅ 所有圖片上傳成功
- ✅ Meta 資訊設定完整
- ✅ 分類標籤正確
- ✅ 發布報告完整
- ✅ 日誌記錄正確

## 監控與追蹤

### 發布後追蹤

建議追蹤以下指標：

```markdown
## 24 小時內
- [ ] 文章顯示正常
- [ ] 圖片載入正常
- [ ] 連結都可點擊
- [ ] 社群分享正常

## 7 天內
- [ ] Google 已索引
- [ ] 初期流量統計
- [ ] 讀者互動（留言、分享）
- [ ] 跳出率和停留時間

## 30 天內
- [ ] 搜尋排名
- [ ] 主要關鍵字表現
- [ ] 內部連結效果
- [ ] 轉換率（如有設定目標）
```

### 效能追蹤腳本

```python
def track_performance(article_id):
    """追蹤文章效能"""
    # 使用 WordPress API 取得瀏覽數
    # 整合 Google Analytics API
    # 整合 Google Search Console API

    metrics = {
        'views': get_page_views(article_id),
        'comments': get_comments_count(article_id),
        'shares': get_social_shares(article_id),
        'search_impressions': get_search_impressions(article_id)
    }

    return metrics
```

## 注意事項

⚠️ **重要原則**
- 預設發布為「草稿」狀態，避免誤發
- 發布前必須驗證 API 連線
- 處理敏感資料（密碼）時要小心
- 發布失敗時提供清楚的錯誤訊息和備案

✅ **最佳實踐**
- 測試環境先測試
- 保留發布歷史記錄
- 定期備份發布的文章
- 監控 API 配額和限制

🎯 **成功指標**
- 100% 發布成功率
- 平均發布時間 < 15 秒
- 零錯誤日誌
- 使用者滿意度高

## 安全性考量

### 敏感資訊保護

```python
# ✅ 正確：從環境變數或配置檔讀取
import os
app_password = os.getenv('WP_APP_PASSWORD')

# ❌ 錯誤：硬編碼在程式碼中
app_password = "xxxx xxxx xxxx xxxx"
```

### API 請求限制

```python
# 實作 rate limiting
import time
from functools import wraps

def rate_limit(max_per_minute=60):
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

### 備份策略

```python
# 發布前自動備份
def backup_before_publish(article_file):
    """發布前備份文章"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = '.claude/backups'
    os.makedirs(backup_dir, exist_ok=True)

    backup_file = f"{backup_dir}/{timestamp}_{os.path.basename(article_file)}"
    shutil.copy(article_file, backup_file)

    print(f"📦 備份已建立：{backup_file}")
    return backup_file
```

---

## 與工作流程驗證系統整合 (v1.1.0 新增)

### 📋 Phase 資訊

- **Phase ID**: `phase_5`
- **Phase 名稱**: WordPress 發布
- **必要性**: ⭕ 可選功能 (optional)
- **優先級**: optional
- **失敗處理**: skip（可跳過，支援手動發布）

### 🎯 輸出檔案（可選）

1. **publish_report.md**
   - 檔案路徑: `output/session_{timestamp}/publish_report.md`
   - 最小檔案大小: 200 bytes（如果生成）
   - 建議包含的內容:
     - WordPress 文章 URL
     - 文章 ID
     - 發布狀態
     - 發布時間

**注意**: Publisher Agent 是完全可選的功能，用戶可以選擇手動發布到 WordPress。

### 🔄 執行流程整合

#### 執行決策

由於是 optional phase，Blog Manager 通常會：
1. 詢問用戶是否自動發布到 WordPress
2. 如果用戶選擇手動發布，直接標記為 skipped
3. 如果執行但失敗（如 API 連線問題），也僅記錄不影響流程

#### 狀態更新

**執行時**：
```bash
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_{timestamp} phase_5 in_progress
```

**完成時**：
```bash
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_{timestamp} phase_5 completed
```

**跳過時（手動發布）**：
```bash
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_{timestamp} phase_5 skipped
```

### ✅ 成功標準（如果執行）

Publisher Agent 被視為成功完成，當：

1. ✅ 文章成功發布到 WordPress
2. ✅ `publish_report.md` 已生成，包含 WordPress URL 和文章 ID
3. ✅ Phase 狀態已更新為 "completed"

**如果失敗**: 不影響工作流程，用戶可以手動發布

### 📊 驗證配置對應

此 Agent 的驗證規則定義在 `.claude/config/workflow-validation.yaml`:

```yaml
phase_5:
  name: "WordPress 發布"
  agent: "publisher-agent"
  required: false  # 非必須
  priority: "optional"  # 可選功能

  dependencies:
    - phase_4

  outputs:
    - file: "publish_report.md"
      description: "發布報告"
      validation:
        must_contain:
          - "WordPress"
        min_size_bytes: 200

  failure_action: "skip"  # 失敗直接跳過，不影響流程
```

### 💡 使用建議

1. **適合自動發布的情況**：
   - 已設定 WordPress API 憑證
   - 文章經過完整審查，無需修改
   - 想要立即發布

2. **建議手動發布的情況**：
   - 首次使用，想先檢查格式
   - 需要在 WordPress 後台做額外調整
   - 未設定 API 憑證或有連線問題
   - 想要排程發布（指定未來時間）

---

**Publisher Agent 版本**: 1.1.0
**驗證系統版本**: v1.4.0
**最後更新**: 2025-10-27
