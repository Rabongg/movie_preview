import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
SENDER_KEY: str = os.getenv("SENDER_KEY", "")
RECEIVER_EMAILS: list[str] = [
    e.strip() for e in os.getenv("RECEIVER_EMAILS", "").split(",") if e.strip()
]
SEND_HOUR_MORNING: int = int(os.getenv("SEND_HOUR_MORNING", "9"))
SEND_HOUR_AFTERNOON: int = int(os.getenv("SEND_HOUR_AFTERNOON", "15"))
