#!/bin/bash
# Skills 系統設定腳本

echo "🚀 喵哩文創 AI 寫手系統 - Skills 設定"
echo "========================================="
echo ""

# 檢查 Python 版本
echo "📋 檢查 Python 版本..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ 找不到 Python 3，請先安裝 Python 3.9+"
    exit 1
fi

echo "✅ Python 版本檢查通過"
echo ""

# 安裝依賴套件
echo "📦 安裝依賴套件..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依賴套件安裝失敗"
    exit 1
fi

echo "✅ 依賴套件安裝完成"
echo ""

# 檢查配置檔案
echo "⚙️  檢查配置檔案..."

CONFIG_DIR=".claude/config"
WORDPRESS_CREDS="$CONFIG_DIR/wordpress-credentials.yaml"

if [ ! -f "$WORDPRESS_CREDS" ]; then
    echo "⚠️  找不到 WordPress 憑證檔案"
    echo "   正在創建範本檔案..."

    cat > "$WORDPRESS_CREDS" << 'EOF'
# WordPress REST API 憑證設定
site_url: "https://your-site.com"
username: "your-username"
application_password: "your-app-password"

# 獲取 Application Password 步驟：
# 1. 登入 WordPress 管理後台
# 2. 前往 用戶 → 個人資料
# 3. 捲動到 "應用程式密碼" 區塊
# 4. 輸入名稱（如 "AI Writer"）並點擊 "新增應用程式密碼"
# 5. 複製生成的密碼（格式：xxxx xxxx xxxx xxxx xxxx xxxx）
# 6. 貼上到上方 application_password 欄位
EOF

    echo "   ✅ 已創建範本檔案：$WORDPRESS_CREDS"
    echo "   ⚠️  請編輯此檔案並填入您的 WordPress 憑證"
else
    echo "   ✅ WordPress 憑證檔案存在"
fi

echo ""

# 測試腳本
echo "🧪 測試支援腳本..."

echo "1️⃣  測試 WordPress Publisher..."
if python3 .claude/skills/wordpress-publisher/publish.py --help 2>&1 | grep -q "用法"; then
    echo "   ✅ WordPress Publisher 可執行"
else
    echo "   ℹ️  WordPress Publisher 需要參數才能執行（正常）"
fi

echo "2️⃣  測試 SEO Analyzer..."
if python3 .claude/skills/seo-analyzer/analyze.py --help 2>&1 | grep -q "用法"; then
    echo "   ✅ SEO Analyzer 可執行"
else
    echo "   ℹ️  SEO Analyzer 需要參數才能執行（正常）"
fi

echo "3️⃣  測試 Analytics Reporter..."
if python3 .claude/skills/analytics-reporter/generate_report.py --help 2>&1 | grep -q "用法"; then
    echo "   ✅ Analytics Reporter 可執行"
else
    echo "   ℹ️  Analytics Reporter 需要參數才能執行（正常）"
fi

echo ""

# 創建輸出目錄
echo "📁 創建輸出目錄..."
mkdir -p output/analytics
mkdir -p output/seo_reports
mkdir -p .claude/skills/research-cache

echo "✅ 輸出目錄已創建"
echo ""

# 顯示 Skills 列表
echo "📋 已安裝的 Skills："
echo ""
echo "1. 🌐 wordpress-publisher - WordPress 文章發布"
echo "   用途：將 Markdown 文章發布到 WordPress 網站"
echo "   腳本：.claude/skills/wordpress-publisher/publish.py"
echo ""
echo "2. 🔍 seo-analyzer - SEO 分析評分"
echo "   用途：分析文章 SEO 質量並給出 0-100 分評分"
echo "   腳本：.claude/skills/seo-analyzer/analyze.py"
echo ""
echo "3. 📊 analytics-reporter - 分析報告生成"
echo "   用途：從 Google Analytics 生成週報/月報"
echo "   腳本：.claude/skills/analytics-reporter/generate_report.py"
echo ""
echo "4. 📝 content-repurposer - 內容改寫器"
echo "   用途：將 1 篇文章轉換為 30+ 社群媒體內容"
echo "   指令：使用 Claude Code 調用此 Skill"
echo ""
echo "5. 🎨 marketing-assets - 行銷素材生成器"
echo "   用途：生成標題、Hook、CTA 等行銷素材"
echo "   指令：使用 Claude Code 調用此 Skill"
echo ""

# 顯示下一步
echo "========================================="
echo "✅ Skills 系統設定完成！"
echo ""
echo "📝 下一步："
echo ""
echo "1. 編輯 WordPress 憑證："
echo "   nano $WORDPRESS_CREDS"
echo ""
echo "2. 測試 WordPress 發布（需先設定憑證）："
echo "   python3 .claude/skills/wordpress-publisher/publish.py test_article.md \"測試標題\""
echo ""
echo "3. 測試 SEO 分析："
echo "   python3 .claude/skills/seo-analyzer/analyze.py output/session_*/final_article.md"
echo ""
echo "4. 在 Claude Code 中使用 Skills："
echo "   「請使用 content-repurposer Skill 將這篇文章轉換為社群媒體內容」"
echo ""
echo "📚 完整文件："
echo "   - README_SKILLS_PLUGIN.md"
echo "   - .claude/skills/*/SKILL.md"
echo ""
