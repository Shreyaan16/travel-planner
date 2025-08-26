"""
Travel Booking Application - Startup Script

This script starts the FastAPI server with the frontend integrated.
Make sure you have activated your fastapi_env before running this.

To run:
1. Open terminal in the project directory
2. Activate fastapi environment: conda activate fastapi_env
3. Run: python run_server.py
"""

import uvicorn
import os

if __name__ == "__main__":
    print("🚀 Starting Travel Booking Application...")
    print("📍 Frontend will be available at: http://localhost:8000")
    print("📡 API documentation at: http://localhost:8000/docs")
    print("⚡ Auto-reload enabled for development")
    print("\n" + "="*50)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[".", "frontend"]
    )
