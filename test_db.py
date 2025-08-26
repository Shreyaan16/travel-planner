import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
import models
from sample_data import create_sample_data

def test_database():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Test database connection
    db = SessionLocal()
    try:
        # Create sample data
        create_sample_data(db)
        
        # Test queries
        users = db.query(models.User).all()
        travel_options = db.query(models.TravelOption).all()
        
        print(f"✅ Database test passed!")
        print(f"Users in database: {len(users)}")
        print(f"Travel options in database: {len(travel_options)}")
        
        # Show some travel options
        for option in travel_options[:3]:
            print(f"- {option.title}: {option.source} → {option.destination} (₹{option.price_per_seat})")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
