import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.models import PostingModel
from app.domain.posting import Posting

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def debug_insert():
    db = SessionLocal()
    try:
        print("Creating Posting domain object...")
        posting = Posting(
            id=None,
            # state=None, # Should be gone
            file_no="DB_TEST",
            name="TEST INSERT",
            conraiss="15",
            station="DEBUG STATION",
            posting="DEBUG POSTING",
            # category=None,
            # rank=None,
            # mandate=None,
            active=True
        )
        
        print(f"Domain Object: {posting}")
        
        print("Converting to Model...")
        db_posting = PostingModel.from_entity(posting)
        print(f"Model Object: {db_posting.__dict__}")
        
        print("Adding to session...")
        db.add(db_posting)
        
        print("Committing...")
        db.commit()
        print("Success!")
        
    except Exception as e:
        print(f"Error during insert: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    debug_insert()
