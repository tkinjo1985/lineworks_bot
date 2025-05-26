"""メッセージ送信関連の処理を管理するモジュール"""
import requests
from urllib.parse import quote
from config.settings import BASE_API_URL

def send_message(content: dict, bot_id: str, user_id: str, access_token: str) -> None:
    """ボットメッセージを送信します。

    Args:
        content: メッセージの内容
        bot_id: ボットのID
        user_id: 送信先ユーザーID
        access_token: アクセストークン
    """
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
        response.raise_for_status()
        print("Success:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        if hasattr(e, 'response') and e.response is not None:
            print("Error response:", e.response.text)
