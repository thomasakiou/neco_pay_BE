from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    print(f"Connecting to {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        # Add rank column
        try:
            print("Adding rank column...")
            conn.execute(text("ALTER TABLE posting ADD COLUMN rank VARCHAR"))
            conn.commit() 
            print("Added rank column")
        except Exception as e:
            print(f"Error adding rank (might exist): {e}")
            conn.rollback()

        # Add mandate column
        try:
            print("Adding mandate column...")
            conn.execute(text("ALTER TABLE posting ADD COLUMN mandate VARCHAR"))
            conn.commit()
            print("Added mandate column")
        except Exception as e:
            print(f"Error adding mandate (might exist): {e}")
            conn.rollback()
        
if __name__ == "__main__":
    migrate()
