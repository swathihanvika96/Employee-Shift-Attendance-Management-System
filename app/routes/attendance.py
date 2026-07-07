from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)

from app.services.attendance_service import AttendanceService

from app.models.user import User

from app.utils.dependencies import (
    admin_required,
    employee_required,
    get_current_user
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post(
    "",
    response_model=AttendanceResponse
)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return AttendanceService.create_attendance(
        db,
        attendance
    )


@router.get(
    "",
    response_model=list[AttendanceResponse]
)
def get_all_attendance(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return AttendanceService.get_all_attendance(
        db,
        page,
        limit
    )


@router.get(
    "/{employee_id}",
    response_model=list[AttendanceResponse]
)
def get_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Admin can view any employee's attendance.
    Employee can view only their own attendance.
    """

    if (
        current_user.role == "Employee"
        and current_user.employee_id != employee_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own attendance."
        )

    return AttendanceService.get_employee_attendance(
        db,
        employee_id
    )


@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    return AttendanceService.update_attendance(
        db,
        attendance_id,
        attendance
    )