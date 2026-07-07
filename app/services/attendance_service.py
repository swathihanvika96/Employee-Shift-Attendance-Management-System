from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.shift import Shift

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate
)


class AttendanceService:

    @staticmethod
    def create_attendance(
        db: Session,
        attendance: AttendanceCreate
    ):

        employee = (
            db.query(Employee)
            .filter(
                Employee.id == attendance.employee_id,
                Employee.is_active == True
            )
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found."
            )

        shift = (
            db.query(Shift)
            .filter(Shift.id == attendance.shift_id)
            .first()
        )

        if not shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shift not found."
            )

        existing = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id == attendance.employee_id,
                Attendance.date == attendance.date
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance already marked for this date."
            )

        if attendance.check_out <= attendance.check_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check-out time must be greater than check-in time."
            )

        db_attendance = Attendance(
            employee_id=attendance.employee_id,
            shift_id=attendance.shift_id,
            date=attendance.date,
            check_in=attendance.check_in,
            check_out=attendance.check_out,
            attendance_status=attendance.attendance_status
        )

        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)

        return db_attendance

    @staticmethod
    def get_all_attendance(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        skip = (page - 1) * limit

        return (
            db.query(Attendance)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_employee_attendance(
        db: Session,
        employee_id: int
    ):

        attendance = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id == employee_id
            )
            .all()
        )

        return attendance

    @staticmethod
    def update_attendance(
        db: Session,
        attendance_id: int,
        attendance: AttendanceUpdate
    ):

        db_attendance = (
            db.query(Attendance)
            .filter(
                Attendance.id == attendance_id
            )
            .first()
        )

        if not db_attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance not found."
            )

        if attendance.check_out <= attendance.check_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check-out time must be greater than check-in time."
            )

        db_attendance.shift_id = attendance.shift_id
        db_attendance.date = attendance.date
        db_attendance.check_in = attendance.check_in
        db_attendance.check_out = attendance.check_out
        db_attendance.attendance_status = attendance.attendance_status

        db.commit()
        db.refresh(db_attendance)

        return db_attendance