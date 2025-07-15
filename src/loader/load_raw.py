import psycopg2
import os
import json

conn = psycopg2.connect(
    host="localhost",
    database="your_db",
    user="your_user",
    password="your_pass"
)
cur = conn.cursor()

for root, dirs, files in os.walk("data/raw/telegram_messages"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    cur.execute(
                        """
                        INSERT INTO raw.telegram_messages (message_id, message, date, has_media)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (msg["id"], msg["message"], msg["date"], "media" in msg)
                    )

conn.commit()
cur.close()
conn.close()
