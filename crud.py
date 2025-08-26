from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, cast, Date
from datetime import datetime, date
import models
import schemas
from auth import get_password_hash
from typing import Optional, List
from decimal import Decimal

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Travel Option CRUD operations
def get_travel_options(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TravelOption).offset(skip).limit(limit).all()

def get_travel_option(db: Session, option_id: int):
    return db.query(models.TravelOption).filter(models.TravelOption.option_id == option_id).first()

def create_travel_option(db: Session, travel_option: schemas.TravelOptionCreate):
    db_option = models.TravelOption(**travel_option.dict())
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

def search_travel_options(
    db: Session, 
    type: Optional[str] = None,
    source: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.TravelOption)
    
    if type:
        query = query.filter(models.TravelOption.type.ilike(f"%{type}%"))
    
    if source:
        query = query.filter(models.TravelOption.source.ilike(f"%{source}%"))
    
    if destination:
        query = query.filter(models.TravelOption.destination.ilike(f"%{destination}%"))
    
    if date:
        try:
            search_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(cast(models.TravelOption.departure_time, Date) == search_date)
        except ValueError:
            pass  # Invalid date format, ignore filter
    
    if min_price is not None:
        query = query.filter(models.TravelOption.price_per_seat >= min_price)
    
    if max_price is not None:
        query = query.filter(models.TravelOption.price_per_seat <= max_price)
    
    # Only show options with available seats
    query = query.filter(models.TravelOption.available_seats > 0)
    
    return query.offset(skip).limit(limit).all()

# Booking CRUD operations
def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    # Get travel option to calculate total price
    travel_option = get_travel_option(db, booking.option_id)
    if not travel_option:
        return None
    
    if travel_option.available_seats < booking.num_seats:
        return None  # Not enough seats available
    
    total_price = travel_option.price_per_seat * booking.num_seats
    
    db_booking = models.Booking(
        user_id=user_id,
        option_id=booking.option_id,
        num_seats=booking.num_seats,
        total_price=total_price,
        status="Confirmed"
    )
    
    # Update available seats
    travel_option.available_seats = travel_option.available_seats - booking.num_seats
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_user_bookings(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

def get_booking(db: Session, booking_id: int, user_id: int):
    return db.query(models.Booking).filter(
        and_(models.Booking.booking_id == booking_id, models.Booking.user_id == user_id)
    ).first()

def cancel_booking(db: Session, booking_id: int, user_id: int):
    booking = get_booking(db, booking_id, user_id)
    if booking and booking.status == "Confirmed":
        # Update booking status
        booking.status = "Cancelled"
        
        # Return seats to travel option
        travel_option = get_travel_option(db, booking.option_id)
        if travel_option:
            travel_option.available_seats = travel_option.available_seats + booking.num_seats
        
        db.commit()
        db.refresh(booking)
        return booking
    return None

def get_all_bookings(db: Session, skip: int = 0, limit: int = 100):
    """Admin function to get all bookings"""
    return db.query(models.Booking).offset(skip).limit(limit).all()
