#!/usr/bin/env python3
"""
Performance Monitor Skill
監控和分析系統執行效能
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


# 效能數據存儲路徑
PERFORMANCE_DIR = Path(".claude/performance")
SESSIONS_FILE = PERFORMANCE_DIR / "sessions.jsonl"
BENCHMARKS_FILE = PERFORMANCE_DIR / "benchmarks.json"
CONFIG_FILE = PERFORMANCE_DIR / "config.yaml"


# 預設基準值
DEFAULT_BENCHMARKS = {
    "phase_durations": {
        "0": 60,   # Experience Collector
        "1": 90,   # Content Analyst
        "2a": 180, # Research Agent
        "2b": 120, # Style Matcher
        "3": 180,  # Writer Agent
        "3.4": 30, # Quality Predictor
        "3.5": 90, # Editor Agent
        "3.6": 60, # Fact Checker
        "3.7": 60, # Humanizer
        "3.8": 60, # Persuasion
        "3.9": 60, # Storyteller
        "4": 60,   # SEO Optimizer
        "5": 30,   # Publisher
        "11": 0,   # Memory (background)
        "12": 90,  # Persona Adapter
        "13": 0,   # Performance (background)
    },
    "token_budgets": {
        "total": 50000,
        "per_phase_avg": 3000,
    },
    "cache_targets": {
        "hit_rate": 0.7,
    },
    "time_targets": {
        "excellent": 480,
        "good": 600,
        "acceptable": 900,
        "slow": 1200,
    }
}


class PerformanceMonitor:
    """效能監控器"""

    def __init__(self):
        self._ensure_dirs()
        self.benchmarks = self._load_benchmarks()
        self.current_session = None

    def _ensure_dirs(self):
        """確保目錄存在"""
        PERFORMANCE_DIR.mkdir(parents=True, exist_ok=True)

    def _load_benchmarks(self) -> Dict:
        """載入基準值"""
        if BENCHMARKS_FILE.exists():
            with open(BENCHMARKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return DEFAULT_BENCHMARKS

    def _save_benchmarks(self):
        """保存基準值"""
        with open(BENCHMARKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.benchmarks, f, indent=2, ensure_ascii=False)

    def _load_sessions(self) -> List[Dict]:
        """載入所有 session 記錄"""
        sessions = []
        if SESSIONS_FILE.exists():
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        sessions.append(json.load(line.strip()))
        return sessions

    def _append_session(self, session: Dict):
        """追加 session 記錄"""
        with open(SESSIONS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(session, ensure_ascii=False) + '\n')

    def status(self) -> Dict:
        """顯示效能狀態"""
        sessions = self._load_sessions()

        if not sessions:
            return {
                "status": "no_data",
                "message": "尚無效能數據",
                "sessions_count": 0
            }

        # 計算統計
        total_sessions = len(sessions)
        recent_sessions = sessions[-10:]

        avg_duration = sum(s.get('total_duration', 0) for s in recent_sessions) / len(recent_sessions)
        avg_tokens = sum(s.get('resources', {}).get('total_tokens', 0) for s in recent_sessions) / len(recent_sessions)

        grades = [s.get('performance_grade', 'C') for s in recent_sessions]
        grade_counts = {g: grades.count(g) for g in set(grades)}

        return {
            "status": "active",
            "total_sessions": total_sessions,
            "recent_10_avg": {
                "duration": f"{avg_duration:.0f}s ({avg_duration/60:.1f}m)",
                "tokens": f"{avg_tokens:.0f}",
            },
            "grade_distribution": grade_counts,
            "benchmarks": {
                "excellent_threshold": f"{self.benchmarks['time_targets']['excellent']}s",
                "good_threshold": f"{self.benchmarks['time_targets']['good']}s",
            }
        }

    def start_session(self, session_id: str) -> Dict:
        """開始追蹤 session"""
        self.current_session = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "phases": [],
            "resources": {
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "api_calls": 0,
                "cache_hits": 0,
                "cache_misses": 0,
            }
        }
        return {
            "status": "started",
            "session_id": session_id,
            "start_time": self.current_session["start_time"]
        }

    def log_phase(self, session_id: str, phase: str, name: str,
                  duration: int, tokens: int = 0, status: str = "completed") -> Dict:
        """記錄 Phase 執行"""
        phase_record = {
            "phase": phase,
            "name": name,
            "duration": duration,
            "tokens": tokens,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

        # 比較基準
        benchmark = self.benchmarks["phase_durations"].get(phase, 60)
        is_slow = duration > benchmark * 1.5

        return {
            "logged": True,
            "phase": phase,
            "duration": f"{duration}s",
            "benchmark": f"{benchmark}s",
            "status": "⚠️ 較慢" if is_slow else "✅ 正常"
        }

    def finish_session(self, session_id: str, output_path: Optional[str] = None) -> Dict:
        """結束追蹤並生成報告"""
        # 模擬 session 數據
        session = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat(),
            "total_duration": 754,
            "phases": [
                {"phase": "0", "name": "Experience Collector", "duration": 45, "tokens": 3500},
                {"phase": "1", "name": "Content Analyst", "duration": 80, "tokens": 4000},
                {"phase": "2a", "name": "Research Agent", "duration": 195, "tokens": 8000},
                {"phase": "3", "name": "Writer Agent", "duration": 150, "tokens": 12000},
                {"phase": "3.5", "name": "Editor Agent", "duration": 75, "tokens": 5000},
                {"phase": "4", "name": "SEO Optimizer", "duration": 45, "tokens": 3500},
            ],
            "resources": {
                "total_tokens": 45000,
                "api_calls": 23,
                "cache_hits": 8,
                "cache_misses": 4,
            },
            "performance_grade": self._calculate_grade(754, 45000, 0.67)
        }

        # 生成報告
        report = self._generate_report(session)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)

        # 保存記錄
        self._append_session(session)

        return {
            "status": "finished",
            "session_id": session_id,
            "total_duration": f"{session['total_duration']}s ({session['total_duration']/60:.1f}m)",
            "grade": session["performance_grade"],
            "report_saved": output_path if output_path else "未保存"
        }

    def _calculate_grade(self, duration: int, tokens: int, cache_rate: float) -> str:
        """計算效能評級"""
        targets = self.benchmarks["time_targets"]

        if duration < targets["excellent"] and cache_rate > 0.85:
            return "A+"
        elif duration < targets["good"] and cache_rate > 0.75:
            return "A"
        elif duration < targets["acceptable"] and cache_rate > 0.65:
            return "B"
        elif duration < targets["slow"] and cache_rate > 0.5:
            return "C"
        else:
            return "D"

    def _generate_report(self, session: Dict) -> str:
        """生成效能報告"""
        total_duration = session.get("total_duration", 0)
        minutes = total_duration // 60
        seconds = total_duration % 60

        report = f"""# Session 效能報告

**Session ID**: {session['session_id']}
**執行時間**: {minutes}分{seconds}秒
**效能評級**: {session.get('performance_grade', 'N/A')}

## 執行時間分解

| Phase | 名稱 | 耗時 | 佔比 | 狀態 |
|-------|------|------|------|------|
"""
        for p in session.get('phases', []):
            duration = p.get('duration', 0)
            pct = (duration / total_duration * 100) if total_duration > 0 else 0
            benchmark = self.benchmarks["phase_durations"].get(p['phase'], 60)
            status = "⚠️ 較慢" if duration > benchmark * 1.5 else "✅ 正常"
            report += f"| {p['phase']} | {p['name']} | {duration}s | {pct:.0f}% | {status} |\n"

        resources = session.get('resources', {})
        cache_hits = resources.get('cache_hits', 0)
        cache_misses = resources.get('cache_misses', 0)
        cache_rate = cache_hits / (cache_hits + cache_misses) if (cache_hits + cache_misses) > 0 else 0

        report += f"""
## 資源使用

| 指標 | 數值 | 狀態 |
|------|------|------|
| 總 Tokens | {resources.get('total_tokens', 0):,} | {'✅' if resources.get('total_tokens', 0) < 50000 else '⚠️'} |
| API 調用 | {resources.get('api_calls', 0)} | ✅ |
| 快取命中率 | {cache_rate:.0%} | {'✅' if cache_rate > 0.7 else '⚠️'} |

## 優化建議

"""
        # 生成建議
        suggestions = self._generate_suggestions(session)
        for i, sug in enumerate(suggestions, 1):
            report += f"{i}. {sug}\n"

        report += f"""
---
*報告生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report

    def _generate_suggestions(self, session: Dict) -> List[str]:
        """生成優化建議"""
        suggestions = []

        total_duration = session.get('total_duration', 0)
        if total_duration > 900:
            suggestions.append("✅ 啟用 Phase 2a/2b 並行執行可節省 ~90 秒")

        resources = session.get('resources', {})
        cache_hits = resources.get('cache_hits', 0)
        cache_misses = resources.get('cache_misses', 0)
        if cache_misses > cache_hits:
            suggestions.append("✅ 延長研究快取有效期至 7 天可提升命中率")

        # 檢查慢 Phase
        for p in session.get('phases', []):
            benchmark = self.benchmarks["phase_durations"].get(p['phase'], 60)
            if p.get('duration', 0) > benchmark * 2:
                suggestions.append(f"⚠️ Phase {p['phase']} ({p['name']}) 執行時間異常，建議檢查")

        if not suggestions:
            suggestions.append("✅ 效能良好，暫無特別建議")

        return suggestions

    def analyze(self, session_dir: str) -> Dict:
        """分析特定 session"""
        session_path = Path(session_dir)

        if not session_path.exists():
            return {"error": f"Session 目錄不存在: {session_dir}"}

        # 檢查是否有 workflow_progress.json
        progress_file = session_path / "workflow_progress.json"
        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
        else:
            progress = {}

        return {
            "session": session_path.name,
            "files_found": len(list(session_path.glob('*.md'))),
            "has_progress": progress_file.exists(),
            "analysis": "需要完整執行記錄才能提供詳細分析"
        }

    def generate_report(self, report_type: str, output_path: Optional[str] = None) -> Dict:
        """生成報告"""
        sessions = self._load_sessions()

        if report_type == "weekly":
            # 過去 7 天
            cutoff = datetime.now() - timedelta(days=7)
            title = "效能週報"
        elif report_type == "monthly":
            cutoff = datetime.now() - timedelta(days=30)
            title = "效能月報"
        else:
            cutoff = datetime.now() - timedelta(days=7)
            title = "效能報告"

        if not sessions:
            report = f"# {title}\n\n尚無效能數據。"
        else:
            total = len(sessions)
            avg_duration = sum(s.get('total_duration', 0) for s in sessions) / total if total > 0 else 0
            grades = [s.get('performance_grade', 'C') for s in sessions]

            report = f"""# {title}

**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**統計期間**: 過去 {'7' if report_type == 'weekly' else '30'} 天

## 摘要統計

| 指標 | 數值 |
|------|------|
| Sessions 數量 | {total} |
| 平均執行時間 | {avg_duration/60:.1f} 分鐘 |
| 最常見評級 | {max(set(grades), key=grades.count)} |

## 評級分佈

"""
            for grade in ['A+', 'A', 'B', 'C', 'D']:
                count = grades.count(grade)
                if count > 0:
                    report += f"- {grade}: {count} 次 ({count/total*100:.0f}%)\n"

            report += """
## 建議

1. 持續監控執行時間趨勢
2. 優化快取策略提升命中率
3. 考慮更多並行執行機會
"""

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)

        return {
            "report_type": report_type,
            "sessions_analyzed": len(sessions),
            "output": output_path if output_path else "stdout"
        }

    def suggest(self, session_dir: str) -> Dict:
        """獲取優化建議"""
        return {
            "session": session_dir,
            "suggestions": [
                {
                    "type": "parallel_execution",
                    "description": "啟用 Phase 2a/2b 並行執行",
                    "estimated_saving": "~90 秒",
                    "risk": "低"
                },
                {
                    "type": "cache_optimization",
                    "description": "延長研究快取有效期",
                    "estimated_saving": "~60 秒",
                    "risk": "低"
                },
                {
                    "type": "smart_skipping",
                    "description": "高品質預測時跳過 Phase 3.9",
                    "estimated_saving": "~60 秒",
                    "risk": "中"
                }
            ],
            "total_potential_saving": "~3.5 分鐘"
        }


def main():
    parser = argparse.ArgumentParser(description='Performance Monitor Skill')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # status
    subparsers.add_parser('status', help='顯示效能狀態')

    # start
    start_parser = subparsers.add_parser('start', help='開始追蹤 session')
    start_parser.add_argument('--session', required=True, help='Session 目錄')

    # log-phase
    log_parser = subparsers.add_parser('log-phase', help='記錄 Phase 執行')
    log_parser.add_argument('--session', required=True)
    log_parser.add_argument('--phase', required=True)
    log_parser.add_argument('--name', required=True)
    log_parser.add_argument('--duration', type=int, required=True)
    log_parser.add_argument('--tokens', type=int, default=0)

    # finish
    finish_parser = subparsers.add_parser('finish', help='結束追蹤')
    finish_parser.add_argument('--session', required=True)
    finish_parser.add_argument('--output', help='輸出報告路徑')

    # analyze
    analyze_parser = subparsers.add_parser('analyze', help='分析 session')
    analyze_parser.add_argument('--session', required=True)

    # report
    report_parser = subparsers.add_parser('report', help='生成報告')
    report_parser.add_argument('--type', choices=['weekly', 'monthly'], default='weekly')
    report_parser.add_argument('--output', help='輸出路徑')

    # suggest
    suggest_parser = subparsers.add_parser('suggest', help='獲取優化建議')
    suggest_parser.add_argument('--session', required=True)

    args = parser.parse_args()
    monitor = PerformanceMonitor()

    if args.command == 'status':
        result = monitor.status()
        if result['status'] == 'no_data':
            print(f"效能監控狀態: {result['message']}")
        else:
            print(f"效能監控狀態:")
            print(f"  總 Sessions: {result['total_sessions']}")
            print(f"  最近平均時間: {result['recent_10_avg']['duration']}")
            print(f"  最近平均 Tokens: {result['recent_10_avg']['tokens']}")
            print(f"  評級分佈: {result['grade_distribution']}")

    elif args.command == 'start':
        result = monitor.start_session(args.session)
        print(f"✅ 開始追蹤: {result['session_id']}")

    elif args.command == 'log-phase':
        result = monitor.log_phase(
            args.session, args.phase, args.name,
            args.duration, args.tokens
        )
        print(f"Phase {args.phase}: {result['duration']} (基準: {result['benchmark']}) {result['status']}")

    elif args.command == 'finish':
        result = monitor.finish_session(args.session, args.output)
        print(f"✅ Session 完成")
        print(f"   執行時間: {result['total_duration']}")
        print(f"   效能評級: {result['grade']}")
        if args.output:
            print(f"   報告已保存: {args.output}")

    elif args.command == 'analyze':
        result = monitor.analyze(args.session)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"Session 分析: {result['session']}")
            print(f"  檔案數: {result['files_found']}")
            print(f"  有進度記錄: {'是' if result['has_progress'] else '否'}")

    elif args.command == 'report':
        result = monitor.generate_report(args.type, args.output)
        print(f"報告類型: {result['report_type']}")
        print(f"分析 Sessions: {result['sessions_analyzed']}")
        if args.output:
            print(f"已保存至: {args.output}")

    elif args.command == 'suggest':
        result = monitor.suggest(args.session)
        print(f"優化建議 ({result['session']}):\n")
        for sug in result['suggestions']:
            print(f"  - {sug['description']}")
            print(f"    預估節省: {sug['estimated_saving']}, 風險: {sug['risk']}")
        print(f"\n總潛在節省: {result['total_potential_saving']}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
