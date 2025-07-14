# src/utils/config.py or main.py

from dotenv import load_dotenv
import os

# Load variables from .env into the environment
load_dotenv()

# Now you can safely use them
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
