from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )

    department = Column(
        String(100),
        nullable=False
    )

    designation = Column(
        String(100),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    attendances = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    user = relationship(
        "User",
        back_populates="employee",
        uselist=False
    )