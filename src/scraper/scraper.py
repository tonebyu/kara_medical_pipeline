# src/scraper/scraper.py

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import os, json, datetime, logging

# Load secrets
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Channels to scrape
channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/CheMed123",
    "https://t.me/tikvahpharma",
]

# Today's date
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
json_base = f"data/raw/telegram_messages/{date_str}"
img_base = f"data/raw/images/{date_str}"
os.makedirs(json_base, exist_ok=True)
os.makedirs(img_base, exist_ok=True)

# Logging setup
logging.basicConfig(filename='scraper.log', level=logging.INFO)

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj

with TelegramClient("anon", api_id, api_hash) as client:
    for url in channels:
        try:
            entity = client.get_entity(url)
            messages = client.iter_messages(entity, limit=100)

            raw_data = []
            for msg in messages:
                raw_data.append(msg.to_dict())

                # Save image if exists
                if msg.media and isinstance(msg.media, MessageMediaPhoto):
                    filename = f"{entity.username}_{msg.id}.jpg"
                    filepath = os.path.join(img_base, filename)
                    client.download_media(msg.media, file=filepath)
                    print(f"📸 Saved image: {filepath}")
                    logging.info(f"Saved image from {url}: {filepath}")

            # Save messages as JSON
            json_path = os.path.join(json_base, f"{entity.username}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(raw_data, f, ensure_ascii=False, indent=2, default=serialize_datetime)
            print(f"✅ Saved JSON: {json_path}")
            logging.info(f"Saved messages from {url} to {json_path}")

        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
            print(f"❌ Error scraping {url}: {e}")
