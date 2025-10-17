from datetime import datetime

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.attendance import StudentListResponse
from app.api.services.check_data import check_achievements
from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.achievement_type import AchievementTypeRepository
from app.db.repository.attendance import AttendanceRepository
from app.db.repository.group import GroupRepository
from app.db.repository.status import StatusRepository
from app.db.repository.student import StudentRepository
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(
    prefix="/attendances",
    tags=["Посещение"],
)


@router.get("/", response_model=StudentListResponse)
async def get_attendance(
    education_year: str,
    education_type_code: str,
    semester: str,
    group_id: int,
    gender: str = "",
    level: str = "",
    search: str = "",
    current_user=Depends(PermissionChecker(["get_attendance", "all"])),
):

    students = await AttendanceRepository.get_by_group(
        education_year=education_year,
        education_type=education_type_code,
        semester=semester,
        group_id=group_id,
        gender=gender,
        level=level,
        search=search,
    )
    print(f"{students["total"]=}")
    # await check_achievements(
    #     students["data"],
    #     education_year,
    #     semester,
    #     education_type_code,
    # )
    # students = await AttendanceRepository.get_by_group(
    #     education_year=education_year,
    #     education_type=education_type_code,
    #     semester=semester,
    #     group_id=group_id,
    #     gender=gender,
    #     level=level,
    #     search=search,
    # )

    return students


@router.post("/")
async def add_attendance(
    education_year: str,
    student_id_number: str,
    semester: str,
    count: int,
    current_user=Depends(PermissionChecker(["add_attendance", "all"])),
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


@router.patch("/{id}")
async def get_attendance(
    id: int,
    count: int,
    education_type_code: str,
    current_user=Depends(PermissionChecker(["patch_attendance", "all"])),
):

    check_attendance = await AttendanceRepository.update_data(
        id=id,
        total_absences=count,
    )
    print(f"{check_attendance=}")
    if not check_attendance:
        return JSONResponse(
            content="Не получилось изменить", status_code=status.HTTP_400_BAD_REQUEST
        )

    attendance = await AchievementTypeRepository.find_by_variable(
        name="Attendance",
        type=education_type_code,
    )
    print(f"{attendance=}")

    if not attendance:
        return JSONResponse(
            content="Не получилось изменить", status_code=status.HTTP_400_BAD_REQUEST
        )

    attendance_scores = await AchievementCriteriaRepository.find_all_by_variable(
        achievement_type_id=attendance.id
    )

    attendance_scores = attendance_scores["data"]
    mark = 5

    if count > 0 and count < 19:
        mark = 0
    elif count > 18:
        mark = -5

    change_attendance = None
    for attendance_score in attendance_scores:
        if attendance_score.score == mark:
            change_attendance = attendance_score

    student_achievement = await StudentAchievementRepository.find_by_variable(
        student_id_number=check_attendance.student_id_number,
        id=check_attendance.student_achievement_id,
        education_year_code=check_attendance.education_year_code,
        education_semester=check_attendance.semester_code,
    )
    if student_achievement:
        await StudentAchievementRepository.update_data(
            id=student_achievement.id,
            achievement_criteria_id=change_attendance.id,
            value=mark,
            added_at=datetime.now(),
        )

    return check_attendance
