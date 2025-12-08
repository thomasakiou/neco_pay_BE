from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    print(f"Connecting to {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            print("Renaming table payment_db to payment...")
            # Check if payment_db exists first
            result = conn.execute(text("SELECT to_regclass('public.payment_db')")).scalar()
            if result:
                conn.execute(text("ALTER TABLE payment_db RENAME TO payment"))
                conn.commit()
                print("Renamed table successfully.")
            else:
                print("Table 'payment_db' not found. It might have been renamed already.")
        except Exception as e:
            print(f"Error renaming table: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
