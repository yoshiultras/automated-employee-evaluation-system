# metrics_quartal.py
from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import MetricsInQuartal
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

# Pydantic схемы
class MetricsInQuartalBase(BaseModel):
    quartal: int
    duration: Optional[List[int]] = None
    metrics_id: Optional[List[int]] = None

class MetricsInQuartalCreate(MetricsInQuartalBase):
    pass

class MetricsInQuartalResponse(MetricsInQuartalBase):
    id: int

    class Config:
        orm_mode = True

router = APIRouter()

@router.get(
    path="/metrics-quartals/",
    response_model=List[MetricsInQuartalResponse],
    status_code=status.HTTP_200_OK
)
async def read_metrics_quartals(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(MetricsInQuartal)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении данных: {str(e)}"
        )

@router.get(
    path="/metrics-quartals/{quartal}",
    response_model=List[MetricsInQuartalResponse],
    status_code=status.HTTP_200_OK
)
async def read_metrics_quartal(
    quartal: int,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(MetricsInQuartal)
        .where(MetricsInQuartal.quartal == quartal)
    )
    items = result.scalars().all()
    if not items:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return items

@router.post(
    path="/metrics-quartals/",
    response_model=MetricsInQuartalResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_metrics_quartal(
    data: MetricsInQuartalCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        db_item = MetricsInQuartal(**data.dict())
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании записи: {str(e)}"
        )

@router.put(
    path="/metrics-quartals/{id}",
    response_model=MetricsInQuartalResponse,
    status_code=status.HTTP_200_OK
)
async def update_metrics_quartal(
    id: int,
    data: MetricsInQuartalCreate,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(MetricsInQuartal)
        .where(MetricsInQuartal.id == id)
    )
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    try:
        for key, value in data.dict().items():
            setattr(db_item, key, value)
        
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при обновлении записи: {str(e)}"
        )

@router.delete(
    path="/metrics-quartals/{id}",
    status_code=status.HTTP_200_OK
)
async def delete_metrics_quartal(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(MetricsInQuartal)
        .where(MetricsInQuartal.id == id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    try:
        await session.delete(item)
        await session.commit()
        return {"message": "Запись успешно удалена"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при удалении записи: {str(e)}"
        )