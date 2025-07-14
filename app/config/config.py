import os

from dotenv import load_dotenv

load_dotenv(override=True)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
BASE_URL = os.getenv("BASE_URL")
TELEGRAM_OTP_TOKEN = os.getenv("TELEGRAM_OTP_TOKEN")
TELEGRAM_OTP_URL = os.getenv("TELEGRAM_OTP_URL")
