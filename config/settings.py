"""設定関連の定数を管理するモジュール"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration constants
SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')
PRIVATE_KEY_FILE = os.getenv('PRIVATE_KEY_FILE')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BASE_API_URL = "https://www.worksapis.com/v1.0"
AUTH_URL = "https://auth.worksmobile.com/oauth2/v2.0/token"
BOT_ID = "10087978"
