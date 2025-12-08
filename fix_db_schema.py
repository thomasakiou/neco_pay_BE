from app.infrastructure.database import engine
from app.infrastructure.models import Base, PostingModel, PaymentModel
from sqlalchemy import text

def reset_schema():
    print("Dropping tables...")
    with engine.connect() as conn:
        # Use CASCADE to handle potential foreign keys (though none explicitly defined)
        conn.execute(text("DROP TABLE IF EXISTS posting CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS payment_db CASCADE"))
        conn.commit()
    
    print("Recreating tables...")
    # This will create all tables defined in Base, counting on checkfirst=True (default) to skip existing ones
    Base.metadata.create_all(bind=engine)
    print("Schema reset successfully.")

if __name__ == "__main__":
    reset_schema()
