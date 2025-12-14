# 🎨 自動化圖片生成系統

使用 Hugging Face API 完全自動生成文章所需的所有圖片。

## ⚡ 快速開始（3 分鐘）

### 步驟 1：取得 Hugging Face API Token

1. 前往 https://huggingface.co/settings/tokens
2. 登入或註冊（完全免費）
3. 點擊「New token」
4. 輸入名稱（如 `blog-image-gen`），選擇 **Read** 權限
5. 點擊「Generate」並複製 Token

### 步驟 2：執行腳本

```bash
# 在專案根目錄執行
python .claude/skills/image-generator/auto_generate_images.py
```

### 步驟 3：輸入 Token

首次執行時，腳本會要求你輸入 Token：

```
請輸入你的 Hugging Face API Token: hf_xxxxxxxxxxxxx
是否儲存 Token 到 ~/.claude/huggingface_token.txt? (y/N): y
```

輸入 `y` 儲存後，之後就不需要再輸入了！

### 步驟 4：選擇要生成的圖片

```
1. 全部生成（5 張）- 約需 5-10 分鐘
2. 只生成必要圖片（2 張）- 約需 2-3 分鐘
3. 自訂選擇

請選擇 (1-3):
```

建議選擇 **2**（必要圖片），包含：
- 封面圖片（Hero Image）
- Sub-agent 系統架構圖

### 步驟 5：等待生成

腳本會自動：
- ✅ 呼叫 Hugging Face API
- ✅ 生成高品質圖片
- ✅ 下載並儲存到 `output/session_xxx/images/`
- ✅ 詢問是否自動更新文章

完成！🎉

---

## 📖 詳細說明

### 使用的模型

預設使用 **FLUX.1-schnell**，這是 2024-2025 年最好的開源圖片生成模型之一：

- ✅ 品質極高（接近 Midjourney）
- ✅ 速度快（schnell = 德語「快速」）
- ✅ 完全免費使用

### 生成的圖片

| 圖片 | 檔名 | 優先度 | 用途 |
|------|------|--------|------|
| 封面圖 | `cover-claude-code-guide.webp` | ⭐⭐⭐ | 文章主視覺 |
| Sub-agent 架構 | `subagent-system-architecture.webp` | ⭐⭐⭐ | 核心功能說明 |
| 工具比較圖 | `tool-comparison-chart.webp` | ⭐⭐ | 幫助選擇 |
| 效率對比圖 | `efficiency-before-after.webp` | ⭐⭐ | 展示價值 |
| Claude.md 概念 | `claude-md-concept.webp` | ⭐ | 輔助理解 |

### 自動更新文章

腳本會自動將圖片插入到文章的正確位置：

```markdown
## Sub-agent 系統：Claude Code 的進階玩法

![Subagent Architecture](./images/subagent-system-architecture.webp)

Sub-agent 系統讓你可以...
```

生成的新文章會命名為 `final_article_with_images.md`。

---

## 🔧 進階設定

### 環境變數方式（推薦）

不想每次都輸入 Token？設定環境變數：

**macOS / Linux**：
```bash
# 編輯 ~/.zshrc 或 ~/.bashrc
export HUGGING_FACE_TOKEN="hf_xxxxxxxxxxxxx"

# 重新載入
source ~/.zshrc
```

**Windows**：
```powershell
# 設定使用者環境變數
setx HUGGING_FACE_TOKEN "hf_xxxxxxxxxxxxx"
```

### 切換模型

編輯腳本，將 `model='flux'` 改為：

```python
generator = ImageGenerator(api_token, model='sdxl')  # Stable Diffusion XL
generator = ImageGenerator(api_token, model='playground')  # Playground v2.5
```

### 自訂提示詞

修改圖片配置（在 `load_prompts()` 函數中）：

```python
{
    'name': 'my-custom-image',
    'filename': 'my-image.webp',
    'priority': 1,
    'prompt': 'Your custom prompt here...'
}
```

---

## 🐛 故障排除

### 問題 1：API 回傳 503 錯誤

**原因**：模型正在載入（冷啟動）

**解決**：腳本會自動等待並重試，請耐心等待 20-60 秒

### 問題 2：生成速度很慢

**原因**：免費 API 有速率限制

**解決**：
- 選擇「只生成必要圖片」（選項 2）
- 腳本已自動在每次生成間等待 3 秒

### 問題 3：圖片品質不滿意

**解決**：
1. 重新生成（選擇覆蓋）
2. 修改提示詞，加入「high quality, 4K, detailed」
3. 嘗試不同模型

### 問題 4：Token 無效

**檢查**：
- Token 是否正確複製（包含 `hf_` 前綴）
- Token 權限是否至少為 **Read**
- 是否過期（Hugging Face tokens 預設不過期）

---

## 💰 費用說明

### 完全免費 ✅

- Hugging Face Inference API：**完全免費**
- FLUX.1-schnell 模型：**開源免費**
- 無需信用卡
- 無隱藏費用

### 速率限制

免費帳號限制：
- 每分鐘約 100 次請求（足夠使用）
- 如果達到限制，腳本會自動等待

---

## 📊 與其他方案比較

| 方案 | 費用 | 速度 | 品質 | 自動化 |
|------|------|------|------|--------|
| **本腳本（Hugging Face）** | 🟢 免費 | 🟡 中等 | 🟢 高 | 🟢 完全 |
| DALL-E 3 | 🔴 $0.04/張 | 🟢 快 | 🟢 高 | 🟢 API |
| Midjourney | 🔴 $10/月 | 🟢 快 | 🟢 極高 | 🔴 無 API |
| Bing Creator | 🟢 免費 | 🟡 中等 | 🟢 高 | 🔴 手動 |
| Leonardo.ai | 🟡 限額 | 🟢 快 | 🟢 高 | 🟡 半自動 |

---

## 🔮 未來功能

- [ ] 支援更多模型（Stable Diffusion 3, SDXL Turbo）
- [ ] 圖片自動壓縮優化
- [ ] 批次編輯（添加文字、Logo）
- [ ] 直接上傳到 WordPress 媒體庫
- [ ] 生成多個變體供選擇

---

## 📚 相關資源

- [Hugging Face Inference API 文件](https://huggingface.co/docs/api-inference/)
- [FLUX.1 模型介紹](https://huggingface.co/black-forest-labs/FLUX.1-schnell)
- [圖片生成提示詞技巧](https://huggingface.co/docs/diffusers/using-diffusers/write_good_prompt)

---

## 🆘 需要幫助？

如果遇到問題：

1. 檢查上面的「故障排除」章節
2. 查看腳本輸出的錯誤訊息
3. 確認 Token 是否有效
4. 嘗試使用不同模型

---

**最後更新**: 2025-10-22
**版本**: 1.0.0
**作者**: WordPress AI 寫手系統
