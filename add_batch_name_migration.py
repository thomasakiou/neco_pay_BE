"""Add batch_name column to posting table"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.database import SessionLocal
from sqlalchemy import text

def migrate():
    db = SessionLocal()
    try:
        db.execute(text("ALTER TABLE posting ADD COLUMN IF NOT EXISTS batch_name VARCHAR"))
        db.execute(text("CREATE INDEX IF NOT EXISTS ix_posting_batch_name ON posting (batch_name)"))
        db.commit()
        print("Migration complete: batch_name column added to posting table.")
    except Exception as e:
        db.rollback()
        print(f"Migration failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
