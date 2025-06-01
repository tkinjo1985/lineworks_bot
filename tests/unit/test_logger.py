"""ロガー機能のテスト"""
from unittest.mock import patch, MagicMock
import pytest
import os
import sys
import logging

from services.logger import Logger, logger


class TestLogger:
    """Logger クラスのテストケース"""

    def test_singleton(self):
        """シングルトンパターンが正しく実装されているか検証"""
        logger1 = Logger()
        logger2 = Logger()
        assert logger1 is logger2
        
    def test_exported_instance(self):
        """エクスポートされたloggerインスタンスが正しいか検証"""
        assert isinstance(logger, Logger)
        
    @patch('logging.getLogger')
    def test_logger_initialization(self, mock_get_logger):
        """ロガーが正しく初期化されるか検証"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Loggerの_initializedフラグをリセットして再初期化させる
        with patch.object(Logger, '_initialized', False):
            logger = Logger()
            
        mock_get_logger.assert_called_once_with('lineworks_bot')
        mock_logger.setLevel.assert_called_once_with(logging.INFO)
    
    @patch.object(Logger, '_setup_handlers')
    def test_init_called_once(self, mock_setup):
        """初期化メソッドが一度だけ呼ばれることを検証"""
        # Loggerの_initializedフラグをリセットして再初期化させる
        with patch.object(Logger, '_initialized', False):
            logger1 = Logger()
            logger2 = Logger()
            
        assert mock_setup.call_count == 1
        
    @patch('logging.StreamHandler')
    def test_console_handler(self, mock_stream_handler):
        """コンソールハンドラーが正しく設定されるか検証"""
        mock_handler = MagicMock()
        mock_stream_handler.return_value = mock_handler
        
        with patch.object(Logger, '_initialized', False):
            with patch.object(Logger, '_logger', MagicMock()) as mock_logger:
                logger = Logger()
                
        mock_stream_handler.assert_called_once_with(sys.stdout)
        mock_handler.setFormatter.assert_called_once()
        mock_logger.addHandler.assert_called_with(mock_handler)
        
    def test_log_methods(self):
        """各ログメソッドが正しく動作するか検証"""
        with patch.object(Logger, '_logger') as mock_logger:
            test_logger = Logger()
            
            test_logger.info("テスト情報ログ")
            mock_logger.info.assert_called_once_with("テスト情報ログ")
            
            test_logger.debug("テストデバッグログ")
            mock_logger.debug.assert_called_once_with("テストデバッグログ")
            
            test_logger.warning("テスト警告ログ")
            mock_logger.warning.assert_called_once_with("テスト警告ログ")
            
            test_logger.error("テストエラーログ")
            mock_logger.error.assert_called_once_with("テストエラーログ", exc_info=None)
            
            exception = Exception("テスト例外")
            test_logger.error("例外付きエラーログ", exception)
            mock_logger.error.assert_called_with("例外付きエラーログ", exc_info=exception)
            
            test_logger.critical("テストクリティカルログ")
            mock_logger.critical.assert_called_once_with("テストクリティカルログ", exc_info=None)