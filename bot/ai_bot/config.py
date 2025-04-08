import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")  # путь к JSON-файлу
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
