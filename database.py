from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_DSN", "sqlite:///./travel_booking.db")

print(f"Attempting to connect to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    # Test connection
    with engine.connect() as conn:
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("Switching to SQLite for development...")
    DATABASE_URL = "sqlite:///./travel_booking.db"
    engine = create_engine(DATABASE_URL)
    print("✅ Using SQLite database instead")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
