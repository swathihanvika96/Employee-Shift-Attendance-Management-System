from fastapi import FastAPI

from app.database import Base, engine

# Import Models
from app.models.user import User
from app.models.employee import Employee
from app.models.shift import Shift
from app.models.attendance import Attendance

# Import Routes
from app.routes.auth import router as auth_router
from app.routes.employee import router as employee_router
from app.routes.shift import router as shift_router
from app.routes.attendance import router as attendance_router
from app.routes.report import router as report_router

# Import Middleware
from app.middleware.logging import LoggingMiddleware

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI(
    title="Employee Shift & Attendance Management System",
    description="FastAPI Backend Assignment",
    version="1.0.0"
)


# Root Endpoint
@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Employee Shift & Attendance Management System",
        "status": "Running"
    }

# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "OK"
    }

# Include Routers
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(shift_router)
app.include_router(attendance_router)
app.include_router(report_router)