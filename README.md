# TravelLykke - Travel Booking Application

A comprehensive travel booking web application built with FastAPI backend and vanilla JavaScript frontend.

## Features

### Backend (FastAPI)
- ✅ User authentication (register, login, logout)
- ✅ JWT token-based security
- ✅ User profile management
- ✅ Travel options management (flights, trains, buses)
- ✅ Booking system with seat management
- ✅ Search and filtering capabilities
- ✅ Booking cancellation
- ✅ Database integration (PostgreSQL/SQLite)
- ✅ API documentation with Swagger UI

### Frontend (HTML/CSS/JavaScript)
- ✅ Responsive design for desktop and mobile
- ✅ User authentication interface
- ✅ Travel search with filters
- ✅ Real-time booking system
- ✅ User dashboard for managing bookings
- ✅ Profile management
- ✅ Modern UI with gradient design

## Project Structure

```
root/
├── app.py                 # Main FastAPI application
├── models.py             # Database models
├── schemas.py            # Pydantic schemas
├── database.py           # Database configuration
├── auth.py               # Authentication utilities
├── crud.py               # Database operations
├── sample_data.py        # Sample data for testing
├── run_server.py         # Server startup script
├── test_db.py           # Database testing script
└── frontend/
    ├── index.html        # Main frontend page
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── app.js        # Frontend JavaScript
```

## Setup Instructions

### 1. Environment Setup
```bash
# Activate your fastapi environment
conda activate fastapi_env

# Install required packages (if not already installed)
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 2. Database Configuration
The application uses SQLite by default for development. For PostgreSQL:
1. Create a `.env` file in the project root
2. Add your PostgreSQL connection string:
```
POSTGRES_DSN=postgresql://username:password@localhost/database_name
```

### 3. Running the Application

#### Option 1: Using the startup script
```bash
python run_server.py
```

#### Option 2: Using uvicorn directly
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Base**: http://localhost:8000/api

## Usage Guide

### 1. First Time Setup
1. Start the server using one of the methods above
2. Open http://localhost:8000 in your browser
3. Click "Register" to create a new account
4. Fill in your details and register

### 2. Using the Application

#### Registration
- Click "Register" in the top navigation
- Fill in required fields (username, email, password)
- Optional: Add full name and phone number
- Click "Register" button

#### Login
- Click "Login" in the top navigation
- Enter your username and password
- Click "Login" button

#### Searching for Travel Options
- After login, you'll see the search form
- Use filters to narrow down options:
  - Travel Type (Flight, Train, Bus)
  - Source and Destination cities
  - Travel Date
  - Price range
- Click "Search" or leave filters empty to see all options

#### Booking a Trip
1. Find a travel option you like
2. Click "Book Now" button
3. Select number of seats
4. Review total price
5. Click "Confirm Booking"

#### Managing Bookings
- Click "My Bookings" in the navigation
- View all your current and past bookings
- Cancel confirmed bookings if needed

#### Profile Management
- Click "Profile" in the navigation
- Update your personal information
- Click "Update Profile" to save changes

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /token` - User login
- `GET /users/me` - Get current user
- `PUT /users/me` - Update user profile

### Travel Options
- `GET /travel-options` - Get all travel options (with optional filters)
- `GET /travel-options/{id}` - Get specific travel option
- `POST /travel-options` - Create new travel option (admin)

### Bookings
- `POST /bookings` - Create new booking
- `GET /bookings` - Get user's bookings
- `GET /bookings/{id}` - Get specific booking
- `PUT /bookings/{id}/cancel` - Cancel booking

## Sample Data

The application comes with pre-loaded sample data including:
- Various flight options (SpiceJet, IndiGo, Air India)
- Train options (Rajdhani Express, Shatabdi Express, Gatimaan Express)
- Bus options (Volvo AC Bus, RedBus Sleeper, Luxury Coach)

## Technical Features

### Security
- JWT token-based authentication
- Password hashing with bcrypt
- Protected routes requiring authentication
- CORS enabled for frontend integration

### Database
- SQLAlchemy ORM for database operations
- Automatic table creation
- Foreign key relationships
- Data validation

### Frontend
- Responsive design (works on mobile and desktop)
- Real-time form validation
- Local storage for authentication
- Modern CSS with gradients and animations
- Async JavaScript for API communication

## Testing

### Database Test
```bash
python test_db.py
```

### API Testing
Visit http://localhost:8000/docs for interactive API documentation.

## Troubleshooting

### Common Issues

1. **Module not found errors**
   - Make sure fastapi_env is activated
   - Install missing packages with pip

2. **Database connection errors**
   - Check your .env file for PostgreSQL
   - Default SQLite should work without configuration

3. **CORS errors in browser**
   - Make sure the backend is running on port 8000
   - Check browser console for specific errors

4. **Frontend not loading**
   - Ensure you're accessing http://localhost:8000 (not just the HTML file)
   - Check that static files are being served correctly

