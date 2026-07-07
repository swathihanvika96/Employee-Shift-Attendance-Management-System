from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)

    shift_name = Column(String(100), nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    shift_type = Column(String(50), nullable=False)

    attendances = relationship(
        "Attendance",
        back_populates="shift"
    )