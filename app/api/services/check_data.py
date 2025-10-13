from datetime import datetime

from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.achievement_type import AchievementTypeRepository
from app.db.repository.attendance import AttendanceRepository
from app.db.repository.rating import RatingRepository
from app.db.repository.status import StatusRepository
from app.db.repository.student_achievement import StudentAchievementRepository


first_semester = [1, 2, 9, 10, 11, 12]


async def check_achievements(
    students: list,
    education_year_code: str,
    group_id: int = None,
):
    attendance = await AchievementTypeRepository.find_by_variable(name="Attendance")
    attendance_scores = await AchievementCriteriaRepository.find_all_by_variable(
        achievement_type_id=attendance.id
    )
    mark = 5
    change_attendance = None

    for attendance_score in attendance_scores["data"]:
        if attendance_score.score == mark:
            change_attendance = attendance_score

    is_updated = False

    behavior = await AchievementTypeRepository.find_by_variable(name="Behavior")
    attendance = await AchievementTypeRepository.find_by_variable(name="Attendance")
    behavior_element = None
    attendance_element = None

    for behavior_criteria in behavior.criterias:
        if behavior_criteria.score == 5:
            behavior_element = behavior_criteria

    for attendance_criteria in attendance.criterias:
        if attendance_criteria.score == 5:
            attendance_element = attendance_criteria

    status = await StatusRepository.find_by_variable(title="succeed")

    if behavior_element and status and attendance_element:
        for student in students:

            year_dif = int(education_year_code) - student.year_of_enter
            need_add = 0
            if datetime.now().month not in [9, 10, 11, 12, 1, 2]:
                need_add += 1
            if (
                0 <= year_dif < 5
                and int(education_year_code) >= student.year_of_enter
                and student.student_status_code == "11"
            ):
                semester_num = str(11 + need_add + (year_dif * 2))
                is_added_attendance = await AttendanceRepository.find_by_variable(
                    education_year_code=education_year_code,
                    student_id_number=student.student_id_number,
                    semester_code=semester_num,
                )

                if not is_added_attendance:
                    if not student.attendance_records:
                        student_achievement = (
                            await StudentAchievementRepository.add_record(
                                student_id_number=student.student_id_number,
                                achievement_criteria_id=change_attendance.id,
                                education_year_code=education_year_code,
                                education_type_code=student.education_type_code,
                                education_semester=semester_num,
                                added_at=datetime.now(),
                                level_code=student.level_code,
                                status_id=status.id,
                                value=mark,
                            )
                        )

                        await AttendanceRepository.add_record(
                            education_year_code=education_year_code,
                            semester_code=semester_num,
                            student_id_number=student.student_id_number,
                            total_absences=0,
                            student_achievement_id=student_achievement.id,
                        )
                    else:

                        is_added = await AttendanceRepository.find_all_by_variable(
                            student_id_number=student.student_id_number,
                            semester_code=semester_num,
                            education_year_code=education_year_code,
                            group_id=group_id,
                        )

                        if not is_added:
                            await AttendanceRepository.add_record(
                                education_year_code=education_year_code,
                                semester_code=semester_num,
                                student_id_number=student.student_id_number,
                                total_absences=0,
                            )
                            await StudentAchievementRepository.add_record(
                                student_id_number=student.student_id_number,
                                achievement_criteria_id=change_attendance.id,
                                education_year_code=education_year_code,
                                education_type_code=student.education_type_code,
                                education_semester=semester_num,
                                added_at=datetime.now(),
                                level_code=student.level_code,
                                status_id=status.id,
                                value=mark,
                            )

                is_added = await StudentAchievementRepository.find_by_variable(
                    achievement_criteria_id=behavior_element.id,
                    education_year_code=education_year_code,
                    student_id_number=student.student_id_number,
                    education_semester=semester_num,
                )

                print(f"{is_added=}")
                if not is_added:
                    if not student.student_achievements:
                        await StudentAchievementRepository.add_record(
                            student_id_number=student.student_id_number,
                            achievement_criteria_id=behavior_element.id,
                            is_verified=True,
                            value=behavior_element.score,
                            added_at=datetime.now(),
                            level_code=student.level_code,
                            education_type_code=student.education_type_code,
                            education_year_code=education_year_code,
                            education_semester=semester_num,
                            status_id=status.id,
                        )
                        is_updated = True

                    else:
                        is_has = False

                        for student_achievement in student.student_achievements:
                            if (
                                student_achievement.achievement_criteria_id
                                == behavior_element.id
                            ):
                                is_has = True

                        if not is_has:
                            await StudentAchievementRepository.add_record(
                                student_id_number=student.student_id_number,
                                achievement_criteria_id=behavior_element.id,
                                is_verified=True,
                                value=behavior_element.score,
                                added_at=datetime.now(),
                                level_code=student.level_code,
                                education_type_code=student.education_type_code,
                                education_year_code=education_year_code,
                                education_semester=semester_num,
                                status_id=status.id,
                            )
                            is_updated = True

    return is_updated
