from datetime import date
from datetime import time

from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    employee_id: int
    shift_id: int
    date: date
    check_in: time
    check_out: time
    attendance_status: str


class AttendanceUpdate(BaseModel):
    shift_id: int
    date: date
    check_in: time
    check_out: time
    attendance_status: str


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    shift_id: int
    date: date
    check_in: time
    check_out: time
    attendance_status: str

    class Config:
        from_attributes = True