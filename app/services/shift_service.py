from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftUpdate


class ShiftService:

    @staticmethod
    def create_shift(db: Session, shift: ShiftCreate):

        if shift.end_time <= shift.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be greater than start time."
            )

        existing_shift = (
            db.query(Shift)
            .filter(Shift.shift_name == shift.shift_name)
            .first()
        )

        if existing_shift:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shift already exists."
            )

        db_shift = Shift(
            shift_name=shift.shift_name,
            start_time=shift.start_time,
            end_time=shift.end_time,
            shift_type=shift.shift_type
        )

        db.add(db_shift)
        db.commit()
        db.refresh(db_shift)

        return db_shift

    @staticmethod
    def get_all_shifts(db: Session):

        return db.query(Shift).all()

    @staticmethod
    def update_shift(
        db: Session,
        shift_id: int,
        shift: ShiftUpdate
    ):

        db_shift = (
            db.query(Shift)
            .filter(Shift.id == shift_id)
            .first()
        )

        if not db_shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shift not found."
            )

        if shift.end_time <= shift.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be greater than start time."
            )

        db_shift.shift_name = shift.shift_name
        db_shift.start_time = shift.start_time
        db_shift.end_time = shift.end_time
        db_shift.shift_type = shift.shift_type

        db.commit()
        db.refresh(db_shift)

        return db_shift