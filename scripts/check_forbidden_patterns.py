#!/usr/bin/env python3
"""
禁止模式檢查器
自動檢查文章中是否包含 AI 常見但不自然的寫作習慣
"""

import sys
import yaml
from pathlib import Path
from typing import List, Dict, Tuple


class ForbiddenPatternChecker:
    """檢查文章中的禁止模式"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            # 使用腳本所在目錄的相對路徑
            script_dir = Path(__file__).parent.parent
            config_path = script_dir / ".claude/config/forbidden-patterns.yaml"

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def check_file(self, file_path: str) -> Tuple[bool, List[Dict]]:
        """
        檢查文件是否包含禁止模式

        Returns:
            (is_clean, issues): (是否通過檢查, 問題列表)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []

        # 檢查禁止符號
        for item in self.config.get('forbidden_symbols', []):
            symbol = item['symbol']
            if symbol in content:
                count = content.count(symbol)
                lines = self._find_lines(content, symbol)
                issues.append({
                    'type': 'forbidden_symbol',
                    'symbol': symbol,
                    'name': item['name'],
                    'reason': item['reason'],
                    'count': count,
                    'lines': lines,
                    'alternatives': item['alternatives']
                })

        # 檢查禁止短語
        for item in self.config.get('forbidden_phrases', []):
            phrase = item['phrase']
            if phrase in content:
                count = content.count(phrase)
                lines = self._find_lines(content, phrase)
                issues.append({
                    'type': 'forbidden_phrase',
                    'phrase': phrase,
                    'reason': item['reason'],
                    'count': count,
                    'lines': lines,
                    'alternatives': item['alternatives']
                })

        is_clean = len(issues) == 0
        return is_clean, issues

    def _find_lines(self, content: str, pattern: str) -> List[int]:
        """找出包含特定模式的行號"""
        lines = []
        for i, line in enumerate(content.split('\n'), 1):
            if pattern in line:
                lines.append(i)
        return lines

    def print_report(self, file_path: str, is_clean: bool, issues: List[Dict]):
        """輸出檢查報告"""
        print(f"\n{'='*70}")
        print(f"📝 檢查文件: {file_path}")
        print(f"{'='*70}\n")

        if is_clean:
            print("✅ 恭喜！文章沒有發現禁止模式\n")
            return

        print(f"❌ 發現 {len(issues)} 個問題需要修正：\n")

        for i, issue in enumerate(issues, 1):
            print(f"{i}. ", end="")

            if issue['type'] == 'forbidden_symbol':
                print(f"禁止符號：{issue['name']}")
                print(f"   符號：{issue['symbol']}")
                print(f"   原因：{issue['reason']}")
                print(f"   出現次數：{issue['count']} 次")
                print(f"   出現行號：{', '.join(map(str, issue['lines'][:5]))}", end="")
                if len(issue['lines']) > 5:
                    print(f" (還有 {len(issue['lines']) - 5} 處)")
                else:
                    print()
                print(f"   建議替換：")
                if isinstance(issue['alternatives'], list):
                    for alt in issue['alternatives']:
                        print(f"      - {alt}")
                else:
                    print(f"      - {issue['alternatives']}")

            elif issue['type'] == 'forbidden_phrase':
                print(f"禁止短語：{issue['phrase']}")
                print(f"   原因：{issue['reason']}")
                print(f"   出現次數：{issue['count']} 次")
                print(f"   出現行號：{', '.join(map(str, issue['lines'][:5]))}", end="")
                if len(issue['lines']) > 5:
                    print(f" (還有 {len(issue['lines']) - 5} 處)")
                else:
                    print()
                print(f"   建議替換：")
                if isinstance(issue['alternatives'], list):
                    for alt in issue['alternatives']:
                        print(f"      - {alt}")
                else:
                    print(f"      - {issue['alternatives']}")

            print()

        print(f"{'='*70}\n")
        print("💡 建議：")
        print("   1. 使用文字編輯器的「尋找與取代」功能")
        print("   2. 手動檢查每個位置，選擇最自然的替換方式")
        print("   3. 修正後重新執行此腳本驗證\n")


def main():
    if len(sys.argv) < 2:
        print("用法: python check_forbidden_patterns.py <文章路徑>")
        print("範例: python check_forbidden_patterns.py output/session_xxx/FINAL_OPTIMIZED_ARTICLE.md")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"❌ 錯誤：文件不存在 - {file_path}")
        sys.exit(1)

    checker = ForbiddenPatternChecker()
    is_clean, issues = checker.check_file(file_path)
    checker.print_report(file_path, is_clean, issues)

    # 返回狀態碼（0=通過, 1=失敗）
    sys.exit(0 if is_clean else 1)


if __name__ == "__main__":
    main()
