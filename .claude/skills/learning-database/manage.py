#!/usr/bin/env python3
"""
Learning Database Skill
管理和操作學習數據庫，支援模式存儲、用戶偏好管理和知識累積

Usage:
    python3 manage.py init
    python3 manage.py add-pattern --type success --category opening --pattern "問句開頭"
    python3 manage.py query-patterns --category opening --min-success-rate 0.7
    python3 manage.py update-preferences --file preferences.yaml
    python3 manage.py log-session --session-dir output/session_xxx --score 85
    python3 manage.py generate-report --type weekly --output report.md
    python3 manage.py status
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import yaml


# 預設路徑
DEFAULT_MEMORY_PATH = Path(__file__).parent.parent.parent / "memory"


class LearningDatabase:
    """學習數據庫管理類"""

    def __init__(self, memory_path: Path = DEFAULT_MEMORY_PATH):
        self.memory_path = memory_path
        self.patterns_file = memory_path / "patterns" / "success.json"
        self.failed_patterns_file = memory_path / "patterns" / "failed.json"
        self.preferences_dir = memory_path / "user_preferences"
        self.history_dir = memory_path / "history"
        self.knowledge_dir = memory_path / "knowledge"

    def init(self) -> Dict:
        """初始化數據庫結構"""
        directories = [
            self.memory_path,
            self.memory_path / "patterns",
            self.preferences_dir,
            self.history_dir,
            self.knowledge_dir,
            self.memory_path / "cache",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # 初始化檔案
        default_files = {
            self.patterns_file: {"patterns": [], "metadata": {"version": "1.0.0", "created": datetime.now().isoformat()}},
            self.failed_patterns_file: {"patterns": [], "metadata": {"version": "1.0.0", "created": datetime.now().isoformat()}},
            self.preferences_dir / "style.yaml": self._default_style_preferences(),
            self.preferences_dir / "content.yaml": self._default_content_preferences(),
            self.preferences_dir / "workflow.yaml": self._default_workflow_preferences(),
            self.knowledge_dir / "terminology.yaml": {"terms": []},
            self.knowledge_dir / "forbidden.yaml": {"words": []},
            self.knowledge_dir / "rules.yaml": {"rules": []},
            self.memory_path / "config.yaml": self._default_config(),
        }

        created = []
        for filepath, default_content in default_files.items():
            if not filepath.exists():
                if filepath.suffix == ".json":
                    filepath.write_text(json.dumps(default_content, ensure_ascii=False, indent=2), encoding="utf-8")
                else:
                    filepath.write_text(yaml.dump(default_content, allow_unicode=True, default_flow_style=False), encoding="utf-8")
                created.append(str(filepath.name))

        return {
            "status": "success",
            "memory_path": str(self.memory_path),
            "created_files": created,
            "message": f"學習數據庫已初始化於 {self.memory_path}",
        }

    def _default_style_preferences(self) -> Dict:
        return {
            "tone": {
                "formality": 0.5,
                "warmth": 0.7,
                "humor": 0.3,
                "directness": 0.6,
            },
            "vocabulary": {
                "complexity": "medium",
                "jargon_level": "low",
            },
            "structure": {
                "paragraph_length": "medium",
                "header_frequency": "normal",
                "list_usage": "medium",
            },
        }

    def _default_content_preferences(self) -> Dict:
        return {
            "depth": {
                "detail_level": "medium",
                "example_frequency": "high",
                "data_citations": True,
            },
            "elements": {
                "personal_stories": True,
                "case_studies": True,
                "actionable_tips": True,
            },
            "length": {
                "min_words": 1500,
                "max_words": 3000,
                "target_words": 2000,
            },
        }

    def _default_workflow_preferences(self) -> Dict:
        return {
            "phases": {
                "skip_style_matcher": False,
                "skip_storyteller": False,
                "auto_publish": False,
            },
            "quality": {
                "min_editor_score": 85,
                "min_seo_score": 80,
                "max_ai_detection": 40,
            },
        }

    def _default_config(self) -> Dict:
        return {
            "database": {
                "version": "1.0.0",
                "backup_enabled": True,
                "backup_frequency": "daily",
            },
            "learning": {
                "min_samples_for_pattern": 5,
                "success_threshold": 0.6,
                "decay_rate": 0.95,
            },
            "storage": {
                "max_patterns": 1000,
                "max_history_days": 90,
                "compression": True,
            },
        }

    def add_pattern(
        self,
        pattern_type: str,
        category: str,
        pattern: str,
        example: str = "",
        context: List[str] = None,
        description: str = "",
    ) -> Dict:
        """添加模式"""
        if context is None:
            context = []

        target_file = self.patterns_file if pattern_type == "success" else self.failed_patterns_file

        if not target_file.exists():
            self.init()

        data = json.loads(target_file.read_text(encoding="utf-8"))

        new_pattern = {
            "id": f"pattern_{uuid.uuid4().hex[:8]}",
            "type": pattern_type,
            "category": category,
            "pattern": pattern,
            "description": description,
            "example": example,
            "context": context,
            "metrics": {
                "usage_count": 1,
                "success_rate": 0.5 if pattern_type == "success" else 0.0,
                "avg_engagement": 0.0,
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        data["patterns"].append(new_pattern)
        target_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "status": "success",
            "pattern_id": new_pattern["id"],
            "message": f"模式已添加: {pattern}",
        }

    def query_patterns(
        self,
        category: Optional[str] = None,
        min_success_rate: float = 0.0,
        context: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict]:
        """查詢模式"""
        if not self.patterns_file.exists():
            return []

        data = json.loads(self.patterns_file.read_text(encoding="utf-8"))
        patterns = data.get("patterns", [])

        # 過濾
        filtered = []
        for p in patterns:
            if category and p.get("category") != category:
                continue
            if p.get("metrics", {}).get("success_rate", 0) < min_success_rate:
                continue
            if context and context not in p.get("context", []):
                continue
            filtered.append(p)

        # 排序 (按成功率)
        filtered.sort(key=lambda x: x.get("metrics", {}).get("success_rate", 0), reverse=True)

        return filtered[:limit]

    def update_preferences(self, preferences: Dict, pref_type: str = "style") -> Dict:
        """更新用戶偏好"""
        pref_file = self.preferences_dir / f"{pref_type}.yaml"

        if pref_file.exists():
            current = yaml.safe_load(pref_file.read_text(encoding="utf-8")) or {}
        else:
            current = {}

        # 深度合併
        def deep_merge(base, update):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value

        deep_merge(current, preferences)
        current["_updated_at"] = datetime.now().isoformat()

        pref_file.write_text(yaml.dump(current, allow_unicode=True, default_flow_style=False), encoding="utf-8")

        return {
            "status": "success",
            "file": str(pref_file),
            "message": f"{pref_type} 偏好已更新",
        }

    def log_session(
        self,
        session_id: str,
        score: int,
        feedback: str = "",
        metrics: Dict = None,
    ) -> Dict:
        """記錄 session"""
        if metrics is None:
            metrics = {}

        sessions_file = self.history_dir / "sessions.jsonl"

        entry = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "feedback": feedback,
            "metrics": metrics,
        }

        with open(sessions_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return {
            "status": "success",
            "session_id": session_id,
            "message": "Session 已記錄",
        }

    def generate_report(self, report_type: str = "weekly") -> Dict:
        """生成學習報告"""
        sessions_file = self.history_dir / "sessions.jsonl"

        # 讀取 session 歷史
        sessions = []
        if sessions_file.exists():
            with open(sessions_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        sessions.append(json.loads(line))

        # 計算時間範圍
        if report_type == "weekly":
            cutoff = datetime.now() - timedelta(days=7)
        elif report_type == "monthly":
            cutoff = datetime.now() - timedelta(days=30)
        else:
            cutoff = datetime.now() - timedelta(days=7)

        recent_sessions = [
            s for s in sessions
            if datetime.fromisoformat(s["timestamp"]) > cutoff
        ]

        # 統計
        total_sessions = len(recent_sessions)
        avg_score = sum(s["score"] for s in recent_sessions) / max(1, total_sessions)

        # 讀取模式統計
        patterns = []
        if self.patterns_file.exists():
            data = json.loads(self.patterns_file.read_text(encoding="utf-8"))
            patterns = data.get("patterns", [])

        high_success_patterns = [p for p in patterns if p.get("metrics", {}).get("success_rate", 0) >= 0.8]

        # 生成報告
        report = {
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "period": {
                "start": cutoff.isoformat(),
                "end": datetime.now().isoformat(),
            },
            "summary": {
                "total_sessions": total_sessions,
                "average_score": round(avg_score, 1),
                "total_patterns": len(patterns),
                "high_success_patterns": len(high_success_patterns),
            },
            "top_patterns": [
                {
                    "pattern": p["pattern"],
                    "category": p["category"],
                    "success_rate": p["metrics"]["success_rate"],
                }
                for p in sorted(patterns, key=lambda x: x.get("metrics", {}).get("success_rate", 0), reverse=True)[:5]
            ],
        }

        return report

    def get_status(self) -> Dict:
        """獲取數據庫狀態"""
        status = {
            "initialized": self.memory_path.exists(),
            "memory_path": str(self.memory_path),
            "statistics": {},
        }

        if self.memory_path.exists():
            # 模式統計
            if self.patterns_file.exists():
                data = json.loads(self.patterns_file.read_text(encoding="utf-8"))
                status["statistics"]["success_patterns"] = len(data.get("patterns", []))

            if self.failed_patterns_file.exists():
                data = json.loads(self.failed_patterns_file.read_text(encoding="utf-8"))
                status["statistics"]["failed_patterns"] = len(data.get("patterns", []))

            # Session 統計
            sessions_file = self.history_dir / "sessions.jsonl"
            if sessions_file.exists():
                with open(sessions_file, "r", encoding="utf-8") as f:
                    status["statistics"]["logged_sessions"] = sum(1 for _ in f)

            # 偏好檔案
            status["preferences"] = {
                "style": (self.preferences_dir / "style.yaml").exists(),
                "content": (self.preferences_dir / "content.yaml").exists(),
                "workflow": (self.preferences_dir / "workflow.yaml").exists(),
            }

        return status

    def cleanup(self, older_than_days: int = 90) -> Dict:
        """清理過期數據"""
        cutoff = datetime.now() - timedelta(days=older_than_days)
        cleaned = {"sessions": 0, "patterns_updated": 0}

        # 清理 session 歷史
        sessions_file = self.history_dir / "sessions.jsonl"
        if sessions_file.exists():
            valid_sessions = []
            with open(sessions_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        session = json.loads(line)
                        if datetime.fromisoformat(session["timestamp"]) > cutoff:
                            valid_sessions.append(session)
                        else:
                            cleaned["sessions"] += 1

            with open(sessions_file, "w", encoding="utf-8") as f:
                for session in valid_sessions:
                    f.write(json.dumps(session, ensure_ascii=False) + "\n")

        return {
            "status": "success",
            "cleaned": cleaned,
            "message": f"已清理 {cleaned['sessions']} 個過期 session",
        }


def generate_markdown_report(report: Dict) -> str:
    """生成 Markdown 格式報告"""
    lines = [
        "# 學習數據庫報告",
        "",
        f"**報告類型**: {report['report_type']}",
        f"**生成時間**: {report['generated_at']}",
        "",
        "## 摘要統計",
        "",
        "| 指標 | 數值 |",
        "|------|------|",
        f"| Session 數量 | {report['summary']['total_sessions']} |",
        f"| 平均品質分數 | {report['summary']['average_score']}/100 |",
        f"| 總模式數 | {report['summary']['total_patterns']} |",
        f"| 高成功率模式 | {report['summary']['high_success_patterns']} |",
        "",
        "## 最佳模式",
        "",
        "| 模式 | 類別 | 成功率 |",
        "|------|------|--------|",
    ]

    for p in report.get("top_patterns", []):
        lines.append(f"| {p['pattern']} | {p['category']} | {p['success_rate']*100:.0f}% |")

    lines.extend([
        "",
        "---",
        "",
        "*自動生成 by Learning Database Skill*",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Learning Database Skill - 學習數據庫管理")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init
    subparsers.add_parser("init", help="初始化學習數據庫")

    # add-pattern
    add_parser = subparsers.add_parser("add-pattern", help="添加模式")
    add_parser.add_argument("--type", choices=["success", "failed"], default="success")
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--pattern", required=True)
    add_parser.add_argument("--example", default="")
    add_parser.add_argument("--context", nargs="*", default=[])
    add_parser.add_argument("--description", default="")

    # query-patterns
    query_parser = subparsers.add_parser("query-patterns", help="查詢模式")
    query_parser.add_argument("--category", default=None)
    query_parser.add_argument("--min-success-rate", type=float, default=0.0)
    query_parser.add_argument("--context", default=None)
    query_parser.add_argument("--limit", type=int, default=10)

    # update-preferences
    pref_parser = subparsers.add_parser("update-preferences", help="更新偏好")
    pref_parser.add_argument("--file", required=True)
    pref_parser.add_argument("--type", default="style")

    # log-session
    log_parser = subparsers.add_parser("log-session", help="記錄 session")
    log_parser.add_argument("--session-dir", required=True)
    log_parser.add_argument("--score", type=int, required=True)
    log_parser.add_argument("--feedback", default="")

    # generate-report
    report_parser = subparsers.add_parser("generate-report", help="生成報告")
    report_parser.add_argument("--type", choices=["weekly", "monthly"], default="weekly")
    report_parser.add_argument("--output", default="learning_report.md")
    report_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    # status
    subparsers.add_parser("status", help="查看數據庫狀態")

    # cleanup
    cleanup_parser = subparsers.add_parser("cleanup", help="清理過期數據")
    cleanup_parser.add_argument("--older-than", type=int, default=90)

    args = parser.parse_args()

    db = LearningDatabase()

    if args.command == "init":
        result = db.init()
        print(f"✅ {result['message']}")
        if result["created_files"]:
            print(f"   創建檔案: {', '.join(result['created_files'])}")

    elif args.command == "add-pattern":
        result = db.add_pattern(
            pattern_type=args.type,
            category=args.category,
            pattern=args.pattern,
            example=args.example,
            context=args.context,
            description=args.description,
        )
        print(f"✅ {result['message']} (ID: {result['pattern_id']})")

    elif args.command == "query-patterns":
        patterns = db.query_patterns(
            category=args.category,
            min_success_rate=args.min_success_rate,
            context=args.context,
            limit=args.limit,
        )
        if patterns:
            print(f"找到 {len(patterns)} 個模式:")
            for p in patterns:
                rate = p.get("metrics", {}).get("success_rate", 0)
                print(f"  - [{p['category']}] {p['pattern']} (成功率: {rate*100:.0f}%)")
        else:
            print("未找到符合條件的模式")

    elif args.command == "update-preferences":
        pref_file = Path(args.file)
        if not pref_file.exists():
            print(f"❌ 檔案不存在: {args.file}")
            sys.exit(1)

        prefs = yaml.safe_load(pref_file.read_text(encoding="utf-8"))
        result = db.update_preferences(prefs, args.type)
        print(f"✅ {result['message']}")

    elif args.command == "log-session":
        session_id = Path(args.session_dir).name
        result = db.log_session(
            session_id=session_id,
            score=args.score,
            feedback=args.feedback,
        )
        print(f"✅ {result['message']}")

    elif args.command == "generate-report":
        report = db.generate_report(args.type)

        output_path = Path(args.output)
        if args.format == "markdown":
            content = generate_markdown_report(report)
        else:
            content = json.dumps(report, ensure_ascii=False, indent=2)

        output_path.write_text(content, encoding="utf-8")
        print(f"✅ 報告已生成: {output_path}")

    elif args.command == "status":
        status = db.get_status()
        print("學習數據庫狀態:")
        print(f"  路徑: {status['memory_path']}")
        print(f"  已初始化: {'是' if status['initialized'] else '否'}")
        if status.get("statistics"):
            print("  統計:")
            for key, value in status["statistics"].items():
                print(f"    - {key}: {value}")

    elif args.command == "cleanup":
        result = db.cleanup(args.older_than)
        print(f"✅ {result['message']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
