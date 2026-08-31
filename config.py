import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]
OLLAMA_API_KEY = os.environ["OLLAMA_API_KEY"]
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
