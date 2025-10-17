from datetime import datetime

from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.achievement_type import AchievementTypeRepository
from app.db.repository.attendance import AttendanceRepository
from app.db.repository.rating import RatingRepository
from app.db.repository.status import StatusRepository
from app.db.repository.student_achievement import StudentAchievementRepository


async def check_achievements(
    students: list,
    education_type_code: str,
    group_id: int = None,
):
    is_updated = False
    current_year = datetime.now().year

    behavior = await AchievementTypeRepository.find_by_variable(
        name="Behavior", type=education_type_code
    )
    attendance = await AchievementTypeRepository.find_by_variable(
        name="Attendance", type=education_type_code
    )
    status = await StatusRepository.find_by_variable(title="succeed")

    if not (behavior and attendance and status):
        return False

    behavior_el = next((c for c in behavior.criterias if c.score == 5), None)
    attendance_el = next((c for c in attendance.criterias if c.score == 5), None)
    if not (behavior_el and attendance_el):
        return False

    for student in students:
        if student.student_status_code != "11":
            continue

        for year in range(student.year_of_enter, current_year + 1):
            for semester_code in ("1", "2"):
                # Attendance
                is_att = await AttendanceRepository.find_by_variable(
                    education_year_code=str(year),
                    student_id_number=student.student_id_number,
                    semester_code=semester_code,
                )
                if not is_att:
                    sa = await StudentAchievementRepository.add_record(
                        student_id_number=student.student_id_number,
                        achievement_criteria_id=attendance_el.id,
                        education_year_code=str(year),
                        education_type_code=student.education_type_code,
                        education_semester=semester_code,
                        is_verified=True,
                        status_id=status.id,
                        level_code=student.level_code,
                        added_at=datetime.now(),
                        value=attendance_el.score,
                    )
                    await AttendanceRepository.add_record(
                        education_year_code=str(year),
                        semester_code=semester_code,
                        student_id_number=student.student_id_number,
                        total_absences=0,
                        student_achievement_id=sa.id,
                    )

                # Behavior
                is_behavior = await StudentAchievementRepository.find_by_variable(
                    achievement_criteria_id=behavior_el.id,
                    education_year_code=str(year),
                    student_id_number=student.student_id_number,
                    education_semester=semester_code,
                )
                if not is_behavior:
                    await StudentAchievementRepository.add_record(
                        student_id_number=student.student_id_number,
                        achievement_criteria_id=behavior_el.id,
                        is_verified=True,
                        value=behavior_el.score,
                        added_at=datetime.now(),
                        level_code=student.level_code,
                        education_type_code=student.education_type_code,
                        education_year_code=str(year),
                        education_semester=semester_code,
                        status_id=status.id,
                    )
                    is_updated = True

    return is_updated
