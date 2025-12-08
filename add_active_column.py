from sqlalchemy import create_engine, text
from app.infrastructure.database import DATABASE_URL

def add_column():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE staff ADD COLUMN active BOOLEAN DEFAULT TRUE"))
            conn.commit()
            print("Successfully added 'active' column to 'staff' table.")
        except Exception as e:
            print(f"Error adding column: {e}")

if __name__ == "__main__":
    add_column()
