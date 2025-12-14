#!/usr/bin/env python3
"""
自動插入圖片到 draft_final.md
根據實際文章結構，精準插入圖片
"""

import os
import shutil
from datetime import datetime


def insert_images_to_draft():
    """將圖片插入到 draft_final.md"""

    # 檔案路徑
    base_dir = "/Users/liutsungying/喵哩文創部落格AI寫手系統"
    draft_path = os.path.join(base_dir, "output/session_20251030_115533/draft_final.md")
    backup_path = draft_path.replace(".md", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

    # 讀取文章
    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 備份原文
    shutil.copy2(draft_path, backup_path)
    print(f"✓ 已備份原文: {os.path.basename(backup_path)}")

    # 定義插入規則（按照 draft_final.md 的實際結構）
    insertions = [
        {
            'marker': '## 技術架構與工作原理：解密背後的運作機制\n\n### 系統架構設計',
            'replacement': '''## 技術架構與工作原理：解密背後的運作機制

![Social Analyzer 系統架構圖](images/system-architecture.png)
*Social Analyzer 的前後端架構與技術堆疊*

### 系統架構設計''',
            'name': 'system-architecture.png'
        },
        {
            'marker': '| 結果呈現 | 分散的搜尋結果 | 統一介面視覺化 |\n\n這使得原本需要數小時甚至數天的調查工作',
            'replacement': '''| 結果呈現 | 分散的搜尋結果 | 統一介面視覺化 |

![傳統方式 vs Social Analyzer 比較](images/comparison-chart.svg)
*傳統搜尋方式與 Social Analyzer 的效率比較*

這使得原本需要數小時甚至數天的調查工作''',
            'name': 'comparison-chart.svg'
        },
        {
            'marker': '### 四種偵測模式深度解析\n\n根據官方文件說明',
            'replacement': '''### 四種偵測模式深度解析

![四種偵測模式流程圖](images/detection-modes.png)
*Social Analyzer 四種偵測模式的運作流程*

根據官方文件說明''',
            'name': 'detection-modes.png'
        },
        {
            'marker': '### 信心度評分機制\n\n根據官方說明文件',
            'replacement': '''### 信心度評分機制

![信心度評分指南](images/confidence-score-chart.svg)
*不同信心度分數的可信度等級*

根據官方說明文件''',
            'name': 'confidence-score-chart.svg'
        },
        {
            'marker': '### 1. 詐騙防制：追蹤多平台詐騙集團\n\n**假設情境**',
            'replacement': '''### 1. 詐騙防制：追蹤多平台詐騙集團

![詐騙查證流程示意圖](images/scam-investigation-flow.png)
*使用 Social Analyzer 追蹤詐騙帳號的完整流程*

**假設情境**''',
            'name': 'scam-investigation-flow.png'
        },
        {
            'marker': '## 法律與倫理注意事項：合法使用的紅線\n\n### 台灣個資法規範',
            'replacement': '''## 法律與倫理注意事項：合法使用的紅線

![個資法合規指南](images/legal-compliance-guide.svg)
*個資法規範下的合法使用 vs 違法行為對照*

### 台灣個資法規範''',
            'name': 'legal-compliance-guide.svg'
        }
    ]

    # 額外檢查：如果有"灰色地帶"的章節，插入決策樹
    if '灰色地帶的判斷原則' in content:
        # 尋找灰色地帶章節的位置
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '灰色地帶的判斷原則' in line and line.startswith('#'):
                # 在標題後插入
                if i + 1 < len(lines):
                    insert_text = '\n![使用場景合法性判斷流程](images/legality-decision-tree.png)\n*判斷使用場景是否合法的決策流程*\n'
                    lines.insert(i + 1, insert_text)
                    content = '\n'.join(lines)
                    print("  ✓ legality-decision-tree.png (在灰色地帶章節)")
                    break

    # 執行插入
    inserted_count = 0
    for insertion in insertions:
        if insertion['marker'] in content:
            content = content.replace(insertion['marker'], insertion['replacement'])
            print(f"  ✓ {insertion['name']} (已插入)")
            inserted_count += 1
        else:
            print(f"  ⚠️  {insertion['name']} (找不到插入位置，已跳過)")

    # 寫入更新後的內容
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return inserted_count, backup_path


def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         📝 自動插入圖片到 draft_final.md 📝               ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        inserted_count, backup_path = insert_images_to_draft()

        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║                   ✅ 插入完成！                            ║")
        print("╚════════════════════════════════════════════════════════════╝\n")

        print(f"✓ 共插入 {inserted_count} 張圖片")
        print(f"✓ 原文備份: {os.path.basename(backup_path)}")
        print(f"✓ 更新文章: draft_final.md\n")

        print("💡 提示:")
        print("  - 打開 draft_final.md 查看結果")
        print("  - 如不滿意可還原備份")
        print("  - 查看 VISUAL_INSERT_GUIDE.md 了解插入位置\n")

    except FileNotFoundError as e:
        print(f"\n❌ 錯誤: 找不到文件")
        print(f"   {e}")
        print("\n   請確認路徑是否正確")
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
