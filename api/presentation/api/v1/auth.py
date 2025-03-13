from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import Employee
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from fastapi import APIRouter, Body, Response, Depends, Query
from fastapi.responses import FileResponse
from passlib.context import CryptContext


router = APIRouter()

@router.get(
    path="/auth",
    status_code=status.HTTP_200_OK,
)
async def get_emploee(
    login: str = Query(..., description="Логин"),
    password: str = Query(..., description="Пароль"),
    sessions: AsyncSession = Depends(get_async_session)
    ):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = pwd_context.hash(password)
    query = select(Employee).where(Employee.login == login and Employee.password == password_hash)
    result = await sessions.execute(query)
    list_user = result.one_or_none()
    if list_user is None:
        return {"status": "Employee not found"}
    response_data = {
        "employee_id": list_user[0].employee_id
    }
    return {"status": "OK", "data": response_data}
