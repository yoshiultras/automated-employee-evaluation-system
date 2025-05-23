from sqlalchemy import select, case, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from api.infrastructure.storage.sqlalchemy.models.asos_models import (
    ActualWorkingDaysOnEmployee,
    Employee,
    Department,
    FacultyAndInstitute
)
from typing import List, Dict

router = APIRouter()
@router.get(
    path="/employees-to-departments/",
    status_code=status.HTTP_200_OK
)
async def get_department_heads_info(
    session: AsyncSession = Depends(get_async_session)
) -> List[Dict]:
    """
    Получает полную информацию о заведующих кафедрами по месяцам
    
    Args:
        session: асинхронная сессия SQLAlchemy
        
    Returns:
        Список словарей с полной информацией о заведующих кафедрами:
        - Кафедра (название)
        - Факультет/институт
        - Месяц (на русском)
        - Год
        - ФИО руководителя
        - Должность
        - Количество рабочих дней
    """
    month_case = case(
        (ActualWorkingDaysOnEmployee.month == 1, "Январь"),
        (ActualWorkingDaysOnEmployee.month == 2, "Февраль"),
        (ActualWorkingDaysOnEmployee.month == 3, "Март"),
        (ActualWorkingDaysOnEmployee.month == 4, "Апрель"),
        (ActualWorkingDaysOnEmployee.month == 5, "Май"),
        (ActualWorkingDaysOnEmployee.month == 6, "Июнь"),
        (ActualWorkingDaysOnEmployee.month == 7, "Июль"),
        (ActualWorkingDaysOnEmployee.month == 8, "Август"),
        (ActualWorkingDaysOnEmployee.month == 9, "Сентябрь"),
        (ActualWorkingDaysOnEmployee.month == 10, "Октябрь"),
        (ActualWorkingDaysOnEmployee.month == 11, "Ноябрь"),
        (ActualWorkingDaysOnEmployee.month == 12, "Декабрь"),
        else_="Неизвестный месяц"
    ).label("month_name")
    
    query = (
        select(
            Department.name_of_department.label("department_name"),
            FacultyAndInstitute.name.label("faculty_name"),
            month_case,
            ActualWorkingDaysOnEmployee.year,
            func.concat(
                Employee.last_name, " ",
                Employee.first_name, " ",
                Employee.surname
            ).label("full_name"),
            ActualWorkingDaysOnEmployee.jobtitle,
            ActualWorkingDaysOnEmployee.count_day
        )
        .join(Employee, ActualWorkingDaysOnEmployee.employee_id == Employee.employee_id)
        .join(Department, ActualWorkingDaysOnEmployee.department_id == Department.id)
        .join(FacultyAndInstitute, Department.id_facultet == FacultyAndInstitute.id)
        .order_by(
            Department.name_of_department,
            ActualWorkingDaysOnEmployee.year,
            ActualWorkingDaysOnEmployee.month
        )
    )
    
    result = await session.execute(query)
    rows = result.all()
    
    return [
        {
            "department": row.department_name,
            "faculty": row.faculty_name,
            "month": row.month_name,
            "year": row.year,
            "head_name": row.full_name,
            "position": row.jobtitle,
            "working_days": row.count_day
        }
        for row in rows
    ]