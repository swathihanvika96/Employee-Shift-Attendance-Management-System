from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(
        ...,
        pattern=r"^[6-9]\d{9}$"
    )
    department: str
    designation: str


class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(
        ...,
        pattern=r"^[6-9]\d{9}$"
    )
    department: str
    designation: str
    is_active: bool


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    department: str
    designation: str
    is_active: bool

    class Config:
        from_attributes = True