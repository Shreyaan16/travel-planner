from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Travel Option schemas
class TravelOptionBase(BaseModel):
    title: str
    type: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price_per_seat: Decimal
    available_seats: int

class TravelOptionCreate(TravelOptionBase):
    pass

class TravelOption(TravelOptionBase):
    option_id: int

    class Config:
        from_attributes = True

# Booking schemas
class BookingBase(BaseModel):
    option_id: int
    num_seats: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    booking_id: int
    user_id: int
    total_price: Decimal
    booking_date: datetime
    status: str
    travel_option: TravelOption

    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    booking_id: int
    num_seats: int
    total_price: Decimal
    booking_date: datetime
    status: str
    travel_option: TravelOption

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Search/Filter schemas
class TravelSearchFilter(BaseModel):
    type: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
