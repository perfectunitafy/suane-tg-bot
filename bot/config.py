import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Ошибка: Переменная GEMINI_API_KEY не задана в .env файле.")
    sys.exit(1)

client = genai.Client(api_key=api_key)
