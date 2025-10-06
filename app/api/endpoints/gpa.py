from fastapi import APIRouter

from app.db.repository.gpa import GPARepository

router = APIRouter(
    prefix="/gpa",
    tags=["GPA"],
)


@router.get("")
async def get_gpa():
    result = await GPARepository.get_all()
    return result
