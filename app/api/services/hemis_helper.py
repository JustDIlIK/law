import asyncio
import uuid
from collections import Counter
from datetime import datetime, timedelta

import httpx
import uvicorn
from httpx import AsyncClient
from sqlalchemy import select

from app.api.services.auth import get_hashed_password
from app.api.services.dates import from_seconds_to_date
from app.api.services.image import download_image
from app.config.config import settings
from app.db.connection import async_session
from app.db.models import LocationType, Student
from app.db.repository.academic_degree import AcademicDegreeRepository
from app.db.repository.academic_rank import AcademicRankRepository
from app.db.repository.accommodation import AccommodationRepository
from app.db.repository.citizenship import CitizenshipRepository
from app.db.repository.country import CountryRepository
from app.db.repository.department import DepartmentRepository
from app.db.repository.education_form import EducationFormRepository
from app.db.repository.education_language import EducationLanguageRepository
from app.db.repository.education_type import EducationTypeRepository
from app.db.repository.education_year import EducationYearRepository
from app.db.repository.employee import EmployeeRepository
from app.db.repository.employee_status import EmployeeStatusRepository
from app.db.repository.employee_type import EmployeeTypeRepository
from app.db.repository.employment_form import EmploymentFormRepository
from app.db.repository.employment_staff import EmploymentStaffRepository
from app.db.repository.gender import GenderRepository
from app.db.repository.group import GroupRepository
from app.db.repository.level import LevelRepository
from app.db.repository.locality_type import LocalityTypeRepository
from app.db.repository.location import LocationRepository
from app.db.repository.payment_form import PaymentFormRepository
from app.db.repository.role import RoleRepository
from app.db.repository.semester import SemesterRepository
from app.db.repository.social_category import SocialCategoryRepository
from app.db.repository.specialty import SpecialtyRepository
from app.db.repository.staff_position import StaffPositionRepository
from app.db.repository.structure_type import StructureTypeRepository
from app.db.repository.student import StudentRepository
from app.db.repository.student_achievement import StudentAchievementRepository
from app.db.repository.student_status import StudentStatusRepository
from app.db.repository.student_subject import StudentSubjectRepository
from app.db.repository.student_type import StudentTypeRepository
from app.db.repository.university import UniversityRepository


async def fetch_employees(
    url: str,
    limit: int = 200,
    page: int = 1,
):
    async with AsyncClient() as client:
        response = await client.get(
            url=f"{url}&limit={limit}&page={page}",
            headers={"Authorization": f"Bearer {settings.HEMIS_TOKEN}"},
        )
        response.raise_for_status()
        return response.json()


async def fetch_students(
    url: str,
    limit: int = 200,
    page: int = 1,
):
    async with AsyncClient() as client:
        response = await client.get(
            url=f"{url}?limit={limit}&page={page}&search=400231100332",
            headers={"Authorization": f"Bearer {settings.HEMIS_TOKEN}"},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


async def fetch_student(
    url: str,
    student_id_number: str,
    student_hemis_id: int,
):
    print(f"{url=}")
    async with AsyncClient() as client:

        response = await client.get(
            url=f"{url}?student_id_number={student_id_number}&student_id={student_hemis_id}",
            headers={"Authorization": f"Bearer {settings.HEMIS_TOKEN}"},
        )
        response.raise_for_status()
        return response.json()


async def add_employee(employees_list: list, outsider_list: list = []):

    if not employees_list:
        employees_list = outsider_list.copy()
        outsider_list.clear()

    employee_role = await RoleRepository.find_by_variable(name="employee")

    if not employee_role:
        employee_role = await RoleRepository.add_record(name="employee")

    index = 0

    for employee_element in employees_list:

        emp = {
            "external_id": employee_element["id"],
            "full_name": employee_element["full_name"],
            "short_name": employee_element["short_name"],
            "first_name": employee_element["first_name"],
            "second_name": employee_element["second_name"],
            "third_name": employee_element["third_name"],
            "employee_id_number": employee_element["employee_id_number"],
            "dob": from_seconds_to_date(employee_element["birth_date"]),
            "image_url": "uploads/template.jpg",
            "year_of_enter": employee_element["year_of_enter"],
            "specialty": employee_element["specialty"],
            "contract_number": employee_element["contract_number"],
            "decree_number": employee_element["decree_number"],
            "contract_date": from_seconds_to_date(employee_element["contract_date"]),
            "decree_date": from_seconds_to_date(employee_element["decree_date"]),
            "created_at": from_seconds_to_date(employee_element["created_at"]),
            "updated_at": from_seconds_to_date(employee_element["updated_at"]),
            "is_active": employee_element["active"],
            "login": employee_element["second_name"],
            "password": get_hashed_password(employee_element["second_name"]),
            "role_id": employee_role.id,
        }

        # Пол

        employee_gender = employee_element["gender"]
        gender = await GenderRepository.find_by_variable(code=employee_gender["code"])
        if not gender:
            gender = await GenderRepository.add_record(**employee_gender)
        emp["gender_code"] = gender.code

        # Фото

        employee_image = employee_element["image"]
        if employee_image:
            filename = uuid.uuid4()
            filetype = employee_image.split(".")[-1]
            emp["image_url"] = f"uploads/employee/{filename}.{filetype}"
            await download_image(employee_image, emp["image_url"])

        # Академ уров

        employee_academic_degree = employee_element["academicDegree"]
        academic_degree = await AcademicDegreeRepository.find_by_variable(
            code=employee_academic_degree["code"]
        )
        if not academic_degree:
            academic_degree = await AcademicDegreeRepository.add_record(
                **employee_academic_degree
            )
        emp["academic_degree_code"] = academic_degree.code

        # Академ ранк

        employee_academic_rank = employee_element["academicRank"]
        academic_rank = await AcademicRankRepository.find_by_variable(
            code=employee_academic_rank["code"]
        )
        if not academic_rank:
            academic_rank = await AcademicRankRepository.add_record(
                **employee_academic_rank
            )
        emp["academic_rank_code"] = academic_rank.code

        # Департамент

        employee_department = employee_element["department"]
        department = await DepartmentRepository.find_by_variable(
            code=employee_department["code"]
        )
        if not department:

            department = await DepartmentRepository.find_by_variable(
                external_id=employee_department["parent"]
            )

            if not department and employee_department["parent"]:
                outsider_list.append(employees_list[index])
                continue

            structure_type = await StructureTypeRepository.find_by_variable(
                code=employee_department["structureType"]["code"]
            )
            if not structure_type:
                await StructureTypeRepository.add_record(
                    **employee_department["structureType"]
                )

            locality_type = await LocalityTypeRepository.find_by_variable(
                code=employee_department["localityType"]["code"]
            )
            if not locality_type:
                await LocalityTypeRepository.add_record(
                    **employee_department["localityType"]
                )
            print(f"{employee_department=}")
            employee_department["structure_type_code"] = employee_department.pop(
                "structureType"
            )["code"]
            employee_department["locality_type_code"] = employee_department.pop(
                "localityType"
            )["code"]
            employee_department["parent_id"] = employee_department.pop("parent")
            employee_department["external_id"] = employee_department.pop("id")
            if employee_department["parent_id"] == 1:
                employee_department["parent_id"] = None
            print(f"{employee_department=}")

            department = await DepartmentRepository.add_record(**employee_department)
        emp["department_code"] = department.code

        # Сотрудник форм

        employee_employment_form = employee_element["employmentForm"]
        employment_form = await EmploymentFormRepository.find_by_variable(
            code=employee_employment_form["code"]
        )
        if not employment_form:
            employment_form = await EmploymentFormRepository.add_record(
                **employee_employment_form
            )
        emp["employment_form_code"] = employment_form.code

        # Сотрудник стафф

        employee_employment_staff = employee_element["employmentStaff"]
        employment_staff = await EmploymentStaffRepository.find_by_variable(
            code=employee_employment_staff["code"]
        )
        if not employment_staff:
            employment_staff = await EmploymentStaffRepository.add_record(
                **employee_employment_staff
            )
        emp["employment_staff_code"] = employment_staff.code

        # Сотрудник стафф позиция

        employee_employment_staff_position = employee_element["staffPosition"]
        staff_position = await StaffPositionRepository.find_by_variable(
            code=employee_employment_staff_position["code"]
        )
        if not staff_position:
            staff_position = await StaffPositionRepository.add_record(
                **employee_employment_staff_position
            )
        emp["staff_position_code"] = staff_position.code

        # Сотрудник статус

        employee_status = employee_element["employeeStatus"]
        status = await EmployeeStatusRepository.find_by_variable(
            code=employee_status["code"]
        )
        if not status:
            status = await EmployeeStatusRepository.add_record(**employee_status)
        emp["employee_status_code"] = status.code

        # Сотрудник тип

        employee_type = employee_element["employeeType"]
        emp_type = await EmployeeTypeRepository.find_by_variable(
            code=employee_type["code"]
        )
        if not emp_type:
            emp_type = await EmployeeTypeRepository.add_record(**employee_type)
        emp["employee_type_code"] = emp_type.code
        print(f"{emp=}")
        await EmployeeRepository.add_record(**emp)

        print(f"{gender=}")
        print(f"{emp=}")
        index += 1

    print("Finished")
    if outsider_list:
        await add_employee([], outsider_list)


async def get_employee_list():
    page = 1
    limit = 200

    while True:

        data = await fetch_employees(
            url=settings.HEMIS_GET_EMPLOYEES,
            limit=limit,
            page=page,
        )
        data = data["data"]
        page += 1
        page_count = data["pagination"]["pageCount"]

        # Сверка/Добавление в БД
        await add_employee(data["items"])

        if page > page_count:
            break

    print("Finished")


async def add_student(students_list: list):

    student_role = await RoleRepository.find_by_variable(name="student")

    if not student_role:
        student_role = await RoleRepository.add_record(name="student")

    for student_element in students_list:

        # Универ

        stud = {
            "external_id": student_element["id"],
            "full_name": student_element["full_name"],
            "short_name": student_element["short_name"],
            "first_name": student_element["first_name"],
            "second_name": student_element["second_name"],
            "third_name": student_element["third_name"],
            "student_id_number": student_element["student_id_number"],
            "dob": from_seconds_to_date(student_element["birth_date"]),
            "image_url": "uploads/template.jpg",
            "avg_gpa": student_element["avg_gpa"],
            "avg_grade": student_element["avg_grade"],
            "total_credit": student_element["total_credit"],
            "year_of_enter": student_element["year_of_enter"],
            "created_at": from_seconds_to_date(student_element["created_at"]),
            "updated_at": from_seconds_to_date(student_element["updated_at"]),
            "login": f"{student_element['second_name'].lower()}_{student_element['first_name'].lower()}",
            "password": get_hashed_password(student_element["second_name"]),
            "role_id": student_role.id,
            "is_graduate": student_element["is_graduate"],
            "total_acload": student_element["total_acload"],
            "other": student_element["other"],
            "validate_url": student_element["validateUrl"],
            "email": student_element["email"],
            "curriculum_id": student_element["_curriculum"],
        }

        print(f"{stud=}")
        student_university = student_element["university"]
        university = await UniversityRepository.find_by_variable(
            code=student_university["code"]
        )
        if not university:
            university = await UniversityRepository.add_record(**student_university)
        stud["university_code"] = university.code

        # Пол

        student_gender = student_element["gender"]
        gender = await GenderRepository.find_by_variable(code=student_gender["code"])
        if not gender:
            gender = await GenderRepository.add_record(**student_gender)
        stud["gender_code"] = gender.code

        # Фото

        student_image = student_element["image"]
        if student_image:
            filename = uuid.uuid4()
            filetype = student_image.split(".")[-1]
            stud["image_url"] = f"uploads/students/{filename}.{filetype}"
            await download_image(student_image, stud["image_url"])

        # Страна

        student_country = student_element["country"]
        country = await CountryRepository.find_by_variable(code=student_country["code"])
        if not country:
            country = await CountryRepository.add_record(**student_country)
        stud["country_code"] = country.code

        # Провинция

        student_province = student_element["province"]
        student_province["parent_id"] = student_province.pop("_parent")
        student_province["type"] = LocationType.province

        province = await LocationRepository.find_by_variable(
            code=student_province["code"]
        )
        if not province:
            province = await LocationRepository.add_record(**student_province)
        stud["province_code"] = province.code

        # ---Текущая---

        student_current_province = student_element["currentProvince"]

        if student_current_province:
            student_current_province["parent_id"] = student_current_province.pop(
                "_parent"
            )
            student_current_province["type"] = LocationType.province

            current_province = await LocationRepository.find_by_variable(
                code=student_current_province["code"]
            )
            if not current_province:
                current_province = await LocationRepository.add_record(
                    **student_current_province
                )
            stud["current_province_code"] = current_province.code

        # Улица

        student_district = student_element["district"]
        student_district["parent_id"] = student_district.pop("_parent")
        student_district["type"] = LocationType.district

        district = await LocationRepository.find_by_variable(
            code=student_district["code"]
        )
        if not district:
            district = await LocationRepository.add_record(**student_district)
        stud["district_code"] = district.code

        # ---Текущая---

        student_current_district = student_element["currentDistrict"]
        if student_current_district:
            student_current_district["parent_id"] = student_current_district.pop(
                "_parent"
            )
            student_current_district["type"] = LocationType.district
            current_district = await LocationRepository.find_by_variable(
                code=student_current_district["code"]
            )
            if not current_district:
                current_district = await LocationRepository.add_record(
                    **student_current_district
                )
            stud["current_district_code"] = current_district.code

        # Местность

        student_terrain = student_element["terrain"]
        if student_terrain:
            student_terrain["type"] = LocationType.terrain

            terrain = await LocationRepository.find_by_variable(
                code=student_terrain["code"]
            )
            if not terrain:
                terrain = await LocationRepository.add_record(**student_terrain)
            stud["terrain_code"] = terrain.code

        # ---Текущая---

        student_current_terrain = student_element["currentTerrain"]
        if student_current_terrain:
            student_current_terrain["type"] = LocationType.terrain

            current_terrain = await LocationRepository.find_by_variable(
                code=student_current_terrain["code"]
            )
            if not current_terrain:
                current_terrain = await LocationRepository.add_record(
                    **student_current_terrain
                )
            stud["current_terrain_code"] = current_terrain.code

        # Гражданство

        student_citizenship = student_element["citizenship"]
        citizenship = await CitizenshipRepository.find_by_variable(
            code=student_citizenship["code"]
        )
        if not citizenship:
            citizenship = await CitizenshipRepository.add_record(**student_citizenship)
        stud["citizenship_code"] = citizenship.code

        # Статус Студента

        student_status = student_element["studentStatus"]
        status = await StudentStatusRepository.find_by_variable(
            code=student_status["code"]
        )
        if not status:
            status = await StudentStatusRepository.add_record(**student_status)
        stud["student_status_code"] = status.code

        # Форма образнования

        student_education_form = student_element["educationForm"]
        education_form = await EducationFormRepository.find_by_variable(
            code=student_education_form["code"]
        )
        if not education_form:
            education_form = await EducationFormRepository.add_record(
                **student_education_form
            )
        stud["education_form_code"] = education_form.code

        # Тип образнования

        student_education_type = student_element["educationType"]
        education_type = await EducationTypeRepository.find_by_variable(
            code=student_education_type["code"]
        )
        if not education_type:
            education_type = await EducationTypeRepository.add_record(
                **student_education_type
            )
        stud["education_type_code"] = education_type.code

        # Тип обучения

        student_payment_form = student_element["paymentForm"]
        payment_form = await PaymentFormRepository.find_by_variable(
            code=student_payment_form["code"]
        )
        if not payment_form:
            payment_form = await PaymentFormRepository.add_record(
                **student_payment_form
            )
        stud["payment_form_code"] = payment_form.code

        # Тип студента

        student_student_type = student_element["studentType"]
        student_type = await StudentTypeRepository.find_by_variable(
            code=student_student_type["code"]
        )
        if not student_type:
            student_type = await StudentTypeRepository.add_record(
                **student_student_type
            )
        stud["student_type_code"] = student_type.code

        # Социальная категория

        student_social = student_element["socialCategory"]
        social = await SocialCategoryRepository.find_by_variable(
            code=student_social["code"]
        )
        if not social:
            social = await SocialCategoryRepository.add_record(**student_social)
        stud["social_category_code"] = social.code

        # Жилье

        student_accommodation = student_element["accommodation"]
        accommodation = await AccommodationRepository.find_by_variable(
            code=student_accommodation["code"]
        )
        if not accommodation:
            accommodation = await AccommodationRepository.add_record(
                **student_accommodation
            )
        stud["accommodation_code"] = accommodation.code

        # Департамент

        student_department = student_element["department"]
        department = await DepartmentRepository.find_by_variable(
            code=student_department["code"]
        )
        if not department:
            structure_type = await StructureTypeRepository.find_by_variable(
                code=student_department["structureType"]["code"]
            )
            if not structure_type:
                await StructureTypeRepository.add_record(
                    **student_department["structureType"]
                )

            locality_type = await LocalityTypeRepository.find_by_variable(
                code=student_department["localityType"]["code"]
            )
            if not locality_type:
                await LocalityTypeRepository.add_record(
                    **student_department["localityType"]
                )
            print(f"{student_department=}")
            student_department["structure_type_code"] = student_department.pop(
                "structureType"
            )["code"]
            student_department["locality_type_code"] = student_department.pop(
                "localityType"
            )["code"]
            student_department["parent_id"] = student_department.pop("parent")
            student_department["external_id"] = student_department.pop("id")
            if student_department["parent_id"] == 1:
                student_department["parent_id"] = None
            department = await DepartmentRepository.add_record(**student_department)
        stud["department_code"] = department.code

        # Специализация

        student_specialty = student_element["specialty"]
        specialty = await SpecialtyRepository.find_by_variable(
            code=student_specialty["code"]
        )
        if not specialty:
            specialty = await SpecialtyRepository.add_record(**student_specialty)
        stud["specialty_code"] = specialty.code

        # Группы

        student_group = student_element["group"]
        group = await GroupRepository.find_by_id(student_group["id"])
        if not group:
            education_lang = await EducationLanguageRepository.find_by_variable(
                code=student_group["educationLang"]["code"]
            )
            if not education_lang:
                await EducationLanguageRepository.add_record(
                    **student_group["educationLang"]
                )
            student_group["education_lang_code"] = student_group.pop("educationLang")[
                "code"
            ]
            group = await GroupRepository.add_record(**student_group)
        stud["group_id"] = group.id

        # Уровень

        student_level = student_element["level"]
        level = await LevelRepository.find_by_variable(code=student_level["code"])
        if not level:
            level = await LevelRepository.add_record(**student_level)
        stud["level_code"] = level.code

        # Специализация

        student_specialty = student_element["specialty"]
        specialty = await SpecialtyRepository.find_by_variable(
            code=student_specialty["code"]
        )
        if not specialty:
            specialty = await SpecialtyRepository.add_record(**student_specialty)
        stud["specialty_code"] = specialty.code

        # Учебный год

        student_education_year = student_element["educationYear"]
        education_year = await EducationYearRepository.find_by_variable(
            code=student_education_year["code"]
        )
        if not education_year:
            education_year = await EducationYearRepository.add_record(
                **student_education_year
            )
        stud["education_year_code"] = education_year.code

        # Семестр

        student_semester = student_element["semester"]
        semester = await SemesterRepository.find_by_variable(
            code=student_semester["code"]
        )
        if not semester:
            student_semester["academic_year_code"] = student_education_year["code"]
            semester = await SemesterRepository.add_record(**student_semester)
        stud["semester_code"] = semester.code

        await StudentRepository.add_record(**stud)


async def get_student_list():
    page = 1
    limit = 200

    while True:

        try:
            data = await fetch_students(
                url=settings.HEMIS_GET_STUDENTS,
                limit=limit,
                page=page,
            )
            data = data["data"]
            page += 1

            await add_student(data["items"])

            page_count = data["pagination"]["pageCount"]
            if page > page_count:
                break
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {e}")

    print("Finished")


async def save_student_from_api():
    page = 1
    limit = 100

    while True:
        students = await StudentRepository.get_all(
            page,
            limit,
        )
        students = students["data"]
        if not students:
            break
        for student in students:
            data = await fetch_student(
                url=settings.HEMIS_GET_STUDENT,
                student_id_number=student.student_id_number,
                student_hemis_id=student.external_id,
            )
            data = data["data"]
            for gpa in data.get("studentGpas", []):

                print(f"{gpa=}")

                # await StudentAchievementRepository.add_record(
                #     student_id_number=student.student_id_number,
                #     achievement_criteria_id=2,
                #     document_url=None,
                #     value=float(gpa["gpa"]),
                #     level_code=gpa["level"]["code"],
                #     year_code=gpa["educationYear"]["code"],
                # )

            for subj in data.get("subjects", []):
                await StudentSubjectRepository.add_record(
                    student_id=student.student_id_number,
                    position=subj["position"],
                    name=subj["name"],
                    subject_type_code=subj["subjectType"]["code"],
                    subject_type_name=subj["subjectType"]["name"],
                    semester_code=subj["semester"]["code"],
                    credit=subj["credit"],
                    grade=subj["grade"],
                    total_point=subj["total_point"],
                    exam_finish_code=subj["subjectType"]["code"],
                    exam_finish_name=subj["subjectType"]["name"],
                )
        page += 1
