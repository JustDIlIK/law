from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import check_permission
from app.db.repository.semester import SemesterRepository

router = APIRouter(
    prefix="/semesters",
    tags=["Семестры"],
)


@router.get("")
async def get_semesters():
    semesters = await SemesterRepository.get_all()

    return semesters
