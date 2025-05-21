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
    role_id: int


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
                        "number_phone": "Телефон",
                        "role_id": "Роль"
                    }
                ]
            }
        }
        from_attributes = True  # Ранее это было orm_mode = True

router = APIRouter()


from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from api.infrastructure.storage.sqlalchemy.models.asos_models import Employee
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

class EmployeeResponse(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    surname: str
    mail_box: str
    number_phone: str
    role_id: int

    class Config:
        from_attributes = True  # Важно для конвертации SQLAlchemy → Pydantic

router = APIRouter()

@router.get("/employees", response_model=List[EmployeeResponse])  # Убрал слэш в конце
async def get_employees(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, le=1000, description="Лимит записей"),
    session: AsyncSession = Depends(get_async_session),
) -> List[EmployeeResponse]:
    """
    Получить список сотрудников.
    """
    result = await session.execute(
        select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.surname,
            Employee.mail_box,
            Employee.number_phone,
            Employee.role_id
        ).offset(skip).limit(limit)
    )
    # Явно преобразуем результат в словари
    employees = [
        {
            "employee_id": emp.employee_id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "surname": emp.surname,
            "mail_box": emp.mail_box,
            "number_phone": emp.number_phone,
            "role_id": emp.role_id
        }
        for emp in result.all()
    ]
    
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