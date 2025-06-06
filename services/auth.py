"""認証関連の処理を管理するモジュール"""
import jwt
import time
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from typing import Optional, Any

from config.settings import CLIENT_ID, SERVICE_ACCOUNT, CLIENT_SECRET, AUTH_URL
from .logger import logger

def get_private_key(key_path: str) -> Optional[Any]:
    """秘密鍵ファイルを読み込み、秘密鍵オブジェクトを返します。

    Args:
        key_path (str): 秘密鍵ファイルのパス

    Returns:
        Optional[Any]: 読み込んだ秘密鍵オブジェクト、エラー時はNone

    Raises:
        FileNotFoundError: 秘密鍵ファイルが見つからない場合
        PermissionError: 秘密鍵ファイルにアクセス権がない場合
        ValueError: 秘密鍵ファイルの形式が不正な場合
        Exception: その他のエラーが発生した場合
    """
    try:
        with open(key_path, 'rb') as key_file:
            key_data = key_file.read()
            try:
                return serialization.load_pem_private_key(
                    key_data,
                    password=None,
                    backend=default_backend()
                )
            except ValueError as e:
                logger.error(f"秘密鍵ファイルの形式が不正です: {e}")
                raise
    except FileNotFoundError:
        logger.error(f"秘密鍵ファイルが見つかりません: {key_path}")
        raise
    except PermissionError:
        logger.error(f"秘密鍵ファイルへのアクセス権がありません: {key_path}")
        raise
    except Exception as e:
        logger.error(f"秘密鍵の読み込み中に予期せぬエラーが発生しました: {e}")
        raise

def get_access_token(private_key: Any) -> Optional[str]:
    """JWTトークンを生成し、アクセストークンを取得します。

    Args:
        private_key: 秘密鍵データ

    Returns:
        Optional[str]: アクセストークン。エラー時はNone
    """
    # JWTペイロード作成
    now = int(time.time())
    payload = {
        "iss": CLIENT_ID,
        "sub": SERVICE_ACCOUNT,
        "iat": now,
        "exp": now + 3600,
    }

    # JWT生成（RS256署名）
    jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

    # アクセストークン取得のためのリクエスト
    try:
        response = requests.post(
            AUTH_URL,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'assertion': jwt_token,
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'scope': 'bot bot.message',
            }
        )
        response.raise_for_status()  # エラーレスポンスの場合は例外を発生
        return response.json()['access_token']
    except requests.RequestException as e:
        logger.error(f"トークン取得に失敗しました: {e}")
        return None
    except KeyError as e:
        logger.error(f"トークン取得のレスポンスが不正です: {e}")
        return None
