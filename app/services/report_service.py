from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.employee import Employee


class ReportService:

    @staticmethod
    def monthly_report(
        db: Session,
        month: int,
        year: int,
        page: int = 1,
        limit: int = 10
    ):

        skip = (page - 1) * limit

        reports = (
            db.query(Attendance)
            .filter(
                Attendance.date.month == month,
                Attendance.date.year == year
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        return reports

    @staticmethod
    def filter_report(
        db: Session,
        employee_id: int = None,
        department: str = None,
        attendance_date: date = None,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Attendance)
            .join(Employee)
        )

        if employee_id:
            query = query.filter(
                Attendance.employee_id == employee_id
            )

        if department:
            query = query.filter(
                Employee.department == department
            )

        if attendance_date:
            query = query.filter(
                Attendance.date == attendance_date
            )

        skip = (page - 1) * limit

        return (
            query.offset(skip)
            .limit(limit)
            .all()
        )