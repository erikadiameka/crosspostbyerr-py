import os
from pathlib import Path
from dotenv import load_dotenv

# Ambil path direktori utama proyek (root directory)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load file .env jika ada
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Konfigurasi Global Variables
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
TIKTOK_SESSION_ID = os.getenv("TIKTOK_SESSION_ID")
APP_ENV = os.getenv("APP_ENV", "development")