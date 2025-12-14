# MCP Servers 配置指南

本指南幫助你配置所有已安裝的 Model Context Protocol (MCP) servers，包含 API 憑證申請和配置步驟。

**文件版本**: v2.1.0
**更新日期**: 2025-11-19
**系統版本**: v2.0.0+

---

## 📋 目錄

1. [已安裝的 MCP Servers](#已安裝的-mcp-servers)
2. [配置檔案位置](#配置檔案位置)
3. [逐步配置教學](#逐步配置教學)
   - [Notion MCP](#1-notion-mcp-✅-已配置)
   - [DataForSEO MCP](#2-dataforseo-mcp-⚠️-需配置)
   - [Supadata MCP](#3-supadata-mcp-⚠️-需配置)
   - [PlainSignal MCP](#4-plainsignal-mcp-⚠️-需配置)
   - [LinkedIn MCP](#5-linkedin-mcp-⚠️-需配置)
4. [測試連接](#測試連接)
5. [故障排除](#故障排除)

---

## 已安裝的 MCP Servers

| MCP Server | 狀態 | 用途 | Priority |
|-----------|------|------|----------|
| **Notion** | ✅ 已配置 | 內容管理、跨平台同步 | Optional |
| **DataForSEO** | ⚠️ 需配置 | SEO 研究、SERP 分析、關鍵字數據 | High |
| **Supadata** | ⚠️ 需配置 | 社群數據抓取 (YouTube, TikTok, X) | High |
| **PlainSignal** | ⚠️ 需配置 | 即時網站 Analytics 數據 | Medium |
| **LinkedIn** | ⚠️ 需配置 | LinkedIn 自動發布和數據 | Medium |

---

## 配置檔案位置

```bash
~/.config/claude-code/mcp.json
```

**當前配置結構**:
```json
{
  "mcpServers": {
    "notion": { ... },      // ✅ 已配置
    "dataforseo": { ... },  // ⚠️ 需 API credentials
    "supadata": { ... },    // ⚠️ 需 API credentials
    "plainsignal": { ... }, // ⚠️ 需 API credentials
    "linkedin": { ... }     // ⚠️ 需帳號密碼
  }
}
```

---

## 逐步配置教學

### 1. Notion MCP ✅ (已配置)

**狀態**: 已配置並運作中

**用途**:
- Phase 8.2: 同步文章 metadata 到 Notion
- Phase 10: 使用 Notion 作為數據儀表板（可選）

**已配置內容**:
```json
{
  "notion": {
    "command": "npx",
    "args": ["-y", "@notionhq/notion-mcp-server"],
    "env": {
      "NOTION_TOKEN": "ntn_***" // 已配置
    }
  }
}
```

**測試命令**:
```bash
claude mcp list
# 應顯示: notion: ✓ Connected
```

---

### 2. DataForSEO MCP ⚠️ (需配置)

**用途**:
- Phase 2a: 市場研究和熱門話題分析
- Phase 4a: 搜尋意圖分析和 SERP features
- Phase 4b: 關鍵字研究和競品分析

**價值**: 取代手動 SEO 研究，自動獲取真實 SERP 數據

#### 申請 API Credentials

1. **註冊帳號**
   - 訪問: https://dataforseo.com/
   - 點擊 "Sign Up" 創建免費帳號
   - 驗證 Email

2. **獲取 Credentials**
   - 登入後進入 Dashboard
   - 點擊 "API Access" 或 "Settings"
   - 複製你的 `Username` 和 `Password`

3. **定價** (參考)
   - 免費額度: 100 次查詢/月
   - Starter Plan: $20/月 (1,000 次查詢)
   - 只在使用時計費

#### 配置步驟

編輯 `~/.config/claude-code/mcp.json`:

```json
{
  "dataforseo": {
    "command": "npx",
    "args": ["-y", "dataforseo-mcp-server"],
    "env": {
      "DATAFORSEO_USERNAME": "your_actual_username",
      "DATAFORSEO_PASSWORD": "your_actual_password"
    }
  }
}
```

#### 測試連接

在 Claude Code 中執行：
```
請使用 DataForSEO MCP 查詢「AI 寫作工具」的 SERP 數據
```

預期結果：返回 Google 搜尋結果頁面的數據

---

### 3. Supadata MCP ⚠️ (需配置)

**用途**:
- Phase 2a: 社群媒體趨勢分析
- 抓取 YouTube、TikTok、Twitter/X 的熱門內容
- 分析影片 transcript 和互動數據

**價值**: 了解社群平台上的熱門話題和內容形式

#### 申請 API Key

1. **註冊帳號**
   - 訪問: https://supadata.ai/
   - 創建免費帳號

2. **獲取 API Key**
   - 進入 Dashboard
   - 點擊 "API Keys"
   - 創建新的 API Key
   - 複製並安全保存

3. **定價** (參考)
   - 免費額度: 50 次查詢/月
   - Basic Plan: $15/月 (500 次查詢)

#### 配置步驟

編輯 `~/.config/claude-code/mcp.json`:

```json
{
  "supadata": {
    "command": "npx",
    "args": ["-y", "@supadata/mcp"],
    "env": {
      "SUPADATA_API_KEY": "your_api_key_here"
    }
  }
}
```

#### 測試連接

```
請使用 Supadata MCP 抓取這個 YouTube 影片的 transcript：https://youtube.com/watch?v=XXXXX
```

---

### 4. PlainSignal MCP ⚠️ (需配置)

**用途**:
- Phase 7: 補充 Google Analytics，提供更多數據來源
- Phase 10: 整合多個 analytics 數據源

**價值**: 即時網站 analytics 數據，無需等待 GA 處理時間

#### 申請 Token

1. **註冊帳號**
   - 訪問: https://plainsignal.com/
   - 創建帳號

2. **獲取 Token**
   - 進入 Settings → API
   - 創建新的 API Token
   - 複製 Token

3. **安裝追蹤碼**
   - 複製 PlainSignal 提供的 JavaScript 追蹤碼
   - 加入到你的 WordPress 網站 `<head>` 中
   - 或使用 WordPress 插件

4. **定價** (參考)
   - 免費額度: 10,000 pageviews/月
   - Pro Plan: $19/月 (100,000 pageviews)

#### 配置步驟

編輯 `~/.config/claude-code/mcp.json`:

```json
{
  "plainsignal": {
    "command": "npx",
    "args": ["-y", "@plainsignal/plainsignal-mcp"],
    "env": {
      "PLAINSIGNAL_TOKEN": "your_token_here"
    }
  }
}
```

#### 測試連接

```
請使用 PlainSignal MCP 獲取我網站過去 7 天的流量數據
```

---

### 5. LinkedIn MCP ⚠️ (需配置)

**用途**:
- Phase 8.1: 自動發布到 LinkedIn
- 讀取 LinkedIn feeds 和 job API

**價值**: 擴展多平台發布能力，觸及專業受眾

#### 配置方式

**重要安全提示**: LinkedIn 帳號密碼是敏感資訊，請確保：
- 使用應用專用密碼（如 LinkedIn 提供）
- 定期更換密碼
- 考慮創建專用的 LinkedIn 帳號用於自動化

#### 配置步驟

編輯 `~/.config/claude-code/mcp.json`:

```json
{
  "linkedin": {
    "command": "npx",
    "args": ["-y", "@adhikasp/mcp-linkedin"],
    "env": {
      "LINKEDIN_USERNAME": "your_linkedin_email@example.com",
      "LINKEDIN_PASSWORD": "your_password_or_app_password"
    }
  }
}
```

**替代方案**: 如果不想使用帳號密碼，可以：
1. 暫時跳過 LinkedIn MCP
2. 使用 Phase 5.2 生成的內容手動發布到 LinkedIn
3. 等待 LinkedIn 官方 API 支援

#### 測試連接

```
請使用 LinkedIn MCP 讀取我的最新 3 則 feeds
```

---

## 測試連接

### 方法 1: 使用 CLI 命令

```bash
# 列出所有 MCP servers 和連接狀態
claude mcp list

# 測試特定 server
claude mcp get dataforseo
claude mcp get supadata
claude mcp get plainsignal
claude mcp get linkedin
```

**預期輸出**:
```
notion: ✓ Connected
dataforseo: ✓ Connected (或 ✗ Failed to connect)
supadata: ✓ Connected
plainsignal: ✓ Connected
linkedin: ✓ Connected
```

### 方法 2: 在 Claude Code 中測試

依次在對話中執行：

```
1. 請用 DataForSEO MCP 查詢「部落格寫作」的關鍵字數據
2. 請用 Supadata MCP 分析這個 YouTube 影片：https://youtube.com/watch?v=xxxxx
3. 請用 PlainSignal MCP 顯示我網站過去 7 天的數據
4. 請用 LinkedIn MCP 讀取我的 LinkedIn profile
```

---

## 故障排除

### 問題 1: MCP server 顯示 "Failed to connect"

**可能原因**:
- API credentials 錯誤
- 網路連接問題
- npm 套件未正確安裝

**解決方案**:
```bash
# 1. 檢查配置檔案
cat ~/.config/claude-code/mcp.json

# 2. 手動測試 npm 套件
npx -y dataforseo-mcp-server

# 3. 檢查網路連接
curl -I https://api.dataforseo.com

# 4. 重啟 Claude Code
```

### 問題 2: API 配額用完

**症狀**: 返回 "Quota exceeded" 或 "Rate limit" 錯誤

**解決方案**:
- 檢查你的 API 使用量
- 升級到付費方案
- 暫時停用該 MCP，使用降級方案

### 問題 3: 配置檔案格式錯誤

**症狀**: 所有 MCP 都無法連接

**解決方案**:
```bash
# 驗證 JSON 格式
cat ~/.config/claude-code/mcp.json | python3 -m json.tool

# 如果格式錯誤，恢復備份
cp ~/.config/claude-code/mcp.json.backup ~/.config/claude-code/mcp.json
```

### 問題 4: LinkedIn 登入失敗

**可能原因**:
- LinkedIn 檢測到自動化行為
- 需要兩步驟驗證
- 帳號密碼錯誤

**解決方案**:
- 關閉 LinkedIn 兩步驟驗證（暫時）
- 使用應用專用密碼
- 考慮手動發布到 LinkedIn

---

## 配置檢查清單

安裝完成後，確認以下項目：

### MCP Servers 狀態
- [ ] Notion MCP: ✓ Connected
- [ ] DataForSEO MCP: ✓ Connected 或已獲取 credentials
- [ ] Supadata MCP: ✓ Connected 或已獲取 API key
- [ ] PlainSignal MCP: ✓ Connected 或已安裝追蹤碼
- [ ] LinkedIn MCP: ✓ Connected 或選擇跳過

### 功能測試
- [ ] 可以用 DataForSEO 查詢 SERP 數據
- [ ] 可以用 Supadata 抓取社群內容
- [ ] 可以用 PlainSignal 讀取 analytics
- [ ] 可以用 LinkedIn MCP 讀取 feeds（如已配置）

### 文件更新
- [ ] `CLAUDE.md` 已更新提及新 MCP
- [ ] `blog-manager-v2.0.0.md` 已更新 Phase 7-10
- [ ] 本配置指南已完成

---

## 優先級建議

如果你不想一次配置所有 MCP，建議按以下優先級：

### 🔴 最高優先級 (立即配置)
1. **DataForSEO** - SEO 研究是核心功能，影響 Phase 2a 和 Phase 4

### 🟡 中優先級 (本週內)
2. **Supadata** - 社群趨勢分析能提升內容品質
3. **PlainSignal** - 補充 Analytics 數據，提供更完整視圖

### 🟢 低優先級 (可選)
4. **LinkedIn** - 如果你的目標受眾在 LinkedIn 上才需要

---

## 降級方案

如果某個 MCP 無法配置，系統會自動降級：

| MCP 失敗 | 降級方案 | 影響 |
|---------|---------|------|
| DataForSEO | 使用 Google Search + 手動分析 | Phase 2a/4 需要更多時間 |
| Supadata | 手動訪問社群平台 | Phase 2a 趨勢分析受限 |
| PlainSignal | 只使用 Google Analytics | Phase 7 數據來源較少 |
| LinkedIn | 手動複製貼上發布 | Phase 8 需要手動操作 |

---

## 安全性建議

### API Credentials 管理

1. **不要提交到 Git**
   - `~/.config/claude-code/mcp.json` 不在 Git 倉庫中
   - 確認 `.gitignore` 包含所有 credential 檔案

2. **定期更換密碼**
   - 每 3-6 個月更換一次 API keys
   - LinkedIn 密碼每月更換

3. **備份配置**
   ```bash
   cp ~/.config/claude-code/mcp.json ~/.config/claude-code/mcp.json.backup
   ```

4. **最小權限原則**
   - API keys 只授予必要的權限
   - 考慮使用只讀 API keys（如可用）

---

## 相關資源

### 官方文件
- [DataForSEO API Docs](https://docs.dataforseo.com/)
- [Supadata API Docs](https://docs.supadata.ai/)
- [PlainSignal API Docs](https://docs.plainsignal.com/)
- [LinkedIn API](https://docs.microsoft.com/linkedin/)

### MCP 相關
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Awesome MCP Servers](https://github.com/wong2/awesome-mcp-servers)

### 系統文件
- `CLAUDE.md` - 系統完整說明
- `blog-manager-v2.0.0.md` - Agent 工作流程
- `MCP_SETUP_GUIDE.md` - 原始 MCP 設定指南（如存在）

---

**下一步**: 配置完成後，回到 [CLAUDE.md](../CLAUDE.md) 繼續使用系統。

**支援**: 如有問題，請參考 [故障排除](#故障排除) 或查看系統 Issues。

---

**文件版本**: v2.1.0
**維護**: 喵哩文創 AI 寫手系統團隊
**最後更新**: 2025-11-19
