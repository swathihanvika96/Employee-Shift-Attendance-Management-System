from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time

from sqlalchemy.orm import relationship

from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    shift_id = Column(
        Integer,
        ForeignKey("shifts.id"),
        nullable=False
    )

    date = Column(Date, nullable=False)

    check_in = Column(Time, nullable=False)

    check_out = Column(Time, nullable=False)

    attendance_status = Column(String(30), nullable=False)

    employee = relationship(
        "Employee",
        back_populates="attendances"
    )

    shift = relationship(
        "Shift",
        back_populates="attendances"
    )