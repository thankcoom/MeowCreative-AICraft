#!/bin/bash

# 喵哩文創部落格自動化圖片生成腳本
# 一鍵生成所有文章所需的圖片

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         🎨 喵哩文創部落格自動化圖片生成系統 🎨             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 取得腳本所在目錄
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 檢查必要工具
echo -e "${BLUE}[1/4] 檢查系統環境...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未找到 Node.js，請先安裝 Node.js${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python3，請先安裝 Python3${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js $(node -v) 已安裝${NC}"
echo -e "${GREEN}✓ Python $(python3 --version) 已安裝${NC}"
echo ""

# 安裝依賴（如果需要）
echo -e "${BLUE}[2/4] 檢查並安裝依賴...${NC}"

if [ ! -d "node_modules" ]; then
    echo "正在安裝 Node.js 依賴..."
    npm install --quiet
fi

# 檢查 Python 依賴
python3 -c "import svgwrite" 2>/dev/null || {
    echo "正在安裝 Python 依賴..."
    pip3 install -q pillow cairosvg svgwrite
}

echo -e "${GREEN}✓ 所有依賴已就緒${NC}"
echo ""

# 生成圖片
echo -e "${BLUE}[3/4] 開始生成圖片...${NC}"
node scripts/generate_images.js

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 圖片生成完成！${NC}"
else
    echo -e "${RED}❌ 圖片生成失敗${NC}"
    exit 1
fi

echo ""

# 顯示結果
echo -e "${BLUE}[4/4] 生成結果摘要${NC}"
echo ""

OUTPUT_DIR="output/session_20251030_115533/images"
if [ -d "$OUTPUT_DIR" ]; then
    IMAGE_COUNT=$(find "$OUTPUT_DIR" -type f \( -name "*.png" -o -name "*.svg" -o -name "*.jpg" \) | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ 共生成 $IMAGE_COUNT 個圖片文件${NC}"
    echo -e "${YELLOW}📁 圖片位置: $OUTPUT_DIR${NC}"
    echo ""

    echo "生成的圖片列表："
    ls -lh "$OUTPUT_DIR" | grep -E "\.(png|svg|jpg)$" | awk '{print "  - " $9 " (" $5 ")"}'
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   ✅ 全部完成！                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${YELLOW}💡 提示:${NC}"
echo "  1. 查看圖片: open $OUTPUT_DIR"
echo "  2. 查看 Markdown 引用: cat $OUTPUT_DIR/image-references.md"
echo "  3. 將圖片插入文章: 複製引用到 final_article.md"
echo ""
