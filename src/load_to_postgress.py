import pandas as pd
import json
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)

base_path = 'data/raw/telegram_messages'
for date_folder in os.listdir(base_path):
    full_path = os.path.join(base_path, date_folder)
    for file in os.listdir(full_path):
        if file.endswith('.json'):
            with open(os.path.join(full_path, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
            df = pd.json_normalize(data)
            df.to_sql('telegram_messages', engine, schema='raw', if_exists='append', index=False)
