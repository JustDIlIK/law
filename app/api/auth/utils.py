import asyncio
from datetime import datetime

from sqlalchemy import insert, select, func

from app.api.services.auth import get_hashed_password
from app.config.config import settings
from app.db.connection import async_session
from app.db.models import Permission, Admin, User
from app.db.repository.gender import GenderRepository
from app.db.repository.role import RoleRepository


async def seed_permissions():
    permission_items = [
        ("all", "Полный доступ к системе"),
        ("change_own_password", "Изменить собственный пароль"),
        ("change_password_by_admin", "Изменить пароль пользователя (администратором)"),
        ("get_role", "Просмотр ролей"),
        ("add_role", "Добавить новую роль"),
        ("patch_role", "Редактировать роль"),
        ("delete_role", "Удалить роль"),
        ("get_rating_own_student", "Просмотр рейтинга своих студентов"),
        ("get_rating_by_course", "Просмотр рейтинга по курсу"),
        ("get_permission", "Просмотр разрешений"),
        ("add_permission_to_role", "Добавить разрешения к роли"),
        ("delete_permission_from_role", "Удалить разрешения из роли"),
        ("get_achievements_criteria", "Просмотр критериев достижений"),
        ("add_achievements_criteria", "Добавить критерий достижения"),
        ("delete_achievements_criteria", "Удалить критерий достижения"),
        ("get_achievements_types", "Просмотр типов достижений"),
        ("add_achievements_types", "Добавить тип достижения"),
        ("delete_achievements_types", "Удалить тип достижения"),
        ("patch_achievements_types", "Редактировать тип достижения"),
        ("admin_register", "Регистрация администратора"),
        ("get_attendance", "Просмотр посещаемости"),
        ("add_attendance", "Добавить запись посещаемости"),
        ("patch_attendance", "Редактировать запись посещаемости"),
        ("user_register", "Регистрация пользователя"),
        ("get_employee", "Просмотр сотрудников"),
        ("get_employee_id", "Просмотр сотрудника по ID"),
        ("delete_employee", "Удалить сотрудника"),
        ("get_psychology_achievement", "Просмотр психологических достижений"),
        ("add_psychology_achievement", "Добавить психологическое достижение"),
        ("delete_psychology_achievement", "Удалить психологическое достижение"),
        ("patch_psychology_achievement", "Редактировать психологическое достижение"),
        ("patch_psychology_scoring", "Редактировать психологическую оценку"),
        ("delete_psychology_scoring", "Удалить психологическую оценку"),
        ("add_psychology_scoring", "Добавить психологическую оценку"),
        (
            "get_psychology_scoring_by_student",
            "Просмотр психологической оценки студента",
        ),
        ("get_psychology_scoring", "Просмотр всех психологических оценок"),
        ("get_rating_student", "Просмотр рейтинга студента"),
        ("get_rating", "Просмотр всех рейтингов"),
        ("get_all_student", "Просмотр всех студентов"),
        ("get_all_student_by_id", "Просмотр студента по ID"),
        ("get_all_student_by_education_year", "Просмотр студентов по учебному году"),
        ("get_all_student_by_rating", "Просмотр студентов по рейтингу"),
        ("get_all_student_by_search", "Поиск студентов"),
        ("delete_all_student_by_id", "Удалить студента по ID"),
        ("count_achievement", "Подсчёт достижений"),
        ("verify_achievement", "Проверка достижения"),
        ("get_achievement_rating", "Просмотр рейтинга достижений"),
        ("add_achievement", "Добавить достижение"),
        ("get_all_achievements_check", "Проверить все достижения"),
        ("get_all_achievements", "Просмотр всех достижений"),
        ("patch_student_contact", "Редактировать контактные данные студента"),
        ("add_student_contact", "Добавить контакт студента"),
        ("get_student_contact", "Просмотр контактов студента"),
        ("delete_student_contact", "Удалить контакт студента"),
        ("patch_student_education", "Редактировать образование студента"),
        ("delete_student_education", "Удалить образование студента"),
        ("add_student_education", "Добавить образование студента"),
        ("get_student_education", "Просмотр образования студента"),
        ("get_subjects", "Просмотр предметов"),
    ]

    async with async_session() as session:
        for name, title in permission_items:
            existing = await session.execute(
                select(Permission).where(Permission.name == name)
            )
            if not existing.scalar_one_or_none():
                session.add(Permission(name=name, title=title))

        admin_exists = await session.execute(
            select(Admin).where(Admin.email == settings.ADMIN_EMAIL)
        )

        if not admin_exists.scalar_one_or_none():
            new_admin = Admin(
                email=settings.ADMIN_EMAIL,
                password=get_hashed_password(settings.ADMIN_PASS),
            )
            session.add(new_admin)

        user_admin_exists = await session.execute(
            select(User).where(User.login == settings.USER_ADMIN_LOGIN)
        )

        if not user_admin_exists.scalar_one_or_none():

            gender_code = await GenderRepository.find_by_variable(code="11")
            admin_role = await RoleRepository.find_by_variable(name="admin")

            if not admin_role:
                admin_role = await RoleRepository.add_record(
                    name="admin",
                    is_show=True,
                )

            if gender_code:
                new_user_admin = User(
                    login=settings.USER_ADMIN_LOGIN,
                    password=get_hashed_password(settings.USER_ADMIN_PASS),
                    full_name="System Administrator",
                    short_name="Admin",
                    first_name="System",
                    second_name="Administrator",
                    third_name="Admin",
                    gender_code=gender_code.code,
                    role_id=admin_role.id,
                    image_url=None,
                    is_active=True,
                    year_of_enter=datetime.now().year,
                    created_at=func.now(),
                    updated_at=func.now(),
                )

                session.add(new_user_admin)

        await session.commit()
