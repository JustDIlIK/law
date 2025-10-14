from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from app.api.schemas.student_contact import (
    StudentContactSchema,
    StudentContactSchemaPatch,
)
from app.db.repository.student_contact import StudentContactRepository

router = APIRouter(prefix="/contacts", tags=["Студенты"])


@router.get("/{student_id_number}")
async def get_contact(student_id_number: str):
    contact = await StudentContactRepository.find_all_by_variable(
        student_id_number=student_id_number,
    )

    if not contact:
        return []

    return contact


@router.post("/add")
async def add_contact(data: StudentContactSchema):

    result = await StudentContactRepository.add_record(**data.model_dump())

    return result


@router.patch("/change/{student_id_number}")
async def change_contact(student_id_number: str, data: StudentContactSchemaPatch):

    old = await StudentContactRepository.find_by_variable(
        student_id_number=student_id_number,
    )

    result = await StudentContactRepository.update_data(old.id, **data.model_dump())

    return result
