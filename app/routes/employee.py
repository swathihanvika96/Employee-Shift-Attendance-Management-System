from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services.employee_service import EmployeeService
from app.utils.dependencies import (
    admin_required,
    employee_required
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "",
    response_model=EmployeeResponse
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return EmployeeService.create_employee(
        db,
        employee
    )


@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def get_all_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(employee_required)
):
    return EmployeeService.get_all_employees(
        db,
        page,
        limit
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(employee_required)
):
    return EmployeeService.get_employee(
        db,
        employee_id
    )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return EmployeeService.update_employee(
        db,
        employee_id,
        employee
    )


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return EmployeeService.delete_employee(
        db,
        employee_id
    )