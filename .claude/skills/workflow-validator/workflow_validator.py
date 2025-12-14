#!/usr/bin/env python3
"""
工作流程完整性驗證器
版本: 1.0.0
目的: 確保 Blog Manager 執行所有必要的 Agent 步驟
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class WorkflowValidator:
    """工作流程驗證器"""

    def __init__(self, config_path: str = None):
        """初始化驗證器"""
        if config_path is None:
            config_path = ".claude/config/workflow-validation.yaml"

        self.config_path = config_path
        self.config = self._load_config()
        self.validation_results = {
            "passed": [],
            "failed": [],
            "warnings": [],
            "skipped": []
        }

    def _load_config(self) -> Dict:
        """載入驗證配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def validate_session(self, session_path: str) -> Dict:
        """
        驗證整個 session 的完整性

        Args:
            session_path: session 資料夾路徑，例如 output/session_20251027_123456

        Returns:
            驗證結果字典
        """
        print(f"🔍 開始驗證 Session: {session_path}\n")

        if not os.path.exists(session_path):
            return {
                "status": "error",
                "message": f"❌ Session 路徑不存在: {session_path}"
            }

        # 驗證每個 Phase
        phases = self.config['required_phases']

        for phase_id, phase_config in phases.items():
            self._validate_phase(session_path, phase_id, phase_config)

        # 生成總結報告
        return self._generate_report()

    def _validate_phase(self, session_path: str, phase_id: str, phase_config: Dict):
        """驗證單個 Phase"""
        phase_name = phase_config['name']
        agent_name = phase_config['agent']
        required = phase_config['required']
        priority = phase_config['priority']

        print(f"📋 驗證 {phase_id.upper()}: {phase_name}")
        print(f"   Agent: {agent_name}")
        print(f"   必要性: {'✅ 必須' if required else '⭕ 可選'} ({priority})")

        # 檢查是否有跳過條件
        skip_conditions = phase_config.get('skip_conditions', [])
        if skip_conditions and not required:
            print(f"   ℹ️  可跳過條件: {len(skip_conditions)} 個")

        # 驗證輸出檔案
        outputs = phase_config.get('outputs', [])
        all_passed = True

        for output in outputs:
            file_path = os.path.join(session_path, output['file'])
            file_desc = output['description']

            if not os.path.exists(file_path):
                if required and priority == 'critical':
                    print(f"   ❌ 缺少必要檔案: {output['file']}")
                    self.validation_results['failed'].append({
                        'phase': phase_id,
                        'issue': f"缺少檔案: {output['file']}",
                        'severity': 'critical'
                    })
                    all_passed = False
                else:
                    print(f"   ⚠️  缺少可選檔案: {output['file']}")
                    self.validation_results['warnings'].append({
                        'phase': phase_id,
                        'issue': f"缺少檔案: {output['file']}",
                        'severity': 'warning'
                    })
                continue

            # 驗證檔案內容
            validation = output.get('validation', {})
            content_valid = self._validate_file_content(file_path, validation)

            if content_valid:
                print(f"   ✅ {output['file']} - 驗證通過")
                self.validation_results['passed'].append({
                    'phase': phase_id,
                    'file': output['file']
                })
            else:
                print(f"   ❌ {output['file']} - 驗證失敗")
                self.validation_results['failed'].append({
                    'phase': phase_id,
                    'file': output['file'],
                    'issue': '內容驗證失敗'
                })
                all_passed = False

        print()  # 空行分隔

    def _validate_file_content(self, file_path: str, validation: Dict) -> bool:
        """驗證檔案內容"""
        if not validation:
            return True

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 檢查檔案大小
            if 'min_size_bytes' in validation:
                size = len(content.encode('utf-8'))
                if size < validation['min_size_bytes']:
                    print(f"      ⚠️  檔案太小: {size} bytes < {validation['min_size_bytes']} bytes")
                    return False

            if 'max_size_bytes' in validation:
                size = len(content.encode('utf-8'))
                if size > validation['max_size_bytes']:
                    print(f"      ⚠️  檔案太大: {size} bytes > {validation['max_size_bytes']} bytes")
                    return False

            # 檢查必須包含的內容
            if 'must_contain' in validation:
                for keyword in validation['must_contain']:
                    if keyword not in content:
                        print(f"      ⚠️  缺少必要內容: '{keyword}'")
                        return False

            return True

        except Exception as e:
            print(f"      ❌ 讀取檔案錯誤: {e}")
            return False

    def _generate_report(self) -> Dict:
        """生成驗證報告"""
        total_checks = (
            len(self.validation_results['passed']) +
            len(self.validation_results['failed']) +
            len(self.validation_results['warnings'])
        )

        passed_count = len(self.validation_results['passed'])
        failed_count = len(self.validation_results['failed'])
        warning_count = len(self.validation_results['warnings'])

        print("=" * 60)
        print("📊 驗證結果總結")
        print("=" * 60)
        print(f"✅ 通過: {passed_count}")
        print(f"❌ 失敗: {failed_count}")
        print(f"⚠️  警告: {warning_count}")
        print(f"總計檢查項: {total_checks}")
        print()

        # 判斷整體狀態
        if failed_count == 0:
            status = "success"
            message = "✅ 所有必要步驟都已完成！"
            print(message)
        elif failed_count > 0:
            status = "failed"
            message = f"❌ 有 {failed_count} 個必要步驟未完成，請檢查！"
            print(message)
            print("\n失敗項目:")
            for item in self.validation_results['failed']:
                print(f"  - Phase {item['phase']}: {item['issue']}")
        else:
            status = "warning"
            message = f"⚠️  有 {warning_count} 個警告，建議檢查"
            print(message)

        if warning_count > 0:
            print("\n警告項目:")
            for item in self.validation_results['warnings']:
                print(f"  - Phase {item['phase']}: {item['issue']}")

        print("=" * 60)

        return {
            "status": status,
            "message": message,
            "passed": passed_count,
            "failed": failed_count,
            "warnings": warning_count,
            "details": self.validation_results
        }

    def create_progress_tracker(self, session_path: str) -> str:
        """
        為新的 session 創建進度追蹤檔案

        Args:
            session_path: session 資料夾路徑

        Returns:
            progress.json 的路徑
        """
        phases = self.config['required_phases']

        progress = {
            "session_path": session_path,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "overall_status": "in_progress",
            "phases": {}
        }

        for phase_id, phase_config in phases.items():
            progress['phases'][phase_id] = {
                "name": phase_config['name'],
                "agent": phase_config['agent'],
                "status": "pending",
                "required": phase_config['required'],
                "priority": phase_config['priority'],
                "start_time": None,
                "end_time": None,
                "duration_seconds": None,
                "outputs": []
            }

        # 儲存進度檔案
        progress_file = os.path.join(session_path, "workflow_progress.json")
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        print(f"✅ 進度追蹤檔案已創建: {progress_file}")
        return progress_file

    def update_phase_status(self, session_path: str, phase_id: str, status: str,
                          outputs: List[str] = None):
        """
        更新 Phase 狀態

        Args:
            session_path: session 路徑
            phase_id: phase ID
            status: 狀態 (pending/in_progress/completed/failed/skipped)
            outputs: 生成的檔案列表
        """
        progress_file = os.path.join(session_path, "workflow_progress.json")

        if not os.path.exists(progress_file):
            print(f"⚠️  進度檔案不存在，正在創建...")
            self.create_progress_tracker(session_path)

        with open(progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)

        if phase_id not in progress['phases']:
            print(f"❌ 錯誤: Phase {phase_id} 不存在")
            return

        phase = progress['phases'][phase_id]
        now = datetime.now().isoformat()

        # 更新狀態
        if status == 'in_progress' and phase['status'] == 'pending':
            phase['start_time'] = now
        elif status in ['completed', 'failed', 'skipped'] and phase['status'] == 'in_progress':
            phase['end_time'] = now
            if phase['start_time']:
                start = datetime.fromisoformat(phase['start_time'])
                end = datetime.fromisoformat(phase['end_time'])
                phase['duration_seconds'] = (end - start).total_seconds()

        phase['status'] = status

        if outputs:
            phase['outputs'] = outputs

        progress['last_updated'] = now

        # 檢查整體狀態
        all_completed = all(
            p['status'] in ['completed', 'skipped']
            for p in progress['phases'].values()
            if p['required']
        )

        if all_completed:
            progress['overall_status'] = 'completed'

        # 儲存
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        print(f"✅ Phase {phase_id} 狀態已更新: {status}")


def main():
    """主函數"""
    import sys

    if len(sys.argv) < 2:
        print("使用方式:")
        print("  驗證 session:")
        print("    python workflow_validator.py validate <session_path>")
        print("")
        print("  創建進度追蹤:")
        print("    python workflow_validator.py init <session_path>")
        print("")
        print("  更新 phase 狀態:")
        print("    python workflow_validator.py update <session_path> <phase_id> <status>")
        print("")
        print("範例:")
        print("  python workflow_validator.py validate output/session_20251027_123456")
        return

    command = sys.argv[1]
    validator = WorkflowValidator()

    if command == "validate":
        if len(sys.argv) < 3:
            print("❌ 請提供 session 路徑")
            return

        session_path = sys.argv[2]
        result = validator.validate_session(session_path)

        # 儲存報告
        report_path = os.path.join(session_path, "validation_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n📄 詳細報告已儲存: {report_path}")

        # 返回狀態碼
        sys.exit(0 if result['status'] == 'success' else 1)

    elif command == "init":
        if len(sys.argv) < 3:
            print("❌ 請提供 session 路徑")
            return

        session_path = sys.argv[2]
        validator.create_progress_tracker(session_path)

    elif command == "update":
        if len(sys.argv) < 5:
            print("❌ 使用方式: update <session_path> <phase_id> <status>")
            return

        session_path = sys.argv[2]
        phase_id = sys.argv[3]
        status = sys.argv[4]

        validator.update_phase_status(session_path, phase_id, status)

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
