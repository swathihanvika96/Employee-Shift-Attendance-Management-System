from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.shift import (
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse
)
from app.services.shift_service import ShiftService
from app.utils.dependencies import (
    admin_required,
    employee_required
)

router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"]
)


@router.post(
    "",
    response_model=ShiftResponse
)
def create_shift(
    shift: ShiftCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return ShiftService.create_shift(db, shift)


@router.get(
    "",
    response_model=list[ShiftResponse]
)
def get_all_shifts(
    db: Session = Depends(get_db),
    current_user=Depends(employee_required)
):
    return ShiftService.get_all_shifts(db)


@router.put(
    "/{shift_id}",
    response_model=ShiftResponse
)
def update_shift(
    shift_id: int,
    shift: ShiftUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return ShiftService.update_shift(
        db,
        shift_id,
        shift
    )