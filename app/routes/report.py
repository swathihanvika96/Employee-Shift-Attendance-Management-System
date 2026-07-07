from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.database import get_db
from app.services.report_service import ReportService
from app.utils.dependencies import admin_required

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/monthly")
def monthly_report(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    return ReportService.monthly_report(
        db=db,
        month=month,
        year=year,
        page=page,
        limit=limit
    )


@router.get("/filter")
def filter_report(
    employee_id: int | None = None,
    department: str | None = None,
    attendance_date: date | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    return ReportService.filter_report(
        db=db,
        employee_id=employee_id,
        department=department,
        attendance_date=attendance_date,
        page=page,
        limit=limit
    )