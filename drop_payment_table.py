
from app.infrastructure.database import engine
from app.infrastructure.models import Base
from sqlalchemy import text

def drop_payment_table():
    print("Dropping payment table...")
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS payment CASCADE"))
        connection.commit()
    print("Payment table dropped.")

if __name__ == "__main__":
    drop_payment_table()
