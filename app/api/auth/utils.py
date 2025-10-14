import asyncio

from app.db.connection import async_session
from app.db.models import Permission


async def seed_permissions():
    permission_names = [
        "all",
        "get_achievements_criteria",
        "add_achievements_criteria",
        "delete_achievements_criteria",
        "get_achievements_types",
        "add_achievements_types",
        "delete_achievements_types",
        "patch_achievements_types",
        "admin_register",
        "get_attendance",
        "add_attendance",
        "patch_attendance",
        "user_register",
        "get_employee",
        "get_employee_id",
        "delete_employee",
        "get_psychology_achievement",
        "add_psychology_achievement",
        "delete_psychology_achievement",
        "patch_psychology_achievement",
        "patch_psychology_scoring",
        "delete_psychology_scoring",
        "add_psychology_scoring",
        "get_psychology_scoring_by_student",
        "get_psychology_scoring",
        "get_rating_student",
        "get_rating",
        "get_all_student",
        "get_all_student_by_id",
        "get_all_student_by_education_year",
        "get_all_student_by_rating",
        "get_all_student_by_search",
        "delete_all_student_by_id",
        "count_achievement",
        "verify_achievement",
        "get_achievement_rating",
        "add_achievement",
        "get_all_achievements_check",
        "get_all_achievements",
        "patch_student_contact",
        "add_student_contact",
        "get_student_contact",
        "delete_student_contact",
        "patch_student_education",
        "delete_student_education",
        "add_student_education",
        "get_student_education",
    ]

    async with async_session() as session:
        for name in permission_names:
            existing = await session.execute(
                Permission.__table__.select().where(Permission.name == name)
            )
            if not existing.first():
                session.add(Permission(name=name))
        await session.commit()
