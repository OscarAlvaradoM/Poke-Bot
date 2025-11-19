# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_CREDS_PATH = os.getenv("GOOGLE_CREDS_PATH")