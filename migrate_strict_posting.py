from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    print(f"Connecting to {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Dropping unused columns from posting table...")
        columns_to_drop = ['state', 'category', 'rank', 'mandate']
        
        for col in columns_to_drop:
            try:
                print(f"Dropping column {col}...")
                conn.execute(text(f"ALTER TABLE posting DROP COLUMN IF EXISTS {col}"))
                conn.commit()
                print(f"Dropped {col}")
            except Exception as e:
                print(f"Error dropping {col}: {e}")
                conn.rollback()

if __name__ == "__main__":
    migrate()
