"""Config."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

BASE_URL = os.getenv("FAVQS_BASE_URL", "https://favqs.com/api")
API_KEY = os.getenv("FAVQS_API_KEY", "YOUR_API_KEY_HERE")


def get_base_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f'Token token="{API_KEY}"'
    }


def get_auth_headers(user_token):
    headers = get_base_headers()
    headers["User-Token"] = user_token
    return headers
