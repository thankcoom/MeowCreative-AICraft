#!/usr/bin/env python3
"""
效能追蹤器 v2.5.0
=================

即時追蹤 Session 執行效能，生成效能報告和優化建議。

功能：
- Session 執行時間追蹤
- Phase 級別效能分析
- 效能評級計算
- 優化建議生成
- 歷史趨勢分析

使用方式：
---------
# 啟動追蹤
python3 tracker.py start --session-id session_20251211_120000

# 記錄 Phase
python3 tracker.py phase-start --phase 3
python3 tracker.py phase-end --phase 3 --success

# 生成報告
python3 tracker.py report --session-id session_20251211_120000

# 建立基準
python3 tracker.py calibrate --from-sessions "output/session_*"
"""

import argparse
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import glob
import statistics

# 添加父目錄到路徑
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from base import BaseSkill, SkillException
except ImportError:
    class BaseSkill:
        def __init__(self, *args, **kwargs):
            self.logger = self._setup_logger()
        def _setup_logger(self):
            import logging
            logging.basicConfig(level=logging.INFO)
            return logging.getLogger(__name__)
    class SkillException(Exception):
        pass


class PerformanceTracker(BaseSkill):
    """效能追蹤器"""

    SKILL_NAME = "performance-tracker"
    VERSION = "1.0.0"

    # 效能數據目錄
    PERF_DIR = Path(__file__).parent.parent.parent / "performance"

    # 效能評級標準
    GRADE_CRITERIA = {
        'A+': {'max_duration': 480, 'min_cache_rate': 0.85},   # < 8 分鐘
        'A':  {'max_duration': 600, 'min_cache_rate': 0.75},   # < 10 分鐘
        'B':  {'max_duration': 900, 'min_cache_rate': 0.65},   # < 15 分鐘
        'C':  {'max_duration': 1200, 'min_cache_rate': 0.50},  # < 20 分鐘
        'D':  {'max_duration': float('inf'), 'min_cache_rate': 0}
    }

    # Phase 基準時間 (秒)
    PHASE_BENCHMARKS = {
        '0': 60,    # Experience Collector
        '1': 45,    # Content Analyst
        '2a': 90,   # Research Agent
        '2b': 60,   # Style Matcher
        '3': 180,   # Writer Agent
        '3.4': 30,  # Quality Predictor
        '3.5': 90,  # Editor Agent
        '3.6': 60,  # Fact Checker
        '3.7': 60,  # Humanizer
        '3.8': 60,  # Persuasion
        '3.9': 60,  # Storyteller
        '4': 90,    # SEO Optimizer
        '5': 30,    # Publisher
        '11': 30,   # Memory Agent
        '12': 120,  # Persona Adapter
        '13': 15,   # Performance Optimizer
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()
        self._current_session = None
        self._phases = []
        self._start_time = None

    def _ensure_directories(self):
        """確保必要目錄存在"""
        self.PERF_DIR.mkdir(parents=True, exist_ok=True)
        (self.PERF_DIR / "dashboard").mkdir(exist_ok=True)

    def _execute(self, *args, **kwargs) -> dict:
        """BaseSkill 需要的抽象方法"""
        return {}

    def start_session(self, session_id: str) -> dict:
        """
        開始追蹤 Session

        Args:
            session_id: Session ID

        Returns:
            追蹤狀態
        """
        self._current_session = session_id
        self._start_time = datetime.now()
        self._phases = []

        self.logger.info(f"Started tracking session: {session_id}")

        return {
            'session_id': session_id,
            'start_time': self._start_time.isoformat(),
            'status': 'tracking'
        }

    def phase_start(self, phase_id: str) -> dict:
        """
        記錄 Phase 開始

        Args:
            phase_id: Phase ID

        Returns:
            Phase 狀態
        """
        phase = {
            'phase': phase_id,
            'start': datetime.now().isoformat(),
            'start_ts': time.time()
        }

        self._phases.append(phase)
        self.logger.info(f"Phase {phase_id} started")

        return phase

    def phase_end(self, phase_id: str, success: bool = True,
                  metadata: dict = None) -> dict:
        """
        記錄 Phase 結束

        Args:
            phase_id: Phase ID
            success: 是否成功
            metadata: 額外元數據

        Returns:
            Phase 結果
        """
        # 找到對應的 Phase
        phase = None
        for p in self._phases:
            if p['phase'] == phase_id and 'end' not in p:
                phase = p
                break

        if not phase:
            self.logger.warning(f"Phase {phase_id} not found or already ended")
            return {}

        end_time = datetime.now()
        phase['end'] = end_time.isoformat()
        phase['end_ts'] = time.time()
        phase['duration'] = phase['end_ts'] - phase['start_ts']
        phase['success'] = success

        if metadata:
            phase['metadata'] = metadata

        # 計算與基準的比較
        benchmark = self.PHASE_BENCHMARKS.get(phase_id, 60)
        phase['benchmark'] = benchmark
        phase['efficiency'] = benchmark / max(phase['duration'], 1)

        self.logger.info(
            f"Phase {phase_id} ended: {phase['duration']:.1f}s "
            f"(benchmark: {benchmark}s, efficiency: {phase['efficiency']:.2f})"
        )

        return phase

    def end_session(self, success: bool = True) -> dict:
        """
        結束 Session 追蹤並生成報告

        Args:
            success: Session 是否成功

        Returns:
            效能報告
        """
        if not self._current_session:
            return {'error': 'No active session'}

        end_time = datetime.now()
        total_duration = (end_time - self._start_time).total_seconds()

        # 計算統計
        phase_durations = [p.get('duration', 0) for p in self._phases if 'duration' in p]
        successful_phases = sum(1 for p in self._phases if p.get('success', False))

        report = {
            'session_id': self._current_session,
            'start_time': self._start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_duration': total_duration,
            'success': success,
            'phases': self._phases,
            'statistics': {
                'total_phases': len(self._phases),
                'successful_phases': successful_phases,
                'failed_phases': len(self._phases) - successful_phases,
                'avg_phase_duration': statistics.mean(phase_durations) if phase_durations else 0,
                'max_phase_duration': max(phase_durations) if phase_durations else 0,
                'min_phase_duration': min(phase_durations) if phase_durations else 0
            },
            'grade': self._calculate_grade(total_duration),
            'bottlenecks': self._identify_bottlenecks(),
            'suggestions': self._generate_suggestions(total_duration)
        }

        # 儲存報告
        self._save_session_report(report)

        # 更新趨勢數據
        self._update_trends(report)

        self.logger.info(
            f"Session {self._current_session} ended: "
            f"{total_duration:.1f}s, Grade: {report['grade']}"
        )

        # 重置狀態
        self._current_session = None
        self._phases = []
        self._start_time = None

        return report

    def _calculate_grade(self, duration: float, cache_rate: float = 0) -> str:
        """計算效能評級"""
        for grade, criteria in self.GRADE_CRITERIA.items():
            if duration <= criteria['max_duration']:
                return grade
        return 'D'

    def _identify_bottlenecks(self) -> List[dict]:
        """識別效能瓶頸"""
        bottlenecks = []

        for phase in self._phases:
            if 'duration' not in phase:
                continue

            benchmark = self.PHASE_BENCHMARKS.get(phase['phase'], 60)
            if phase['duration'] > benchmark * 1.5:  # 超過基準 50%
                bottlenecks.append({
                    'phase': phase['phase'],
                    'duration': phase['duration'],
                    'benchmark': benchmark,
                    'excess': phase['duration'] - benchmark,
                    'severity': 'high' if phase['duration'] > benchmark * 2 else 'medium'
                })

        return sorted(bottlenecks, key=lambda x: x['excess'], reverse=True)

    def _generate_suggestions(self, total_duration: float) -> List[str]:
        """生成優化建議"""
        suggestions = []

        # 根據總時間建議
        if total_duration > 900:  # > 15 分鐘
            suggestions.append("考慮啟用並行執行 Phase 2a 和 2b")

        # 根據瓶頸建議
        bottlenecks = self._identify_bottlenecks()
        for bn in bottlenecks[:3]:  # 前 3 個瓶頸
            phase = bn['phase']
            if phase == '2a':
                suggestions.append("Research Agent 耗時較長，考慮使用快取或縮小研究範圍")
            elif phase == '3':
                suggestions.append("Writer Agent 耗時較長，考慮簡化大綱或使用範本")
            elif phase == '4':
                suggestions.append("SEO Optimizer 耗時較長，考慮減少關鍵字分析數量")

        # 根據 Phase 數量建議
        if len(self._phases) > 10:
            suggestions.append("執行了較多 Phase，考慮使用 Quality Predictor 跳過低優先級 Phase")

        if not suggestions:
            suggestions.append("效能表現良好，繼續保持！")

        return suggestions

    def _save_session_report(self, report: dict) -> None:
        """儲存 Session 報告"""
        # 追加到 sessions.jsonl
        sessions_file = self.PERF_DIR / "sessions.jsonl"
        with open(sessions_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(report, ensure_ascii=False) + '\n')

    def _update_trends(self, report: dict) -> None:
        """更新趨勢數據"""
        trends_file = self.PERF_DIR / "trends.json"

        # 載入現有趨勢
        trends = {
            'updated_at': datetime.now().isoformat(),
            'sessions': [],
            'averages': {}
        }

        if trends_file.exists():
            try:
                with open(trends_file, 'r', encoding='utf-8') as f:
                    trends = json.load(f)
            except Exception:
                pass

        # 添加新數據點
        trends['sessions'].append({
            'session_id': report['session_id'],
            'timestamp': report['end_time'],
            'duration': report['total_duration'],
            'grade': report['grade'],
            'phase_count': report['statistics']['total_phases']
        })

        # 只保留最近 100 個
        trends['sessions'] = trends['sessions'][-100:]

        # 計算滾動平均
        if len(trends['sessions']) >= 5:
            recent = trends['sessions'][-5:]
            trends['averages'] = {
                'duration_5': statistics.mean([s['duration'] for s in recent]),
                'phase_count_5': statistics.mean([s['phase_count'] for s in recent])
            }

        if len(trends['sessions']) >= 20:
            recent = trends['sessions'][-20:]
            trends['averages']['duration_20'] = statistics.mean([s['duration'] for s in recent])

        trends['updated_at'] = datetime.now().isoformat()

        # 儲存
        with open(trends_file, 'w', encoding='utf-8') as f:
            json.dump(trends, f, ensure_ascii=False, indent=2)

    def calibrate(self, sessions_pattern: str = "output/session_*") -> dict:
        """
        從歷史 Session 建立效能基準

        Args:
            sessions_pattern: Session 目錄匹配模式

        Returns:
            校準結果
        """
        session_dirs = glob.glob(sessions_pattern)
        self.logger.info(f"Calibrating from {len(session_dirs)} sessions")

        phase_times = {}  # phase_id -> list of durations

        for session_dir in session_dirs:
            progress_file = Path(session_dir) / "workflow_progress.json"
            if not progress_file.exists():
                continue

            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)

                # 支援兩種格式：dict 或 list
                phases_data = progress.get('phases', {})

                # 如果是 dict 格式 (v2.0.0+)
                if isinstance(phases_data, dict):
                    for phase_key, phase_info in phases_data.items():
                        if not isinstance(phase_info, dict):
                            continue
                        # 從 phase_key 提取 ID (例如 "phase_0" -> "0")
                        phase_id = phase_key.replace('phase_', '').replace('_', '.')

                        # 計算 duration
                        started = phase_info.get('started_at')
                        completed = phase_info.get('completed_at')
                        if started and completed:
                            try:
                                start_dt = datetime.fromisoformat(started)
                                end_dt = datetime.fromisoformat(completed)
                                duration = (end_dt - start_dt).total_seconds()
                                if duration > 0:  # 忽略負值或零
                                    if phase_id not in phase_times:
                                        phase_times[phase_id] = []
                                    phase_times[phase_id].append(duration)
                            except Exception:
                                pass
                # 如果是 list 格式
                elif isinstance(phases_data, list):
                    for phase in phases_data:
                        phase_id = str(phase.get('phase', ''))
                        duration = phase.get('duration')
                        if phase_id and duration:
                            if phase_id not in phase_times:
                                phase_times[phase_id] = []
                            phase_times[phase_id].append(duration)

            except Exception as e:
                self.logger.warning(f"Failed to parse {session_dir}: {e}")

        # 計算基準
        benchmarks = {}
        for phase_id, times in phase_times.items():
            if len(times) >= 3:
                benchmarks[phase_id] = {
                    'mean': statistics.mean(times),
                    'median': statistics.median(times),
                    'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                    'samples': len(times)
                }

        # 儲存基準
        benchmarks_file = self.PERF_DIR / "benchmarks.json"
        result = {
            'calibrated_at': datetime.now().isoformat(),
            'sessions_analyzed': len(session_dirs),
            'benchmarks': benchmarks
        }

        with open(benchmarks_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Calibration complete: {len(benchmarks)} phases benchmarked")
        return result

    def get_status(self) -> dict:
        """取得目前追蹤狀態"""
        sessions_file = self.PERF_DIR / "sessions.jsonl"
        trends_file = self.PERF_DIR / "trends.json"

        status = {
            'tracking_active': self._current_session is not None,
            'current_session': self._current_session,
            'sessions_logged': 0,
            'latest_grade': None,
            'avg_duration': None
        }

        # 計算已記錄的 session 數
        if sessions_file.exists():
            status['sessions_logged'] = sum(1 for _ in open(sessions_file, 'r'))

        # 讀取最新趨勢
        if trends_file.exists():
            try:
                with open(trends_file, 'r', encoding='utf-8') as f:
                    trends = json.load(f)
                    if trends.get('sessions'):
                        status['latest_grade'] = trends['sessions'][-1]['grade']
                    if trends.get('averages', {}).get('duration_5'):
                        status['avg_duration'] = trends['averages']['duration_5']
            except Exception:
                pass

        return status

    def generate_dashboard_data(self) -> dict:
        """生成儀表板數據"""
        trends_file = self.PERF_DIR / "trends.json"
        benchmarks_file = self.PERF_DIR / "benchmarks.json"

        data = {
            'generated_at': datetime.now().isoformat(),
            'trends': None,
            'benchmarks': None,
            'grade_distribution': {}
        }

        if trends_file.exists():
            with open(trends_file, 'r', encoding='utf-8') as f:
                data['trends'] = json.load(f)

            # 計算評級分布
            grades = [s['grade'] for s in data['trends'].get('sessions', [])]
            for grade in ['A+', 'A', 'B', 'C', 'D']:
                data['grade_distribution'][grade] = grades.count(grade)

        if benchmarks_file.exists():
            with open(benchmarks_file, 'r', encoding='utf-8') as f:
                data['benchmarks'] = json.load(f)

        return data


def main():
    parser = argparse.ArgumentParser(
        description="效能追蹤器 v2.5.0",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # start 命令
    start_parser = subparsers.add_parser('start', help='開始追蹤 Session')
    start_parser.add_argument('--session-id', '-s', required=True, help='Session ID')

    # phase-start 命令
    ps_parser = subparsers.add_parser('phase-start', help='記錄 Phase 開始')
    ps_parser.add_argument('--phase', '-p', required=True, help='Phase ID')

    # phase-end 命令
    pe_parser = subparsers.add_parser('phase-end', help='記錄 Phase 結束')
    pe_parser.add_argument('--phase', '-p', required=True, help='Phase ID')
    pe_parser.add_argument('--success', action='store_true', default=True, help='是否成功')
    pe_parser.add_argument('--failed', action='store_true', help='標記為失敗')

    # end 命令
    end_parser = subparsers.add_parser('end', help='結束 Session')
    end_parser.add_argument('--success', action='store_true', default=True)
    end_parser.add_argument('--failed', action='store_true')

    # status 命令
    subparsers.add_parser('status', help='取得追蹤狀態')

    # calibrate 命令
    cal_parser = subparsers.add_parser('calibrate', help='從歷史建立基準')
    cal_parser.add_argument('--from-sessions', '-f', default='output/session_*')

    # dashboard 命令
    dash_parser = subparsers.add_parser('dashboard', help='生成儀表板數據')
    dash_parser.add_argument('--output', '-o', help='輸出檔案')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    tracker = PerformanceTracker(debug=True)

    if args.command == 'start':
        result = tracker.start_session(args.session_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'phase-start':
        result = tracker.phase_start(args.phase)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'phase-end':
        success = not args.failed if hasattr(args, 'failed') else True
        result = tracker.phase_end(args.phase, success)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'end':
        success = not args.failed if hasattr(args, 'failed') else True
        result = tracker.end_session(success)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'status':
        result = tracker.get_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'calibrate':
        result = tracker.calibrate(args.from_sessions)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'dashboard':
        data = tracker.generate_dashboard_data()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Dashboard data saved to: {args.output}")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
