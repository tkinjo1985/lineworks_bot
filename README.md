# LINEWORKS Bot

LINEWORKSのBot APIを使用してメッセージを送信するためのPythonライブラリです。

## 機能

- JWT認証を使用したアクセストークンの取得
- ボットメッセージの送信
- エラーハンドリングとログ出力

## 必要要件

- Python 3.10以上
- 以下のPythonパッケージ:
  - `PyJWT`
  - `requests`
  - `cryptography`
  - `python-dotenv`

## インストール

1. リポジトリをクローン:
```bash
git clone https://github.com/yourusername/lineworks-bot.git
cd lineworks-bot
```

2. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
`.env`ファイルを作成し、以下の変数を設定:
```
SERVICE_ACCOUNT=your_service_account
PRIVATE_KEY_FILE=path_to_your_private_key
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
BOT_ID=your_bot_id
```

## 使用方法

基本的な使用例:

```python
from main import main

# メッセージを送信
send_bot_message(user_id='user@example.com', message='Hello, LINEWORKS!')
```

## プロジェクト構造

```
.
├── config/
│   └── settings.py    # 設定関連
├── services/
│   ├── auth.py        # 認証関連
│   └── message.py     # メッセージ送信関連
└── main.py            # メインスクリプト
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
詳細は[LICENSE.md](LICENSE.md)をご覧ください。

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 注意事項

- このライブラリはLINEWORKS APIの仕様変更により動作しなくなる可能性があります。
- 本番環境で使用する前に十分なテストを行ってください。
- 秘密鍵ファイルは適切に管理してください。
