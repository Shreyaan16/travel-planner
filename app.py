from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import models
import schemas
import crud
import auth
from database import engine, SessionLocal
from sample_data import create_sample_data
from typing import List, Optional
import os

app = FastAPI(title="Travel Booking API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Create tables in database
models.Base.metadata.create_all(bind=engine)

# Create sample data on startup
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        create_sample_data(db)
    finally:
        db.close()

@app.get("/")
def read_root():
    return FileResponse('frontend/index.html')

@app.get("/api")
def api_root():
    return {"message": "Travel Booking API - Ready to serve!", "version": "1.0.0"}

# Authentication endpoints
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    # Check if username already exists
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User management endpoints
@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.put("/users/me", response_model=schemas.User)
def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    updated_user = crud.update_user(db, current_user.user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Travel options endpoints
@app.get("/travel-options", response_model=List[schemas.TravelOption])
def get_travel_options(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    source: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(auth.get_db)
):
    from decimal import Decimal
    if any([type, source, destination, date, min_price, max_price]):
        # Convert float to Decimal for database queries
        min_price_decimal = Decimal(str(min_price)) if min_price is not None else None
        max_price_decimal = Decimal(str(max_price)) if max_price is not None else None
        
        # Use search function if any filters are provided
        return crud.search_travel_options(
            db=db,
            type=type,
            source=source,
            destination=destination,
            date=date,
            min_price=min_price_decimal,
            max_price=max_price_decimal,
            skip=skip,
            limit=limit
        )
    else:
        # Return all travel options
        return crud.get_travel_options(db=db, skip=skip, limit=limit)

@app.get("/travel-options/{option_id}", response_model=schemas.TravelOption)
def get_travel_option(option_id: int, db: Session = Depends(auth.get_db)):
    db_option = crud.get_travel_option(db, option_id=option_id)
    if db_option is None:
        raise HTTPException(status_code=404, detail="Travel option not found")
    return db_option

@app.post("/travel-options", response_model=schemas.TravelOption)
def create_travel_option(
    travel_option: schemas.TravelOptionCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # This endpoint could be restricted to admin users in a real application
    return crud.create_travel_option(db=db, travel_option=travel_option)

# Booking endpoints
@app.post("/bookings", response_model=schemas.Booking)
def create_booking(
    booking: schemas.BookingCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    # Validate that the travel option exists and has enough seats
    travel_option = crud.get_travel_option(db, booking.option_id)
    if not travel_option:
        raise HTTPException(status_code=404, detail="Travel option not found")
    
    if travel_option.available_seats < booking.num_seats:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough seats available. Only {travel_option.available_seats} seats left."
        )
    
    if booking.num_seats <= 0:
        raise HTTPException(status_code=400, detail="Number of seats must be greater than 0")
    
    db_booking = crud.create_booking(db=db, booking=booking, user_id=current_user.user_id)
    if db_booking is None:
        raise HTTPException(status_code=400, detail="Failed to create booking")
    
    return db_booking

@app.get("/bookings", response_model=List[schemas.Booking])
def get_user_bookings(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    return crud.get_user_bookings(db=db, user_id=current_user.user_id)

@app.get("/bookings/{booking_id}", response_model=schemas.Booking)
def get_booking(
    booking_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    booking = crud.get_booking(db=db, booking_id=booking_id, user_id=current_user.user_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.put("/bookings/{booking_id}/cancel", response_model=schemas.Booking)
def cancel_booking(
    booking_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    booking = crud.cancel_booking(db=db, booking_id=booking_id, user_id=current_user.user_id)
    if booking is None:
        raise HTTPException(
            status_code=400,
            detail="Booking not found or cannot be cancelled"
        )
    return booking

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Travel Booking API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)