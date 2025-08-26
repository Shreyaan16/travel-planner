from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
from decimal import Decimal

def create_sample_data(db: Session):
    """Create sample travel options for testing"""
    
    # Check if data already exists
    existing_options = db.query(models.TravelOption).first()
    if existing_options:
        return  # Data already exists
    
    sample_options = [
        # Flights
        models.TravelOption(
            title="SpiceJet Flight SG-123",
            type="Flight",
            source="Mumbai",
            destination="Delhi",
            departure_time=datetime.now() + timedelta(days=1, hours=8),
            arrival_time=datetime.now() + timedelta(days=1, hours=10),
            price_per_seat=Decimal("5500.00"),
            available_seats=120
        ),
        models.TravelOption(
            title="IndiGo Flight 6E-456",
            type="Flight",
            source="Delhi",
            destination="Bangalore",
            departure_time=datetime.now() + timedelta(days=2, hours=14),
            arrival_time=datetime.now() + timedelta(days=2, hours=17),
            price_per_seat=Decimal("6200.00"),
            available_seats=150
        ),
        models.TravelOption(
            title="Air India Flight AI-789",
            type="Flight",
            source="Mumbai",
            destination="Chennai",
            departure_time=datetime.now() + timedelta(days=3, hours=11),
            arrival_time=datetime.now() + timedelta(days=3, hours=13, minutes=30),
            price_per_seat=Decimal("5800.00"),
            available_seats=100
        ),
        
        # Trains
        models.TravelOption(
            title="Rajdhani Express",
            type="Train",
            source="Delhi",
            destination="Mumbai",
            departure_time=datetime.now() + timedelta(days=1, hours=16),
            arrival_time=datetime.now() + timedelta(days=2, hours=8),
            price_per_seat=Decimal("2500.00"),
            available_seats=200
        ),
        models.TravelOption(
            title="Shatabdi Express",
            type="Train",
            source="Delhi",
            destination="Chandigarh",
            departure_time=datetime.now() + timedelta(days=2, hours=7),
            arrival_time=datetime.now() + timedelta(days=2, hours=10, minutes=30),
            price_per_seat=Decimal("800.00"),
            available_seats=300
        ),
        models.TravelOption(
            title="Gatimaan Express",
            type="Train",
            source="Delhi",
            destination="Agra",
            departure_time=datetime.now() + timedelta(days=4, hours=8),
            arrival_time=datetime.now() + timedelta(days=4, hours=10),
            price_per_seat=Decimal("750.00"),
            available_seats=180
        ),
        
        # Buses
        models.TravelOption(
            title="Volvo AC Bus",
            type="Bus",
            source="Delhi",
            destination="Manali",
            departure_time=datetime.now() + timedelta(days=5, hours=22),
            arrival_time=datetime.now() + timedelta(days=6, hours=12),
            price_per_seat=Decimal("1200.00"),
            available_seats=45
        ),
        models.TravelOption(
            title="RedBus Sleeper",
            type="Bus",
            source="Mumbai",
            destination="Pune",
            departure_time=datetime.now() + timedelta(days=1, hours=23),
            arrival_time=datetime.now() + timedelta(days=2, hours=3),
            price_per_seat=Decimal("400.00"),
            available_seats=32
        ),
        models.TravelOption(
            title="Luxury Coach",
            type="Bus",
            source="Bangalore",
            destination="Mysore",
            departure_time=datetime.now() + timedelta(days=3, hours=9),
            arrival_time=datetime.now() + timedelta(days=3, hours=12),
            price_per_seat=Decimal("350.00"),
            available_seats=40
        ),
    ]
    
    for option in sample_options:
        db.add(option)
    
    db.commit()
    print("Sample travel options created successfully!")
