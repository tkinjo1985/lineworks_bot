"""APIクライアントのテスト"""
import pytest
import requests
from unittest.mock import patch, MagicMock

from services.api import APIClient


class TestAPIClient:
    """APIClient クラスのテストケース"""

    @pytest.fixture
    def api_client(self):
        """テスト用のAPIクライアントを生成"""
        return APIClient("dummy_token")

    def test_initialization(self, api_client):
        """初期化が正しく行われることを検証"""
        assert api_client.access_token == "dummy_token"
        assert api_client.headers == {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer dummy_token'
        }

    def test_make_request_get(self, api_client, requests_mock):
        """GET リクエストが正しく行われることを検証"""
        requests_mock.get(
            "https://www.worksapis.com/v1.0/test-endpoint",
            json={"status": "success"}
        )
        
        result = api_client._make_request("GET", "/test-endpoint")
        
        assert result == {"status": "success"}
        assert requests_mock.request_history[0].method == "GET"
        assert requests_mock.request_history[0].headers["Authorization"] == "Bearer dummy_token"

    def test_make_request_post(self, api_client, requests_mock):
        """POST リクエストが正しく行われることを検証"""
        test_data = {"key": "value"}
        requests_mock.post(
            "https://www.worksapis.com/v1.0/test-endpoint",
            json={"status": "created"}
        )
        
        result = api_client._make_request("POST", "/test-endpoint", test_data)
        
        assert result == {"status": "created"}
        assert requests_mock.request_history[0].method == "POST"
        assert requests_mock.request_history[0].json() == test_data

    def test_make_request_unsupported_method(self, api_client):
        """サポートされていないHTTPメソッドの検証"""
        with pytest.raises(ValueError, match="サポートされていないHTTPメソッド"):
            api_client._make_request("UNSUPPORTED", "/test")

    def test_make_request_connection_error(self, api_client, requests_mock):
        """ネットワークエラー発生時の挙動検証"""
        requests_mock.get(
            "https://www.worksapis.com/v1.0/test-endpoint",
            exc=requests.exceptions.ConnectionError
        )
        
        with pytest.raises(requests.exceptions.ConnectionError):
            api_client._make_request("GET", "/test-endpoint")

    def test_make_request_api_error(self, api_client, requests_mock):
        """APIエラー発生時の挙動検証"""
        requests_mock.get(
            "https://www.worksapis.com/v1.0/test-endpoint",
            status_code=500,
            text="Internal Server Error"
        )
        
        with pytest.raises(requests.exceptions.RequestException):
            api_client._make_request("GET", "/test-endpoint")

    def test_send_bot_message(self, api_client, requests_mock):
        """send_bot_message メソッドの検証"""
        bot_id = "test_bot"
        user_id = "test_user@example.com"
        content = {"type": "text", "text": "テストメッセージ"}
        
        # URLエンコードされたユーザーIDを含むURLになることを確認
        requests_mock.post(
            f"https://www.worksapis.com/v1.0/bots/{bot_id}/users/test_user%40example.com/messages",
            json={"messageId": "123456"}
        )
        
        result = api_client.send_bot_message(bot_id, user_id, content)
        
        assert result == {"messageId": "123456"}
        assert requests_mock.request_history[0].json() == {"content": content}

    def test_get_bot_info(self, api_client, requests_mock):
        """get_bot_info メソッドの検証"""
        bot_id = "test_bot"
        bot_info = {"name": "テストボット", "photoUrl": "http://example.com/bot.jpg"}
        
        requests_mock.get(
            f"https://www.worksapis.com/v1.0/bots/{bot_id}",
            json=bot_info
        )
        
        result = api_client.get_bot_info(bot_id)
        
        assert result == bot_info