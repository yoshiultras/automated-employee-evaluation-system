from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import EmployeesToMetrics
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

# Pydantic схемы
class EmployeesToMetricsBase(BaseModel):
    metrics_id: List[int] = Field(..., description="Список ID метрик")
    value: Optional[List[int]] = Field(..., description="Список значений для метрик")
    year: int = Field(..., description="Год")
    quarter: int = Field(..., description="Квартал (1-4)")
    employee_id: int = Field(..., description="ID сотрудника")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "metrics_id": [1, 2, 3],
                    "value": [10, 20, 30],
                    "year": 2023,
                    "quarter": 1,
                    "employee_id": 1
                }
            ]
        }
    }

class EmployeesToMetricsCreate(EmployeesToMetricsBase):
    pass

class EmployeesToMetricsResponse(EmployeesToMetricsBase):
    id: int

    class Config:
        orm_mode = True
        model_config = {
            "from_attributes": True,
            "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "metrics_id": [1, 2, 3],
                        "value": [10, 20, 30],
                        "year": 2023,
                        "quarter": 1,
                        "employee_id": 1
                    }
                ]
            }
        }

router = APIRouter()

# EmployeesToMetrics Endpoints
@router.get(
    path="/employees-to-metrics/",
    response_model=List[EmployeesToMetricsResponse],
    status_code=status.HTTP_200_OK
)
async def read_employees_to_metrics(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(EmployeesToMetrics).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get(
    path="/employees-to-metrics/{record_id}",
    response_model=EmployeesToMetricsResponse,
    status_code=status.HTTP_200_OK
)
async def read_employee_to_metric(
        record_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(EmployeesToMetrics).where(EmployeesToMetrics.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post(
    path="/employees-to-metrics/",
    response_model=EmployeesToMetricsResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_employee_to_metric(
        record: EmployeesToMetricsCreate,
        session: AsyncSession = Depends(get_async_session)
):
    db_record = EmployeesToMetrics(**record.dict())
    session.add(db_record)
    await session.commit()
    await session.refresh(db_record)
    return db_record

@router.put(
    path="/employees-to-metrics/{record_id}",
    response_model=EmployeesToMetricsResponse,
    status_code=status.HTTP_200_OK
)
async def update_employee_to_metric(
        record_id: int,
        record: EmployeesToMetricsCreate,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(EmployeesToMetrics).where(EmployeesToMetrics.id == record_id)
    )
    db_record = result.scalar_one_or_none()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in record.dict().items():
        setattr(db_record, key, value)

    session.add(db_record)
    await session.commit()
    await session.refresh(db_record)
    return db_record

@router.delete(
    path="/employees-to-metrics/{record_id}",
    status_code=status.HTTP_200_OK
)
async def delete_employee_to_metric(
        record_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(EmployeesToMetrics).where(EmployeesToMetrics.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    await session.delete(record)
    await session.commit()
    return {"message": "Record deleted successfully"}