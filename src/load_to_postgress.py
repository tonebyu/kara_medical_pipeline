import pandas as pd
import json
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)

# Adjust this relative path according to your folder structure
base_path = "../data/raw/telegram_messages"

for date_folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, date_folder)
    if not os.path.isdir(folder_path):
        continue

    for file in os.listdir(folder_path):
        if file.endswith('.json'):
            file_path = os.path.join(folder_path, file)
            print(f"Loading file: {file_path}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON file {file_path}: {e}")
                continue

            # Normalize JSON data
            df = pd.json_normalize(data)

            # Prepare DataFrame with exact columns expected by the database
            df_out = pd.DataFrame({
                'file_source': file,
                'message_id': df.get('id'),
                'chat_id': df.get('peer_id.channel_id'),
                'message_text': df.get('message'),
                'timestamp': pd.to_datetime(df.get('date')),
                'forwarded_at': pd.to_datetime(df.get('fwd_from.date'))
            })

            # Insert into PostgreSQL table
            try:
                df_out.to_sql('telegram_messages', engine, schema='raw', if_exists='append', index=False)
                print(f"Inserted {len(df_out)} records from {file}")
            except Exception as e:
                print(f"Error inserting data from {file}: {e}")
