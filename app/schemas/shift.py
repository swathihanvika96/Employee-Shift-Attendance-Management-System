from datetime import time

from pydantic import BaseModel


class ShiftCreate(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
    shift_type: str


class ShiftUpdate(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
    shift_type: str


class ShiftResponse(BaseModel):
    id: int
    shift_name: str
    start_time: time
    end_time: time
    shift_type: str

    class Config:
        from_attributes = True