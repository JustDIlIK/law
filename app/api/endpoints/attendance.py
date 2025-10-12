from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.db.repository.attendance import AttendanceRepository

router = APIRouter(
    prefix="/attendances",
    tags=["Посещение"],
)


@router.get("/education_year")
async def get_attendance(education_year: str, semester: str, group_id: int):

    attendance = await AttendanceRepository.find_all_by_variable(
        education_year_code=education_year,
        semester_code=semester,
        group_id=group_id,
    )

    return attendance


@router.post("/education_year")
async def get_attendance(
    education_year: str,
    student_id_number: str,
    semester: str,
    count: int,
):

    check_attendance = await AttendanceRepository.find_by_variable(
        education_year_code=education_year,
        semester_code=semester,
        student_id_number=student_id_number,
    )

    if check_attendance:
        return JSONResponse(content="Уже нельзя загрузить за этот период")

    attendance = await AttendanceRepository.add_record(
        education_year_code=education_year,
        semester_code=semester,
        student_id_number=student_id_number,
        total_absences=count,
    )

    return attendance
