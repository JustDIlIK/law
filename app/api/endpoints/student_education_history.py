from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.student_education_history import (
    StudentEducationHistorySchema,
    StudentEducationHistoryPatch,
)
from app.db.repository.student_education_history import (
    StudentEducationHistoryRepository,
)

router = APIRouter(prefix="/education-history", tags=["Студенты"])


@router.get("/{student_id_number}")
async def get_education_history(
    student_id_number: str,
    current_user=Depends(PermissionChecker(["get_student_education", "all"])),
):
    history = await StudentEducationHistoryRepository.find_all_by_variable(
        student_id_number=student_id_number,
    )

    if not history:
        return []

    result = []

    for res in history["data"]:
        result.append(
            {
                "student_id_number": res.student_id_number,
                "order": res.order,
                "title": {
                    "ru": res.title_ru,
                    "en": res.title_en,
                    "uz": res.title_uz,
                    "uz_l": res.title_uz_l,
                },
                "started_year": res.started_year,
                "ended_year": res.ended_year,
                "id": res.id,
            }
        )
    return result


@router.post("/add")
async def add_history(
    data: StudentEducationHistorySchema,
    current_user=Depends(PermissionChecker(["add_student_education", "all"])),
):

    res = data.model_dump()

    title = res.pop("title")
    res["title_en"] = title["en"]
    res["title_ru"] = title["ru"]
    res["title_uz"] = title["uz"]
    res["title_uz_l"] = title["uz_l"]

    result = await StudentEducationHistoryRepository.add_record(**res)

    return result


@router.delete("/{id}")
async def add_history(
    id: int,
    current_user=Depends(PermissionChecker(["delete_student_education", "all"])),
):

    result = await StudentEducationHistoryRepository.remove_by_id(
        record_id=id,
    )

    return result


@router.patch("/change/{id}")
async def change_history(
    id: int,
    data: StudentEducationHistoryPatch,
    current_user=Depends(PermissionChecker(["patch_student_education", "all"])),
):
    res = data.model_dump()

    title = res.pop("title", None)
    if title:
        res["title_en"] = title.get("en")
        res["title_ru"] = title.get("ru")
        res["title_uz"] = title.get("uz")
        res["title_uz_l"] = title.get("uz_l")

    result = await StudentEducationHistoryRepository.update_data(id, **res)

    return result
