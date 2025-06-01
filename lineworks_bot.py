"""LINEWORKSボットのメインスクリプト"""

from config.settings import PRIVATE_KEY_FILE, BOT_ID
from services.auth import get_private_key, get_access_token
from services.message import send_message
from services.logger import logger


def send_bot_message(user_id: str, message: str) -> bool:
    """LINEWORKSボットを使用してメッセージを送信します。

    このメインの実行関数は以下の処理を行います：
    1. 秘密鍵を読み込み
    2. アクセストークンを取得
    3. 指定されたユーザーにメッセージを送信

    Args:
        user_id (str): メッセージを送信する対象のユーザーID（例：'user@domain'）
        message (str): 送信するメッセージの内容

    Returns:
        bool: 送信が成功した場合はTrue、失敗した場合はFalse

    Note:
        アクセストークンの取得に失敗した場合、メッセージは送信されません。
    """
    try:
        logger.info(f"メッセージ送信開始: ユーザー {user_id}")
        
        private_key = get_private_key(PRIVATE_KEY_FILE)
        if not private_key:
            logger.error("秘密鍵の取得に失敗しました")
            return False

        access_token = get_access_token(private_key)
        if not access_token:
            logger.error("アクセストークンの取得に失敗しました")
            return False
        
        send_message(
            content={
                "type": "text",
                "text": message
            },
            bot_id=BOT_ID,
            user_id=user_id,
            access_token=access_token
        )
        
        logger.info("メッセージ送信完了")
        return True
        
    except Exception as e:
        logger.error(f"メッセージ送信処理中にエラーが発生しました: {e}", exc_info=e)
        return False