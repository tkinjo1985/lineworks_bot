"""メッセージ送信関連の処理を管理するモジュール"""
from typing import Dict, Any

from .api import APIClient
from .logger import logger

def send_message(content: Dict[str, Any], bot_id: str, user_id: str, access_token: str) -> Dict[str, Any]:
    """ボットメッセージを送信します。

    Args:
        content: メッセージの内容
        bot_id: ボットのID
        user_id: 送信先ユーザーID
        access_token: アクセストークン

    Returns:
        Dict[str, Any]: APIレスポンス

    Raises:
        requests.exceptions.RequestException: APIリクエストが失敗した場合
        requests.exceptions.ConnectionError: ネットワークエラーが発生した場合
    """
    logger.info(f"メッセージ送信開始: ユーザー {user_id}")
    
    # APIクライアントを初期化してメッセージ送信
    api_client = APIClient(access_token)
    return api_client.send_bot_message(bot_id, user_id, content)
