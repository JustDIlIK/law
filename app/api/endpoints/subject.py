from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.db.repository.student_subject import StudentSubjectRepository

router = APIRouter(
    prefix="/subjects",
    tags=["Предметы"],
)


@router.get("/{student_id_number}")
async def get_subject_info(
    student_id_number: str,
    semester_code: str,
    current_user=Depends(PermissionChecker(["get_subjects", "all"])),
):

    subjects_info = await StudentSubjectRepository.find_all_by_variable(
        student_id=student_id_number,
        semester_code=semester_code,
    )

    return subjects_info
