from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.infrastructure.storage.sqlalchemy.models.asos_models import Employee
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from pydantic import BaseModel

class EmployeeResponse(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    surname: str
    mail_box: str
    number_phone: str


    class Config:
        model_config = {
            "from_attributes": True,
            "json_schema_extra": {
                "examples": [
                    {
                        "employee_id": 1,
                        "first_name": "Имя",
                        "last_name": "Отчество",
                        "surname": "Фамилия",
                        "mail_box": "Почта",
                        "number_phone": "Телефон"
                    }
                ]
            }
        }
        from_attributes = True  # Ранее это было orm_mode = True

router = APIRouter()


@router.get("/employees/", response_model=List[EmployeeResponse])
async def get_employees(
        skip: int = Query(0, description="Количество записей для пропуска"),
        limit: int = Query(100, description="Лимит записей"),
        session: AsyncSession = Depends(get_async_session),
) -> List[EmployeeResponse]:
    """
    Получить список сотрудников с пагинацией.

    :param skip: Количество записей для пропуска
    :param limit: Максимальное количество возвращаемых записей
    :param session: Асинхронная сессия SQLAlchemy
    :return: Список сотрудников в формате EmployeeResponse
    """
    result = await session.execute(
        select(Employee).offset(skip).limit(limit)  # Исправлено: добавлена закрывающая скобка
    )
    employees = result.scalars().all()
    return employees

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
        employee_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получить информацию о сотруднике по его ID.

    :param employee_id: ID сотрудника.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Информация о сотруднике.
    """
    # Выполняем запрос к базе данных
    result = await session.execute(
        select(Employee).where(Employee.employee_id == employee_id)
    )
    employee = result.scalar_one_or_none()

    # Если сотрудник не найден, возвращаем 404
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудник с ID {employee_id} не найден."
        )

    # Возвращаем данные сотрудника
    return employee