#!/bin/bash
# 快速檢查工作流程完整性
# 版本: 1.0.0

echo "🔍 工作流程完整性檢查工具"
echo "================================"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查 output 目錄是否存在
if [ ! -d "output" ]; then
    echo -e "${RED}❌ 錯誤：找不到 output 目錄${NC}"
    exit 1
fi

# 獲取最新的 session
LATEST_SESSION=$(ls -t output/ | grep "^session_" | head -1)

if [ -z "$LATEST_SESSION" ]; then
    echo -e "${RED}❌ 錯誤：找不到任何 session${NC}"
    echo ""
    echo "請先執行 Blog Manager 創建一個 session"
    exit 1
fi

SESSION_PATH="output/$LATEST_SESSION"

echo -e "${BLUE}📁 檢查 Session：${NC}$LATEST_SESSION"
echo ""

# 執行驗證
python3 .claude/skills/workflow-validator/workflow_validator.py validate "$SESSION_PATH"

EXIT_CODE=$?

echo ""
echo "================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ 驗證通過！所有必要步驟都已完成。${NC}"
else
    echo -e "${RED}❌ 驗證失敗！請檢查缺少的步驟。${NC}"
    echo ""
    echo "查看詳細報告："
    echo "  cat $SESSION_PATH/validation_report.json"
fi

echo ""
echo "================================"

exit $EXIT_CODE
