from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from app.api.schemas.student_education_history import (
    StudentEducationHistorySchema,
    StudentEducationHistoryPatch,
)
from app.db.repository.student_education_history import (
    StudentEducationHistoryRepository,
)

router = APIRouter(prefix="/education-history", tags=["Студенты"])


@router.get("/{student_id_number}")
async def get_education_history(student_id_number: str):
    history = await StudentEducationHistoryRepository.find_all_by_variable(
        student_id_number=student_id_number,
    )

    if not history:
        return []

    return history["data"]


@router.post("/add")
async def add_history(data: StudentEducationHistorySchema):

    result = await StudentEducationHistoryRepository.add_record(**data.model_dump())

    return result


@router.patch("/change/{id}")
async def change_history(id: int, data: StudentEducationHistoryPatch):

    result = await StudentEducationHistoryRepository.update_data(
        id, **data.model_dump()
    )

    return result
