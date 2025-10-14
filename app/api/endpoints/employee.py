from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.db.repository.employee import EmployeeRepository

router = APIRouter(prefix="/employees", tags=["Сотрудники"])


@router.get("")
async def get_employees(
    page: int = 1,
    limit: int = 10,
    current_user=Depends(PermissionChecker(["get_employee", "all"])),
):

    employees = await EmployeeRepository.get_all(
        page,
        limit,
    )
    return employees


@router.get("/{employee_id}")
async def get_employee(
    employee_id: str,
    current_user=Depends(PermissionChecker(["get_employee_id", "all"])),
):

    employee = await EmployeeRepository.find_by_variable(employee_id_number=employee_id)
    return employee


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    current_user=Depends(PermissionChecker(["delete_employee", "all"])),
):
    employee = await EmployeeRepository.delete_employee(employee_id)
    return employee
