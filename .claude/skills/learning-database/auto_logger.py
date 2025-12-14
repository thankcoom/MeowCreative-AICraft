#!/usr/bin/env python3
"""
Session 自動記錄器 v2.5.0
========================

自動從 Session 輸出中提取學習數據，更新 Memory 系統。

功能：
- 自動解析 workflow_progress.json
- 提取品質分數和模式
- 更新成功/失敗模式庫
- 記錄 Session 歷史

使用方式：
---------
# 記錄單個 Session
python3 auto_logger.py log --session output/session_20251123_142834

# 批次學習所有歷史 Session
python3 auto_logger.py batch-learn --from-sessions "output/session_*"

# 生成學習報告
python3 auto_logger.py report --type weekly
"""

import argparse
import json
import re
import glob
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

# 添加父目錄到路徑以便導入
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from base import BaseSkill, SkillException, ValidationError
except ImportError:
    # Fallback 如果基類不可用
    class BaseSkill:
        def __init__(self, *args, **kwargs):
            self.logger = self._setup_logger()
        def _setup_logger(self):
            import logging
            logging.basicConfig(level=logging.INFO)
            return logging.getLogger(__name__)
    class SkillException(Exception):
        pass
    class ValidationError(Exception):
        pass


class SessionAutoLogger(BaseSkill):
    """Session 自動記錄器"""

    SKILL_NAME = "session-auto-logger"
    VERSION = "1.0.0"

    # 記憶體路徑
    MEMORY_DIR = Path(__file__).parent.parent.parent / "memory"
    PATTERNS_DIR = MEMORY_DIR / "patterns"
    HISTORY_DIR = MEMORY_DIR / "history"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()

    def _ensure_directories(self):
        """確保必要目錄存在"""
        self.PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
        self.HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    def _execute(self, session_dir: str) -> dict:
        """執行 Session 記錄"""
        return self.log_session(session_dir)

    def log_session(self, session_dir: str) -> dict:
        """
        記錄單個 Session

        Args:
            session_dir: Session 目錄路徑

        Returns:
            記錄結果
        """
        session_path = Path(session_dir)

        if not session_path.exists():
            raise ValidationError(f"Session directory not found: {session_dir}")

        self.logger.info(f"Logging session: {session_dir}")

        result = {
            'session_id': session_path.name,
            'logged_at': datetime.now().isoformat(),
            'extracted': {}
        }

        # 1. 解析 workflow_progress.json
        progress = self._parse_progress(session_path)
        if progress:
            result['extracted']['progress'] = progress
            self._record_history(session_path.name, progress)

        # 2. 提取品質分數
        scores = self._extract_scores(session_path)
        if scores:
            result['extracted']['scores'] = scores

        # 3. 識別成功/失敗模式
        patterns = self._identify_patterns(session_path, scores)
        if patterns:
            result['extracted']['patterns'] = patterns
            self._update_patterns(patterns)

        # 4. 提取寫作風格特徵
        style_features = self._extract_style_features(session_path)
        if style_features:
            result['extracted']['style'] = style_features

        self.logger.info(f"Session logged successfully: {result['session_id']}")
        return result

    def _parse_progress(self, session_path: Path) -> Optional[dict]:
        """解析 workflow_progress.json"""
        progress_file = session_path / "workflow_progress.json"

        if not progress_file.exists():
            self.logger.warning(f"No workflow_progress.json found in {session_path}")
            return None

        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to parse progress: {e}")
            return None

    def _extract_scores(self, session_path: Path) -> dict:
        """從各報告中提取品質分數"""
        scores = {}

        # 從 editor_review.md 提取分數
        editor_review = session_path / "editor_review.md"
        if editor_review.exists():
            content = editor_review.read_text(encoding='utf-8')
            scores['editor'] = self._extract_score_from_content(content, 'editor')

        # 從 seo_report.md 提取分數
        seo_report = session_path / "seo_report.md"
        if seo_report.exists():
            content = seo_report.read_text(encoding='utf-8')
            scores['seo'] = self._extract_score_from_content(content, 'seo')

        # 從 validation_report.json 提取分數
        validation_report = session_path / "validation_report.json"
        if validation_report.exists():
            try:
                with open(validation_report, 'r', encoding='utf-8') as f:
                    validation = json.load(f)
                    if 'overall_score' in validation:
                        scores['overall'] = validation['overall_score']
                    if 'phase_scores' in validation:
                        scores['phases'] = validation['phase_scores']
            except Exception as e:
                self.logger.warning(f"Failed to parse validation report: {e}")

        return scores

    def _extract_score_from_content(self, content: str, score_type: str) -> Optional[float]:
        """從內容中提取分數"""
        patterns = [
            r'總分[：:]\s*(\d+(?:\.\d+)?)',
            r'分數[：:]\s*(\d+(?:\.\d+)?)',
            r'Score[：:]\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*/\s*100',
            r'評分[：:]\s*(\d+(?:\.\d+)?)',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return float(match.group(1))

        return None

    def _identify_patterns(self, session_path: Path, scores: dict) -> List[dict]:
        """識別成功/失敗模式"""
        patterns = []
        overall_score = scores.get('overall') or scores.get('editor', 0)

        # 讀取草稿
        draft_file = session_path / "draft_final.md"
        if not draft_file.exists():
            return patterns

        try:
            content = draft_file.read_text(encoding='utf-8')
        except Exception:
            return patterns

        # 分析開頭模式
        opening_pattern = self._analyze_opening(content, overall_score)
        if opening_pattern:
            patterns.append(opening_pattern)

        # 分析結構模式
        structure_pattern = self._analyze_structure(content, overall_score)
        if structure_pattern:
            patterns.append(structure_pattern)

        # 分析 CTA 模式
        cta_pattern = self._analyze_cta(content, overall_score)
        if cta_pattern:
            patterns.append(cta_pattern)

        return patterns

    def _analyze_opening(self, content: str, score: float) -> Optional[dict]:
        """分析開頭模式"""
        lines = content.split('\n')
        first_paragraph = ""

        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                first_paragraph = line
                break

        if not first_paragraph:
            return None

        # 識別開頭類型
        opening_type = "unknown"
        if first_paragraph.endswith('?') or first_paragraph.endswith('？'):
            opening_type = "question"
        elif any(word in first_paragraph for word in ['你是否', '有沒有', '想不想', '曾經']):
            opening_type = "empathy_question"
        elif any(word in first_paragraph for word in ['數據', '研究', '報告', '%']):
            opening_type = "data_hook"
        elif any(word in first_paragraph for word in ['故事', '記得', '那天', '當時']):
            opening_type = "story_hook"

        pattern_type = "success" if score >= 70 else "failed"

        return {
            'id': self._generate_pattern_id(f"opening_{opening_type}"),
            'type': pattern_type,
            'category': 'opening',
            'pattern': opening_type,
            'description': f"開頭使用{opening_type}模式",
            'example': first_paragraph[:200],
            'context': [],
            'metrics': {
                'usage_count': 1,
                'success_rate': 1.0 if score >= 70 else 0.0,
                'avg_score': score
            },
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

    def _analyze_structure(self, content: str, score: float) -> Optional[dict]:
        """分析結構模式"""
        # 計算標題數量和層級
        h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
        h3_count = len(re.findall(r'^### ', content, re.MULTILINE))

        # 計算段落數量
        paragraphs = [p for p in content.split('\n\n') if p.strip()]

        structure_type = "flat"
        if h2_count >= 5 and h3_count >= 3:
            structure_type = "deep_hierarchy"
        elif h2_count >= 3:
            structure_type = "standard_hierarchy"
        elif len(paragraphs) > 10:
            structure_type = "long_form"

        pattern_type = "success" if score >= 70 else "failed"

        return {
            'id': self._generate_pattern_id(f"structure_{structure_type}"),
            'type': pattern_type,
            'category': 'structure',
            'pattern': structure_type,
            'description': f"文章結構: {structure_type}",
            'example': f"H1:{h1_count}, H2:{h2_count}, H3:{h3_count}, Paragraphs:{len(paragraphs)}",
            'context': [],
            'metrics': {
                'usage_count': 1,
                'success_rate': 1.0 if score >= 70 else 0.0,
                'avg_score': score
            },
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

    def _analyze_cta(self, content: str, score: float) -> Optional[dict]:
        """分析 CTA 模式"""
        cta_patterns = [
            r'立即', r'馬上', r'現在就', r'點擊', r'下載',
            r'訂閱', r'加入', r'開始', r'免費', r'試試看'
        ]

        cta_count = sum(len(re.findall(pattern, content)) for pattern in cta_patterns)

        if cta_count == 0:
            return None

        cta_type = "none"
        if cta_count >= 5:
            cta_type = "aggressive"
        elif cta_count >= 2:
            cta_type = "moderate"
        else:
            cta_type = "subtle"

        pattern_type = "success" if score >= 70 else "failed"

        return {
            'id': self._generate_pattern_id(f"cta_{cta_type}"),
            'type': pattern_type,
            'category': 'cta',
            'pattern': cta_type,
            'description': f"CTA 強度: {cta_type} (count: {cta_count})",
            'example': f"CTA 出現 {cta_count} 次",
            'context': [],
            'metrics': {
                'usage_count': 1,
                'success_rate': 1.0 if score >= 70 else 0.0,
                'avg_score': score
            },
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

    def _extract_style_features(self, session_path: Path) -> dict:
        """提取寫作風格特徵"""
        draft_file = session_path / "draft_final.md"
        if not draft_file.exists():
            return {}

        try:
            content = draft_file.read_text(encoding='utf-8')
        except Exception:
            return {}

        # 計算各種特徵
        words = re.findall(r'[\u4e00-\u9fff]+', content)
        sentences = re.split(r'[。！？.!?]', content)

        features = {
            'word_count': len(''.join(words)),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_sentence_length': len(''.join(words)) / max(len(sentences), 1),
            'question_count': content.count('?') + content.count('？'),
            'exclamation_count': content.count('!') + content.count('！'),
            'list_count': len(re.findall(r'^[-*]\s', content, re.MULTILINE)),
            'code_block_count': len(re.findall(r'```', content)) // 2
        }

        return features

    def _generate_pattern_id(self, base: str) -> str:
        """生成唯一的 pattern ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_input = f"{base}_{timestamp}"
        return f"pattern_{hashlib.md5(hash_input.encode()).hexdigest()[:8]}"

    def _update_patterns(self, new_patterns: List[dict]) -> None:
        """更新模式庫"""
        for pattern in new_patterns:
            pattern_type = pattern['type']
            file_path = self.PATTERNS_DIR / f"{pattern_type}.json"

            # 載入現有模式
            existing = {'patterns': [], 'metadata': {'version': '1.0.0'}}
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                except Exception:
                    pass

            # 檢查是否有相似模式
            updated = False
            for i, existing_pattern in enumerate(existing['patterns']):
                if (existing_pattern['category'] == pattern['category'] and
                    existing_pattern['pattern'] == pattern['pattern']):
                    # 更新現有模式
                    existing['patterns'][i]['metrics']['usage_count'] += 1
                    old_rate = existing['patterns'][i]['metrics']['success_rate']
                    old_count = existing['patterns'][i]['metrics']['usage_count'] - 1
                    new_rate = pattern['metrics']['success_rate']
                    # 計算新的平均成功率
                    existing['patterns'][i]['metrics']['success_rate'] = (
                        (old_rate * old_count + new_rate) / (old_count + 1)
                    )
                    existing['patterns'][i]['updated_at'] = datetime.now().isoformat()
                    updated = True
                    break

            if not updated:
                existing['patterns'].append(pattern)

            # 儲存更新
            existing['metadata']['updated'] = datetime.now().isoformat()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Updated {pattern_type} pattern: {pattern['category']}/{pattern['pattern']}")

    def _record_history(self, session_id: str, progress: dict) -> None:
        """記錄 Session 歷史"""
        history_file = self.HISTORY_DIR / "sessions.jsonl"

        record = {
            'session_id': session_id,
            'logged_at': datetime.now().isoformat(),
            'progress': progress
        }

        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

        self.logger.info(f"Recorded session history: {session_id}")

    def batch_learn(self, sessions_pattern: str = "output/session_*") -> dict:
        """
        從所有歷史 Session 批次學習

        Args:
            sessions_pattern: Session 目錄匹配模式

        Returns:
            學習結果摘要
        """
        # 找出所有已記錄的 session
        history_file = self.HISTORY_DIR / "sessions.jsonl"
        logged_sessions = set()

        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        logged_sessions.add(record['session_id'])
                    except Exception:
                        pass

        # 找出所有 session 目錄
        session_dirs = glob.glob(sessions_pattern)
        self.logger.info(f"Found {len(session_dirs)} sessions, {len(logged_sessions)} already logged")

        results = {
            'total_found': len(session_dirs),
            'already_logged': len(logged_sessions),
            'newly_logged': 0,
            'failed': 0,
            'sessions': []
        }

        for session_dir in session_dirs:
            session_name = Path(session_dir).name

            if session_name in logged_sessions:
                self.logger.debug(f"Skipping already logged: {session_name}")
                continue

            try:
                result = self.log_session(session_dir)
                results['newly_logged'] += 1
                results['sessions'].append({
                    'session_id': session_name,
                    'status': 'success',
                    'patterns': len(result.get('extracted', {}).get('patterns', []))
                })
            except Exception as e:
                self.logger.error(f"Failed to log {session_name}: {e}")
                results['failed'] += 1
                results['sessions'].append({
                    'session_id': session_name,
                    'status': 'failed',
                    'error': str(e)
                })

        self.logger.info(f"Batch learning complete: {results['newly_logged']} new, {results['failed']} failed")
        return results

    def generate_report(self, report_type: str = "weekly") -> str:
        """生成學習報告"""
        report_lines = [
            f"# 學習報告 ({report_type})",
            f"\n**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "---\n"
        ]

        # 讀取模式統計
        success_patterns = self._load_patterns("success")
        failed_patterns = self._load_patterns("failed")

        report_lines.append("## 模式統計\n")
        report_lines.append(f"- 成功模式數: {len(success_patterns)}")
        report_lines.append(f"- 失敗模式數: {len(failed_patterns)}\n")

        # 高成功率模式
        if success_patterns:
            report_lines.append("## 高效模式 (成功率 > 70%)\n")
            high_success = [p for p in success_patterns if p['metrics']['success_rate'] >= 0.7]
            for pattern in sorted(high_success, key=lambda x: -x['metrics']['success_rate'])[:10]:
                report_lines.append(
                    f"- **{pattern['category']}/{pattern['pattern']}**: "
                    f"成功率 {pattern['metrics']['success_rate']:.1%}, "
                    f"使用 {pattern['metrics']['usage_count']} 次"
                )

        # Session 歷史
        history_file = self.HISTORY_DIR / "sessions.jsonl"
        if history_file.exists():
            session_count = sum(1 for _ in open(history_file, 'r'))
            report_lines.append(f"\n## Session 歷史\n")
            report_lines.append(f"- 已記錄 Session 數: {session_count}")

        return '\n'.join(report_lines)

    def _load_patterns(self, pattern_type: str) -> List[dict]:
        """載入指定類型的模式"""
        file_path = self.PATTERNS_DIR / f"{pattern_type}.json"
        if not file_path.exists():
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('patterns', [])
        except Exception:
            return []


def main():
    parser = argparse.ArgumentParser(
        description="Session 自動記錄器 v2.5.0",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # log 命令
    log_parser = subparsers.add_parser('log', help='記錄單個 Session')
    log_parser.add_argument('--session', '-s', required=True, help='Session 目錄路徑')

    # batch-learn 命令
    batch_parser = subparsers.add_parser('batch-learn', help='批次學習所有歷史 Session')
    batch_parser.add_argument('--from-sessions', '-f', default='output/session_*',
                              help='Session 目錄匹配模式')

    # report 命令
    report_parser = subparsers.add_parser('report', help='生成學習報告')
    report_parser.add_argument('--type', '-t', default='weekly',
                               choices=['daily', 'weekly', 'monthly'],
                               help='報告類型')
    report_parser.add_argument('--output', '-o', help='輸出檔案路徑')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    logger = SessionAutoLogger(debug=True)

    if args.command == 'log':
        result = logger.log_session(args.session)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'batch-learn':
        result = logger.batch_learn(args.from_sessions)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'report':
        report = logger.generate_report(args.type)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        else:
            print(report)


if __name__ == '__main__':
    main()
