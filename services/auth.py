"""認証関連の処理を管理するモジュール"""
import jwt
import time
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from config.settings import CLIENT_ID, SERVICE_ACCOUNT, CLIENT_SECRET, AUTH_URL

def get_private_key(key_path: str) -> bytes:
    """秘密鍵ファイルを読み込み、秘密鍵オブジェクトを返します。

    Args:
        key_path (str): 秘密鍵ファイルのパス

    Returns:
        bytes: 読み込んだ秘密鍵オブジェクト

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
                print(f"秘密鍵ファイルの形式が不正です: {e}")
                raise
    except FileNotFoundError:
        print(f"秘密鍵ファイルが見つかりません: {key_path}")
        raise
    except PermissionError:
        print(f"秘密鍵ファイルへのアクセス権がありません: {key_path}")
        raise
    except Exception as e:
        print(f"秘密鍵の読み込み中に予期せぬエラーが発生しました: {e}")
        raise

def get_access_token(private_key: bytes) -> str:
    """JWTトークンを生成し、アクセストークンを取得します。

    Args:
        private_key: 秘密鍵データ

    Returns:
        str: アクセストークン
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
        print(f"トークン取得に失敗しました: {e}")
        return None
