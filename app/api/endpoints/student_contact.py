from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.student_contact import (
    StudentContactSchema,
    StudentContactSchemaPatch,
)
from app.db.repository.student_contact import StudentContactRepository

router = APIRouter(prefix="/contacts", tags=["Студенты"])


@router.get("/{student_id_number}")
async def get_contact(
    student_id_number: str,
    current_user=Depends(PermissionChecker(["get_student_contact", "all"])),
):
    contact = await StudentContactRepository.find_all_by_variable(
        student_id_number=student_id_number,
    )

    if not contact:
        return []

    return contact["data"]


@router.post("/add")
async def add_contact(
    data: StudentContactSchema,
    current_user=Depends(PermissionChecker(["add_student_contact", "all"])),
):

    result = await StudentContactRepository.add_record(**data.model_dump())

    return result


@router.delete("/{id}")
async def delete_contact(
    id: int,
    current_user=Depends(PermissionChecker(["delete_student_contact", "all"])),
):

    result = await StudentContactRepository.remove_by_id(
        id,
    )

    return result


@router.patch("/change/{student_id_number}")
async def change_contact(
    student_id_number: str,
    data: StudentContactSchemaPatch,
    current_user=Depends(PermissionChecker(["patch_student_contact", "all"])),
):

    old = await StudentContactRepository.find_by_variable(
        student_id_number=student_id_number,
    )

    result = await StudentContactRepository.update_data(old.id, **data.model_dump())

    return result
