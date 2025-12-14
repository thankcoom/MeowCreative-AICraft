"""
Skill 基類模組 v2.5.0
=====================

提供統一的：
- 錯誤處理
- 日誌記錄
- 配置載入
- 重試機制
- 效能追蹤

所有 Skill 應繼承 BaseSkill 類別以獲得這些功能。

使用範例:
---------
```python
from claude.skills.base import BaseSkill, SkillException

class MySkill(BaseSkill):
    def _execute(self, input_file: str) -> dict:
        # 實現具體邏輯
        return {"result": "success"}
```
"""

from abc import ABC, abstractmethod
import logging
import json
import yaml
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional, Callable
from functools import wraps

# ============================================================
# 異常類別
# ============================================================

class SkillException(Exception):
    """Skill 異常基類"""
    def __init__(self, message: str, skill_name: str = None, details: dict = None):
        self.message = message
        self.skill_name = skill_name
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "skill": self.skill_name,
            "details": self.details,
            "timestamp": self.timestamp
        }


class ValidationError(SkillException):
    """輸入驗證錯誤"""
    pass


class ConfigurationError(SkillException):
    """配置錯誤"""
    pass


class APIError(SkillException):
    """API 調用錯誤"""
    def __init__(self, message: str, status_code: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.status_code = status_code


class MCPConnectionError(SkillException):
    """MCP 連接錯誤"""
    pass


class FileOperationError(SkillException):
    """檔案操作錯誤"""
    pass


class TimeoutError(SkillException):
    """超時錯誤"""
    pass


# ============================================================
# 裝飾器
# ============================================================

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0,
          exceptions: tuple = (Exception,)):
    """
    重試裝飾器

    Args:
        max_attempts: 最大重試次數
        delay: 初始延遲秒數
        backoff: 延遲倍數
        exceptions: 需要重試的異常類型
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator


def timed(func: Callable) -> Callable:
    """執行時間追蹤裝飾器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        # 如果是類別方法且有 logger
        if args and hasattr(args[0], 'logger'):
            args[0].logger.debug(f"{func.__name__} executed in {duration:.2f}s")

        return result
    return wrapper


# ============================================================
# 基類
# ============================================================

class BaseSkill(ABC):
    """
    所有 Skill 的基類

    提供：
    - 統一的日誌記錄
    - 配置載入
    - 錯誤處理
    - 效能追蹤

    子類必須實現 _execute() 方法
    """

    # 類別變數
    SKILL_NAME: str = "base"
    VERSION: str = "1.0.0"

    # 日誌目錄
    LOG_DIR = Path(__file__).parent.parent.parent / "logs"

    def __init__(self, config_path: Optional[str] = None, debug: bool = False):
        """
        初始化 Skill

        Args:
            config_path: 配置檔案路徑
            debug: 是否啟用除錯模式
        """
        self.debug = debug
        self.logger = self._setup_logger()
        self.config = self._load_config(config_path)
        self._execution_stats = []

    def _setup_logger(self) -> logging.Logger:
        """設定日誌"""
        # 確保日誌目錄存在
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(f"skill.{self.SKILL_NAME}")

        # 避免重複添加 handler
        if not logger.handlers:
            # 檔案 handler - 所有 skill 共用
            file_handler = logging.FileHandler(
                self.LOG_DIR / "skills.log",
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)

            # 錯誤專用 handler
            error_handler = logging.FileHandler(
                self.LOG_DIR / "errors.log",
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)

            # 格式設定
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            error_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(error_handler)

            # Debug 模式加入 console handler
            if self.debug:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            logger.setLevel(logging.DEBUG if self.debug else logging.INFO)

        return logger

    def _load_config(self, config_path: Optional[str]) -> dict:
        """載入配置"""
        default_config = {
            'retry_enabled': True,
            'max_retries': 3,
            'retry_delay': 1.0,
            'timeout': 300,  # 5 分鐘
            'track_performance': True
        }

        if config_path is None:
            return default_config

        path = Path(config_path)
        if not path.exists():
            self.logger.warning(f"Config file not found: {config_path}, using defaults")
            return default_config

        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    user_config = yaml.safe_load(f)
                elif path.suffix == '.json':
                    user_config = json.load(f)
                else:
                    self.logger.warning(f"Unknown config format: {path.suffix}")
                    return default_config

            # 合併配置
            return {**default_config, **(user_config or {})}

        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return default_config

    def execute(self, *args, **kwargs) -> Any:
        """
        統一執行入口

        包含：
        - 日誌記錄
        - 效能追蹤
        - 錯誤處理
        - 重試機制
        """
        execution_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        start_time = time.time()

        self.logger.info(f"[{execution_id}] Starting {self.SKILL_NAME} v{self.VERSION}")
        self.logger.debug(f"[{execution_id}] Args: {args}, Kwargs: {kwargs}")

        try:
            # 驗證輸入
            self._validate_input(*args, **kwargs)

            # 執行核心邏輯
            result = self._execute(*args, **kwargs)

            # 記錄執行統計
            duration = time.time() - start_time
            self._record_stats(execution_id, duration, True)

            self.logger.info(f"[{execution_id}] Completed in {duration:.2f}s")
            return result

        except SkillException as e:
            duration = time.time() - start_time
            self._record_stats(execution_id, duration, False, str(e))
            self.logger.error(f"[{execution_id}] Failed: {e}")

            # 嘗試重試
            if self.config.get('retry_enabled') and self._should_retry(e):
                self.logger.info(f"[{execution_id}] Attempting retry...")
                return self._retry_execute(*args, **kwargs)

            raise

        except Exception as e:
            duration = time.time() - start_time
            self._record_stats(execution_id, duration, False, str(e))
            self.logger.error(f"[{execution_id}] Unexpected error: {e}", exc_info=True)
            raise SkillException(
                f"Unexpected error in {self.SKILL_NAME}: {e}",
                skill_name=self.SKILL_NAME,
                details={'original_error': str(e)}
            )

    def _validate_input(self, *args, **kwargs) -> None:
        """
        驗證輸入

        子類可覆寫此方法實現自定義驗證
        """
        pass

    @abstractmethod
    def _execute(self, *args, **kwargs) -> Any:
        """
        核心執行邏輯

        子類必須實現此方法
        """
        pass

    def _should_retry(self, exception: Exception) -> bool:
        """
        判斷是否應該重試

        預設：API 錯誤和超時可以重試
        """
        return isinstance(exception, (APIError, TimeoutError))

    def _retry_execute(self, *args, **kwargs) -> Any:
        """重試執行"""
        max_retries = self.config.get('max_retries', 3)
        delay = self.config.get('retry_delay', 1.0)

        for attempt in range(max_retries):
            try:
                self.logger.info(f"Retry attempt {attempt + 1}/{max_retries}")
                time.sleep(delay * (attempt + 1))  # 遞增延遲
                return self._execute(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                self.logger.warning(f"Retry {attempt + 1} failed: {e}")

        raise SkillException(f"All {max_retries} retries failed", skill_name=self.SKILL_NAME)

    def _record_stats(self, execution_id: str, duration: float,
                      success: bool, error: str = None) -> None:
        """記錄執行統計"""
        if not self.config.get('track_performance', True):
            return

        stats = {
            'execution_id': execution_id,
            'skill': self.SKILL_NAME,
            'version': self.VERSION,
            'duration': duration,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }

        if error:
            stats['error'] = error

        self._execution_stats.append(stats)

        # 寫入效能日誌
        perf_log = self.LOG_DIR / "performance.log"
        try:
            with open(perf_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(stats, ensure_ascii=False) + '\n')
        except Exception as e:
            self.logger.warning(f"Failed to write performance log: {e}")

    def get_stats(self) -> list:
        """取得執行統計"""
        return self._execution_stats.copy()

    # ============================================================
    # 工具方法
    # ============================================================

    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """安全讀取檔案"""
        path = Path(file_path)
        if not path.exists():
            raise FileOperationError(
                f"File not found: {file_path}",
                skill_name=self.SKILL_NAME
            )

        try:
            return path.read_text(encoding=encoding)
        except Exception as e:
            raise FileOperationError(
                f"Failed to read file: {e}",
                skill_name=self.SKILL_NAME,
                details={'file': file_path}
            )

    def write_file(self, file_path: str, content: str,
                   encoding: str = 'utf-8') -> None:
        """安全寫入檔案"""
        path = Path(file_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=encoding)
            self.logger.debug(f"Written to {file_path}")
        except Exception as e:
            raise FileOperationError(
                f"Failed to write file: {e}",
                skill_name=self.SKILL_NAME,
                details={'file': file_path}
            )

    def load_json(self, file_path: str) -> dict:
        """載入 JSON 檔案"""
        content = self.read_file(file_path)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValidationError(
                f"Invalid JSON: {e}",
                skill_name=self.SKILL_NAME,
                details={'file': file_path}
            )

    def save_json(self, file_path: str, data: dict, indent: int = 2) -> None:
        """儲存 JSON 檔案"""
        content = json.dumps(data, ensure_ascii=False, indent=indent)
        self.write_file(file_path, content)

    def load_yaml(self, file_path: str) -> dict:
        """載入 YAML 檔案"""
        content = self.read_file(file_path)
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValidationError(
                f"Invalid YAML: {e}",
                skill_name=self.SKILL_NAME,
                details={'file': file_path}
            )


# ============================================================
# 匯出
# ============================================================

__all__ = [
    # 基類
    'BaseSkill',

    # 異常
    'SkillException',
    'ValidationError',
    'ConfigurationError',
    'APIError',
    'MCPConnectionError',
    'FileOperationError',
    'TimeoutError',

    # 裝飾器
    'retry',
    'timed'
]
