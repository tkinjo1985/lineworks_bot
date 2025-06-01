"""ロギング機能を提供するモジュール"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    """ロギング機能を提供するクラス"""

    _instance = None
    _initialized = False

    def __new__(cls):
        """シングルトンパターンを実装"""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初期化メソッド（シングルトンのため一度のみ実行）"""
        if not Logger._initialized:
            self._logger = logging.getLogger('lineworks_bot')
            self._logger.setLevel(logging.INFO)
            self._setup_handlers()
            Logger._initialized = True

    def _setup_handlers(self) -> None:
        """ログハンドラーの設定"""
        # フォーマッタを作成
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # コンソールハンドラー
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # ファイルハンドラー（ログディレクトリがある場合のみ）
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        if os.path.exists(log_dir):
            log_file = os.path.join(log_dir, 'lineworks_bot.log')
            file_handler = RotatingFileHandler(
                log_file, maxBytes=10485760, backupCount=5
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        """情報レベルのログを記録

        Args:
            message: ログメッセージ
        """
        self._logger.info(message)

    def debug(self, message: str) -> None:
        """デバッグレベルのログを記録

        Args:
            message: ログメッセージ
        """
        self._logger.debug(message)

    def warning(self, message: str) -> None:
        """警告レベルのログを記録

        Args:
            message: ログメッセージ
        """
        self._logger.warning(message)

    def error(self, message: str, exc_info: Optional[Exception] = None) -> None:
        """エラーレベルのログを記録

        Args:
            message: ログメッセージ
            exc_info: 例外情報（オプション）
        """
        self._logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: Optional[Exception] = None) -> None:
        """クリティカルレベルのログを記録

        Args:
            message: ログメッセージ
            exc_info: 例外情報（オプション）
        """
        self._logger.critical(message, exc_info=exc_info)


# シングルトンインスタンスをエクスポート
logger = Logger()