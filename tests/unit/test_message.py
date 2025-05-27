"""メッセージ送信機能のテスト"""
import pytest
import requests
from services.message import send_message
from urllib.parse import quote


@pytest.fixture
def message_content():
    """テスト用のメッセージコンテンツ"""
    return {
        "type": "text",
        "text": "テストメッセージ"
    }


class TestSendMessage:
    """send_message関数のテストケース"""

    def test_success(self, message_content, requests_mock, caplog):
        """正常系：メッセージ送信が成功する"""
        # テストデータ
        bot_id = "test_bot"
        user_id = "test_user@example.com"
        access_token = "dummy_token"
        encoded_user_id = quote(user_id)

        # APIモック
        requests_mock.post(
            f"https://www.worksapis.com/v1.0/bots/{bot_id}/users/{encoded_user_id}/messages",
            json={"status": "success"}
        )

        # テスト実行
        send_message(
            content=message_content,
            bot_id=bot_id,
            user_id=user_id,
            access_token=access_token
        )

        # リクエストの検証
        history = requests_mock.request_history[0]
        assert history.headers['Content-Type'] == 'application/json'
        assert history.headers['Authorization'] == f'Bearer {access_token}'
        assert history.json() == {"content": message_content}

    def test_api_error(self, message_content, requests_mock, caplog):
        """異常系：APIリクエストが失敗する"""
        bot_id = "test_bot"
        user_id = "test_user@example.com"
        access_token = "dummy_token"
        encoded_user_id = quote(user_id)

        # 500エラーをモック
        requests_mock.post(
            f"https://www.worksapis.com/v1.0/bots/{bot_id}/users/{encoded_user_id}/messages",
            status_code=500
        )

        # テスト実行
        with pytest.raises(requests.exceptions.RequestException):
            send_message(
                content=message_content,
                bot_id=bot_id,
                user_id=user_id,
                access_token=access_token
            )
        assert "APIエラー" in caplog.text

    def test_invalid_user_id(self, message_content, requests_mock, caplog):
        """異常系：不正なユーザーID"""
        bot_id = "test_bot"
        user_id = "invalid user"  # スペースを含む不正なID
        access_token = "dummy_token"
        encoded_user_id = quote(user_id)

        # APIモック
        requests_mock.post(
            f"https://www.worksapis.com/v1.0/bots/{bot_id}/users/{encoded_user_id}/messages",
            status_code=400  # 不正なリクエストとしてモック
        )

        # テスト実行
        with pytest.raises(requests.exceptions.RequestException):
            send_message(
                content=message_content,
                bot_id=bot_id,
                user_id=user_id,
                access_token=access_token
            )

    def test_network_error(self, message_content, requests_mock, caplog):
        """異常系：ネットワークエラー"""
        bot_id = "test_bot"
        user_id = "test_user@example.com"
        access_token = "dummy_token"

        # ネットワークエラーをモック
        requests_mock.post(
            f"https://www.worksapis.com/v1.0/bots/{bot_id}/users/{quote(user_id)}/messages",
            exc=requests.exceptions.ConnectionError
        )

        # テスト実行
        with pytest.raises(requests.exceptions.ConnectionError):
            send_message(
                content=message_content,
                bot_id=bot_id,
                user_id=user_id,
                access_token=access_token
            )
        assert "ネットワークエラー" in caplog.text
