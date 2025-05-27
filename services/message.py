"""メッセージ送信関連の処理を管理するモジュール"""
import requests
import logging
from urllib.parse import quote
from config.settings import BASE_API_URL

def send_message(content: dict, bot_id: str, user_id: str, access_token: str) -> None:
    """ボットメッセージを送信します。

    Args:
        content: メッセージの内容
        bot_id: ボットのID
        user_id: 送信先ユーザーID
        access_token: アクセストークン

    Raises:
        requests.exceptions.RequestException: APIリクエストが失敗した場合
        requests.exceptions.ConnectionError: ネットワークエラーが発生した場合
    """
    logger = logging.getLogger(__name__)
    encoded_user_id = quote(user_id)
    url = f"{BASE_API_URL}/bots/{bot_id}/users/{encoded_user_id}/messages"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    body = {
        "content": content
    }

    try:
        response = requests.post(url=url, json=body, headers=headers)
        response.raise_for_status()  # ステータスコードが4xx/5xxの場合は例外を発生
        logger.info("メッセージ送信成功: %s", response.text)
    except requests.exceptions.ConnectionError as e:
        logger.error("ネットワークエラーが発生しました: %s", e)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("APIエラーが発生しました: %s", e)
        if hasattr(e, 'response') and e.response is not None:
            logger.error("エラーレスポンス: %s", e.response.text)
        raise
