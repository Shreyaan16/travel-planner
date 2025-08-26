from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Users Table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone_number = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())

    bookings = relationship("Booking", back_populates="user")


# Travel Options Table
class TravelOption(Base):
    __tablename__ = "travel_options"

    option_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)       # e.g., Flight / Train / Bus
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price_per_seat = Column(DECIMAL(10, 2), nullable=False)
    available_seats = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="travel_option")


# Bookings Table
class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    option_id = Column(Integer, ForeignKey("travel_options.option_id", ondelete="CASCADE"))
    num_seats = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    booking_date = Column(DateTime, server_default=func.now())
    status = Column(String(20), default="Confirmed")

    user = relationship("User", back_populates="bookings")
    travel_option = relationship("TravelOption", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)


# Payments Table (Optional)
class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50))
    payment_date = Column(DateTime, server_default=func.now())
    status = Column(String(20), default="Success")

    booking = relationship("Booking", back_populates="payment")
