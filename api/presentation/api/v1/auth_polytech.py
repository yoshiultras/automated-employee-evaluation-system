from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
import httpx
from httpx import AsyncClient

router = APIRouter(
    prefix="/auth_polytech",
    tags=["auth_polytech"]
)

# Модели данных
class LoginRequest(BaseModel):
    login: str
    password: str
    service_name: str = "empl_eval_sys"

class VerifyRequest(BaseModel):
    login: str
    code: int
    service_name: str = "empl_eval_sys"

class TokenResponse(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str

# Конфигурация API
AUTH_API_URL = "https://admin.kd.mospolytech.ru/api/v1/users"
LOGIN_ENDPOINT = f"{AUTH_API_URL}/login"
VERIFY_ENDPOINT = f"{AUTH_API_URL}/verification_auth_code"

async def get_auth_client() -> AsyncClient:
    """Получение асинхронного HTTP клиента"""
    async with AsyncClient(base_url=AUTH_API_URL, timeout=30.0) as client:
        yield client

async def make_auth_request(
    client: AsyncClient,
    endpoint: str,
    payload: Dict
) -> Dict:
    """Общая функция для авторизационных запросов"""
    try:
        response = await client.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Auth API error: {e.response.text}"
        )

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Запрос кода верификации",
    response_model=Dict[str, str]
)
async def login(
    request: LoginRequest,
    client: AsyncClient = Depends(get_auth_client)
):
    """Отправляет данные для входа и инициирует отправку кода верификации"""
    payload = request.dict()
    await make_auth_request(client, LOGIN_ENDPOINT, payload)
    return {"status": "OK"}

@router.post(
    "/verify",
    status_code=status.HTTP_200_OK,
    summary="Подтверждение кода верификации",
    response_model=TokenResponse
)
async def verify(
    request: VerifyRequest,
    client: AsyncClient = Depends(get_auth_client)
):
    """Проверяет код верификации и возвращает токены доступа"""
    payload = request.dict()
    response = await make_auth_request(client, VERIFY_ENDPOINT, payload)
    
    return TokenResponse(
        user_id=response["user_id"],
        access_token=response["access_token"],
        refresh_token=response["refresh_token"]
    )

