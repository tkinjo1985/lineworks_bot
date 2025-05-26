"""LINEWORKSボットのメインスクリプト"""
from config.settings import PRIVATE_KEY_FILE, BOT_ID
from services.auth import get_private_key, get_access_token
from services.message import send_message


def send_bot_message(user_id: str, message: str) -> None:
    """LINEWORKSボットを使用してメッセージを送信します。

    このメインの実行関数は以下の処理を行います：
    1. 秘密鍵を読み込み
    2. アクセストークンを取得
    3. 指定されたユーザーにメッセージを送信

    Args:
        user_id (str): メッセージを送信する対象のユーザーID（例：'user@domain'）
        message (str): 送信するメッセージの内容

    Returns:
        None: この関数は戻り値を返しません

    Note:
        アクセストークンの取得に失敗した場合、メッセージは送信されません。
    """
    try:
        private_key = get_private_key(PRIVATE_KEY_FILE)
        if not private_key:
            print("秘密鍵の取得に失敗しました")
            return

        access_token = get_access_token(private_key)
        if not access_token:
            print("アクセストークンの取得に失敗しました")
            return
        
        send_message(
            content={
                "type": "text",
                "text": message
            },
            bot_id=BOT_ID,
            user_id=user_id,
            access_token=access_token
        )
    except Exception as e:
        print(f"メッセージ送信処理中にエラーが発生しました: {e}")
        return
    
if __name__ == "__main__":
    # 例として、ユーザーIDとメッセージを指定して実行
    user_id = "xxx@xxx"
    message = "こんにちは！これはテストメッセージです。"
    send_bot_message(user_id, message)