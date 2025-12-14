---
name: wordpress-publisher
description: Publish articles to WordPress sites using REST API. Use when ready to publish final blog posts, update existing articles, or manage WordPress content including categories, tags, and featured images.
license: MIT
version: 1.0.0
allowed-tools:
  - bash
  - read
  - write
---

# WordPress Publisher Skill

Automates WordPress article publishing using the WordPress REST API. Handles Markdown to WordPress conversion, category/tag management, and featured image uploads.

## When to Use This Skill

Invoke this skill when you need to:
- Publish final articles to WordPress blog
- Update existing WordPress posts
- Manage post categories and tags
- Upload and set featured images
- Configure SEO metadata (Yoast/RankMath)
- Schedule posts for future publication

## Prerequisites

1. **WordPress Site Requirements**:
   - WordPress REST API enabled (default in WP 4.7+)
   - Application Password or OAuth token configured
   - Appropriate user permissions (Editor or Administrator)

2. **Configuration File**:
   - `.claude/config/wordpress-credentials.yaml` must exist
   - Contains site URL, username, and app password

3. **Python Dependencies**:
   ```bash
   pip install requests pyyaml markdown python-frontmatter
   ```

## Configuration

The skill requires a credentials file at:
`.claude/config/wordpress-credentials.yaml`

**Example Structure**:
```yaml
site_url: "https://yourblog.com"
username: "your-username"
app_password: "xxxx xxxx xxxx xxxx xxxx xxxx"
default_status: "draft"  # or "publish"
default_category: "未分類"
author_id: 1
```

### How to Get Application Password

1. Go to WordPress Admin → Users → Profile
2. Scroll to "Application Passwords"
3. Enter name (e.g., "Claude Code Publisher")
4. Click "Add New Application Password"
5. Copy the generated password (spaces included)
6. Save to credentials file

## Usage Workflow

### Standard Publishing Flow

1. **Prepare Article**:
   - Ensure article is in Markdown format
   - Include frontmatter for metadata (optional)
   - Location: `output/session_YYYYMMDD_HHMMSS/final_article.md`

2. **Invoke Skill**:
   ```
   User: "請發布這篇文章到 WordPress"
   Claude: [Activates wordpress-publisher skill]
   ```

3. **Skill Actions**:
   - Reads article content
   - Converts Markdown to WordPress HTML blocks
   - Extracts metadata from frontmatter or seo_report.md
   - Uploads featured image (if provided)
   - Creates/updates WordPress post
   - Returns post URL and status

### Advanced Options

**Custom Categories and Tags**:
```
User: "發布到 WordPress，分類為「AI 開發」，標籤為「Claude Code, 自動化, Python」"
```

**Schedule Publication**:
```
User: "排程這篇文章在明天早上 8:00 發布"
```

**Update Existing Post**:
```
User: "更新 WordPress 文章 ID 123 的內容"
```

## Implementation Details

### Step 1: Load Configuration

```python
import yaml
from pathlib import Path

config_path = Path.home() / '.claude/config/wordpress-credentials.yaml'
with open(config_path) as f:
    config = yaml.safe_load(f)
```

### Step 2: Process Article

1. **Read Markdown**:
   ```python
   import frontmatter

   with open(article_path) as f:
       post = frontmatter.load(f)

   title = post.get('title', 'Untitled')
   content = post.content
   categories = post.get('categories', [])
   tags = post.get('tags', [])
   ```

2. **Convert to HTML**:
   ```python
   import markdown

   html_content = markdown.markdown(
       content,
       extensions=['fenced_code', 'tables', 'toc']
   )
   ```

### Step 3: Upload to WordPress

```python
import requests
from requests.auth import HTTPBasicAuth

url = f"{config['site_url']}/wp-json/wp/v2/posts"

data = {
    'title': title,
    'content': html_content,
    'status': config.get('default_status', 'draft'),
    'categories': get_category_ids(categories),
    'tags': get_tag_ids(tags),
    'author': config['author_id']
}

response = requests.post(
    url,
    json=data,
    auth=HTTPBasicAuth(config['username'], config['app_password'])
)

if response.status_code == 201:
    post_data = response.json()
    print(f"✅ Published: {post_data['link']}")
    print(f"📝 Post ID: {post_data['id']}")
else:
    print(f"❌ Error: {response.text}")
```

### Step 4: Handle Featured Image

```python
def upload_featured_image(image_path, post_id):
    """Upload image and set as post thumbnail"""
    media_url = f"{config['site_url']}/wp-json/wp/v2/media"

    with open(image_path, 'rb') as img:
        files = {'file': img}
        headers = {'Content-Disposition': f'attachment; filename={Path(image_path).name}'}

        response = requests.post(
            media_url,
            files=files,
            headers=headers,
            auth=HTTPBasicAuth(config['username'], config['app_password'])
        )

    if response.status_code == 201:
        media_id = response.json()['id']

        # Set as featured image
        post_url = f"{config['site_url']}/wp-json/wp/v2/posts/{post_id}"
        requests.post(
            post_url,
            json={'featured_media': media_id},
            auth=HTTPBasicAuth(config['username'], config['app_password'])
        )

        return media_id
```

## Category and Tag Management

### Get or Create Category

```python
def get_or_create_category(name):
    """Get category ID or create if doesn't exist"""
    # Search existing
    search_url = f"{config['site_url']}/wp-json/wp/v2/categories?search={name}"
    response = requests.get(search_url)

    if response.json():
        return response.json()[0]['id']

    # Create new
    create_url = f"{config['site_url']}/wp-json/wp/v2/categories"
    response = requests.post(
        create_url,
        json={'name': name},
        auth=HTTPBasicAuth(config['username'], config['app_password'])
    )

    return response.json()['id']
```

### Get or Create Tag

```python
def get_or_create_tag(name):
    """Get tag ID or create if doesn't exist"""
    search_url = f"{config['site_url']}/wp-json/wp/v2/tags?search={name}"
    response = requests.get(search_url)

    if response.json():
        return response.json()[0]['id']

    create_url = f"{config['site_url']}/wp-json/wp/v2/tags"
    response = requests.post(
        create_url,
        json={'name': name},
        auth=HTTPBasicAuth(config['username'], config['app_password'])
    )

    return response.json()['id']
```

## SEO Integration

### Set Yoast SEO Metadata

```python
def set_yoast_meta(post_id, meta_title, meta_description, focus_keyword):
    """Set Yoast SEO fields via REST API"""
    url = f"{config['site_url']}/wp-json/wp/v2/posts/{post_id}"

    data = {
        'yoast_meta': {
            'yoast_wpseo_title': meta_title,
            'yoast_wpseo_metadesc': meta_description,
            'yoast_wpseo_focuskw': focus_keyword
        }
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(config['username'], config['app_password'])
    )
```

## Error Handling

### Common Issues and Solutions

**1. Authentication Failed (401)**
```
Error: {"code":"rest_forbidden","message":"Sorry, you are not allowed to create posts as this user."}

Solution:
- Verify username is correct
- Regenerate Application Password
- Check user has Editor/Administrator role
```

**2. Invalid Categories (400)**
```
Error: {"code":"rest_invalid_param","message":"Invalid parameter(s): categories"}

Solution:
- Categories must be IDs, not names
- Use get_or_create_category() to get valid IDs
```

**3. Image Upload Failed (413)**
```
Error: Request Entity Too Large

Solution:
- Resize image before upload
- Check WordPress max upload size (php.ini)
- Use image optimization before upload
```

## Best Practices

### 1. Always Draft First
```python
# Default to draft, then review before publishing
'status': 'draft'

# After review, update to publish
update_post_status(post_id, 'publish')
```

### 2. Preserve Formatting
```python
# Use Gutenberg blocks for better compatibility
html_content = convert_to_gutenberg_blocks(markdown_content)
```

### 3. Validate Before Upload
```python
# Check required fields
assert title, "Title is required"
assert content, "Content is required"
assert len(content) > 300, "Content too short"
```

### 4. Log All Actions
```python
import logging

logging.info(f"Publishing to {config['site_url']}")
logging.info(f"Title: {title}")
logging.info(f"Categories: {categories}")
logging.info(f"Status: {response.status_code}")
```

## Output Format

After successful publication, skill returns:

```yaml
✅ WordPress Publishing Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: "Claude Code 完整開發指南"
Post URL: https://yourblog.com/claude-code-guide/
Post ID: 42
Status: draft
Categories: AI 開發 (ID: 3)
Tags: Claude Code, 自動化, Python
Featured Image: ✅ Uploaded (Media ID: 156)

📊 Statistics:
- Word Count: 2,450
- Estimated Reading Time: 10 minutes
- Images: 1
- Code Blocks: 5

⏭️ Next Steps:
1. Review post at: https://yourblog.com/wp-admin/post.php?post=42&action=edit
2. Preview: https://yourblog.com/?p=42&preview=true
3. Publish when ready: Update status to "publish"
```

## Integration with Blog Manager

This skill is designed to work seamlessly with the Blog Manager workflow:

```
Phase 4: SEO Optimizer → generates seo_report.md
Phase 4.5: Marketing Optimizer → generates marketing_assets.md
Phase 5: WordPress Publisher (this skill) → publishes to WordPress
```

**Automatic Metadata Extraction**:
- Reads `seo_report.md` for meta title/description
- Uses recommended title from SEO Optimizer
- Extracts categories/tags from analysis
- Pulls featured image suggestion from Marketing Optimizer

## Troubleshooting

### Debug Mode

Set verbose logging to diagnose issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Connection

Before publishing, test API connection:

```python
test_url = f"{config['site_url']}/wp-json/wp/v2/posts?per_page=1"
response = requests.get(
    test_url,
    auth=HTTPBasicAuth(config['username'], config['app_password'])
)

if response.status_code == 200:
    print("✅ Connection successful")
else:
    print(f"❌ Connection failed: {response.status_code}")
```

## Security Notes

- **Never commit credentials to git**
- Store `wordpress-credentials.yaml` in `.gitignore`
- Use Application Passwords (not main password)
- Rotate passwords regularly
- Use HTTPS for WordPress site

## Version History

- **1.0.0** (2025-11-10): Initial release
  - Basic publish/update functionality
  - Category/tag management
  - Featured image upload
  - SEO metadata support

---

**Skill Maintained By**: 喵哩文創 AI 寫手系統團隊
**Last Updated**: 2025-11-10
**Dependencies**: Python 3.9+, WordPress 5.0+, REST API enabled
