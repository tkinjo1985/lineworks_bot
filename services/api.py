"""LINEWORKS API通信を担当するモジュール"""
import requests
from typing import Dict, Any, Optional
from urllib.parse import quote

from .logger import logger
from config.settings import BASE_API_URL


class APIClient:
    """LINEWORKS APIとの通信を行うクラス"""

    def __init__(self, access_token: str):
        """APIクライアントの初期化

        Args:
            access_token: APIアクセストークン
        """
        self.access_token = access_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """API リクエストを実行する

        Args:
            method: HTTPメソッド（'GET', 'POST', 'PUT', 'DELETE'）
            endpoint: APIエンドポイント（例：'/bots/{bot_id}/users/{user_id}/messages'）
            data: リクエストボディ（省略可）

        Returns:
            Dict[str, Any]: レスポンスデータ

        Raises:
            requests.exceptions.ConnectionError: ネットワークエラー発生時
            requests.exceptions.RequestException: APIリクエストエラー発生時
        """
        url = f"{BASE_API_URL}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=self.headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=self.headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"サポートされていないHTTPメソッド: {method}")
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"ネットワークエラーが発生しました: {e}", exc_info=e)
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"APIエラーが発生しました: {e}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - レスポンス: {e.response.text}"
            logger.error(error_msg, exc_info=e)
            raise

    def send_bot_message(
        self, 
        bot_id: str, 
        user_id: str, 
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """ボットメッセージを送信する

        Args:
            bot_id: ボットID
            user_id: 送信先のユーザーID
            content: メッセージコンテンツ

        Returns:
            Dict[str, Any]: APIレスポンス
        """
        encoded_user_id = quote(user_id)
        endpoint = f"/bots/{bot_id}/users/{encoded_user_id}/messages"
        
        logger.info(f"ユーザー {user_id} へメッセージ送信開始")
        
        data = {
            "content": content
        }
        
        response = self._make_request('POST', endpoint, data)
        
        logger.info("メッセージ送信成功")
        return response

    def get_bot_info(self, bot_id: str) -> Dict[str, Any]:
        """ボット情報を取得する

        Args:
            bot_id: ボットID

        Returns:
            Dict[str, Any]: ボット情報
        """
        endpoint = f"/bots/{bot_id}"
        logger.info(f"ボット情報取得: {bot_id}")
        
        return self._make_request('GET', endpoint)