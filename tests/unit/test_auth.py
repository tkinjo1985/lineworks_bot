"""認証関連機能のテスト"""
from unittest.mock import mock_open, patch
import pytest
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from services.auth import get_private_key, get_access_token


@pytest.fixture
def mock_private_key():
    """テスト用の秘密鍵を生成するフィクスチャ"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key


@pytest.fixture
def mock_pem_data(mock_private_key):
    """秘密鍵のPEMデータを生成するフィクスチャ"""
    return mock_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


class TestGetPrivateKey:
    """get_private_key関数のテストケース"""

    def test_success(self, mock_pem_data):
        """正常系：秘密鍵ファイルの読み込みが成功する"""
        with patch('builtins.open', mock_open(read_data=mock_pem_data)):
            result = get_private_key('dummy.key')
            assert isinstance(result, rsa.RSAPrivateKey)

    def test_file_not_found(self, caplog):
        """異常系：ファイルが存在しない"""
        with patch('builtins.open', side_effect=FileNotFoundError()):
            with pytest.raises(FileNotFoundError):
                get_private_key('not_exist.key')
            assert "秘密鍵ファイルが見つかりません" in caplog.text

    def test_permission_error(self, caplog):
        """異常系：ファイルにアクセス権がない"""
        with patch('builtins.open', side_effect=PermissionError()):
            with pytest.raises(PermissionError):
                get_private_key('no_permission.key')
            assert "秘密鍵ファイルへのアクセス権がありません" in caplog.text

    def test_invalid_key_format(self, caplog):
        """異常系：不正な形式の秘密鍵ファイル"""
        with patch('builtins.open', mock_open(read_data=b'invalid key data')):
            with pytest.raises(ValueError):
                get_private_key('invalid.key')
            assert "秘密鍵ファイルの形式が不正です" in caplog.text


class TestGetAccessToken:
    """get_access_token関数のテストケース"""

    def test_success(self, mock_private_key, requests_mock):
        """正常系：アクセストークンの取得が成功する"""
        mock_token = "dummy_access_token"
        requests_mock.post(
            'https://auth.worksmobile.com/oauth2/v2.0/token',
            json={'access_token': mock_token}
        )

        result = get_access_token(mock_private_key)
        assert result == mock_token

        # リクエストの検証
        history = requests_mock.request_history[0]
        assert history.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        
        # データにJWTトークンが含まれていることを確認
        # ボディデータをパースして検証
        from urllib.parse import parse_qs
        body_data = parse_qs(history.text)
        assert 'assertion' in body_data
        jwt_token = body_data['assertion'][0]

        # JWTトークンがデコード可能であることを確認
        decoded = jwt.decode(
            jwt_token,
            mock_private_key.public_key(),
            algorithms=['RS256'],
            options={"verify_signature": False}
        )
        assert "iss" in decoded
        assert "sub" in decoded
        assert "iat" in decoded
        assert "exp" in decoded

    def test_api_error(self, mock_private_key, requests_mock, caplog):
        """異常系：APIリクエストが失敗する"""
        requests_mock.post(
            'https://auth.worksmobile.com/oauth2/v2.0/token',
            status_code=500
        )

        result = get_access_token(mock_private_key)
        assert result is None
        assert "トークン取得に失敗しました" in caplog.text

    def test_invalid_response(self, mock_private_key, requests_mock, caplog):
        """異常系：APIレスポンスが不正"""
        requests_mock.post(
            'https://auth.worksmobile.com/oauth2/v2.0/token',
            json={}  # access_tokenが含まれていない
        )

        result = get_access_token(mock_private_key)
        assert result is None
        assert "トークン取得のレスポンスが不正です" in caplog.text
