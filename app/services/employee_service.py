from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:

    @staticmethod
    def create_employee(db: Session, employee: EmployeeCreate):

        existing_employee = (
            db.query(Employee)
            .filter(Employee.email == employee.email)
            .first()
        )

        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee email already exists"
            )

        db_employee = Employee(
            name=employee.name,
            email=employee.email,
            phone=employee.phone,
            department=employee.department,
            designation=employee.designation,
            is_active=True
        )

        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        return db_employee

    @staticmethod
    def get_all_employees(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        skip = (page - 1) * limit

        employees = (
            db.query(Employee)
            .filter(Employee.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return employees

    @staticmethod
    def get_employee(
        db: Session,
        employee_id: int
    ):

        employee = (
            db.query(Employee)
            .filter(
                Employee.id == employee_id,
                Employee.is_active == True
            )
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return employee

    @staticmethod
    def update_employee(
        db: Session,
        employee_id: int,
        employee: EmployeeUpdate
    ):

        db_employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        email_exists = (
            db.query(Employee)
            .filter(
                Employee.email == employee.email,
                Employee.id != employee_id
            )
            .first()
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        db_employee.name = employee.name
        db_employee.email = employee.email
        db_employee.phone = employee.phone
        db_employee.department = employee.department
        db_employee.designation = employee.designation
        db_employee.is_active = employee.is_active

        db.commit()
        db.refresh(db_employee)

        return db_employee

    @staticmethod
    def delete_employee(
        db: Session,
        employee_id: int
    ):

        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        employee.is_active = False

        db.commit()

        return {
            "message": "Employee deleted successfully"
        }