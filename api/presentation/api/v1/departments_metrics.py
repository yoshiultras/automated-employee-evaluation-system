from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel, Field

from api.infrastructure.storage.sqlalchemy.models.asos_models import DepartmentsMetrics
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

router = APIRouter()

# Pydantic models
class DepartmentsMetricsBase(BaseModel):
    department_id: int
    metrics_id: int
    value: int
    year: int
    quarter: int
    period_date: date
    author_id: int
    status: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "department_id": 1,
                "metrics_id": 2,
                "value": 10,
                "year": 2025,
                "quarter": 1,
                "period_date": "2024-03-31",
                "author_id": 1,
                "status": 1
            }
        }

class DepartmentsMetricsCreate(DepartmentsMetricsBase):
    pass

class DepartmentsMetricsResponse(DepartmentsMetricsBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "department_id": 1,
                "metrics_id": 2,
                "value": 10,
                "year": 2025,
                "quarter": 1,
                "period_date": "2024-03-31",
                "author_id": 1,
                "status": 1
            }
        }

# Endpoints
@router.get("/departments-metrics", response_model=List[DepartmentsMetricsResponse])
async def get_departments_metrics(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    metrics_id: Optional[int] = Query(None, description="Filter by metrics ID"),
    year: Optional[int] = Query(None, description="Filter by year"),
    quarter: Optional[int] = Query(None, ge=1, le=4, description="Filter by quarter (1-4)"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get list of department metrics with optional filtering.
    """
    query = select(DepartmentsMetrics)
    
    if department_id:
        query = query.where(DepartmentsMetrics.department_id == department_id)
    if metrics_id:
        query = query.where(DepartmentsMetrics.metrics_id == metrics_id)
    if year:
        query = query.where(DepartmentsMetrics.year == year)
    if quarter:
        query = query.where(DepartmentsMetrics.quarter == quarter)
    
    result = await session.execute(
        query.offset(skip).limit(limit)
    )
    metrics = result.scalars().all()
    return metrics

@router.get("/departments-metrics/{record_id}", response_model=DepartmentsMetricsResponse)
async def get_department_metric(
    record_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get department metric by ID.
    """
    result = await session.execute(
        select(DepartmentsMetrics).where(DepartmentsMetrics.id == record_id)
    )
    metric = result.scalar_one_or_none()
    
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department metric with ID {record_id} not found."
        )
    
    return metric

@router.post("/departments-metrics", response_model=DepartmentsMetricsResponse, status_code=status.HTTP_201_CREATED)
async def create_department_metric(
    metric: DepartmentsMetricsCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new department metric record.
    """
    db_metric = DepartmentsMetrics(**metric.dict())
    
    # Generate new ID
    result = await session.execute(
        select(DepartmentsMetrics).order_by(desc(DepartmentsMetrics.id)).limit(1)
    )
    last_record = result.scalar_one_or_none()
    db_metric.id = (last_record.id + 1) if last_record else 1
    
    session.add(db_metric)
    await session.commit()
    await session.refresh(db_metric)
    return db_metric

@router.put("/departments-metrics/{record_id}", response_model=DepartmentsMetricsResponse)
async def update_department_metric(
    record_id: int,
    metric: DepartmentsMetricsCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update department metric by ID.
    """
    result = await session.execute(
        select(DepartmentsMetrics).where(DepartmentsMetrics.id == record_id)
    )
    db_metric = result.scalar_one_or_none()
    
    if not db_metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department metric with ID {record_id} not found."
        )
    
    for key, value in metric.dict().items():
        setattr(db_metric, key, value)
    
    session.add(db_metric)
    await session.commit()
    await session.refresh(db_metric)
    return db_metric

@router.delete("/departments-metrics/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department_metric(
    record_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete department metric by ID.
    """
    result = await session.execute(
        select(DepartmentsMetrics).where(DepartmentsMetrics.id == record_id)
    )
    metric = result.scalar_one_or_none()
    
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department metric with ID {record_id} not found."
        )
    
    await session.delete(metric)
    await session.commit()
    return None