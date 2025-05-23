from fastapi import HTTPException, Depends, APIRouter, status
from pydantic import BaseModel
from typing import List, Dict, Tuple

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.infrastructure.storage.sqlalchemy.models.asos_models import (
    DepartmentsMetrics,
    ActualWorkingDaysOnEmployee,
)
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

# Pydantic schemas
class MetricScore(BaseModel):
    metrics_id: int
    score: int

    class Config:
        orm_mode = True

class EmployeesMetricsBase(BaseModel):
    employee_id: int
    year: int
    quarter: int
    metrics: List[MetricScore]

class EmployeesMetricsResponse(EmployeesMetricsBase):
    class Config:
        orm_mode = True

router = APIRouter()

@router.get(
    "/employees_metrics/",
    response_model=List[EmployeesMetricsResponse],
    status_code=status.HTTP_200_OK
)
async def read_employees_metrics(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve, paginated, for each (employee, year, quarter) the list of metric‐score pairs
    based on ActualWorkingDaysOnEmployee → DepartmentsMetrics join.
    """
    stmt = (
        select(
            ActualWorkingDaysOnEmployee.employee_id,
            ActualWorkingDaysOnEmployee.year,
            ActualWorkingDaysOnEmployee.quarter,
            DepartmentsMetrics.metrics_id,
            DepartmentsMetrics.value
        )
        .join(
            DepartmentsMetrics,
            and_(
                DepartmentsMetrics.department_id == ActualWorkingDaysOnEmployee.department_id,
                DepartmentsMetrics.year == ActualWorkingDaysOnEmployee.year,
                DepartmentsMetrics.quarter == ActualWorkingDaysOnEmployee.quarter
            )
        )
        .offset(0)  # fetch all rows, grouping comes next
    )
    result = await session.execute(stmt)
    rows = result.all()

    # Group by (employee_id, year, quarter)
    grouped: Dict[Tuple[int,int,int], List[MetricScore]] = {}
    for emp_id, yr, qt, m_id, score in rows:
        key = (emp_id, yr, qt)
        grouped.setdefault(key, []).append(MetricScore(metrics_id=m_id, score=score))

    # paginate the groups
    items = list(grouped.items())[skip: skip + limit]

    return [
        EmployeesMetricsResponse(
            employee_id=emp, year=yr, quarter=qt, metrics=ms_list
        )
        for (emp, yr, qt), ms_list in items
    ]


@router.get(
    "/employees_metrics/all",
    response_model=List[EmployeesMetricsResponse],
    status_code=status.HTTP_200_OK
)
async def read_all_employees_metrics(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve for each (employee, year, quarter) the full list of metric‐score pairs.
    """
    stmt = (
        select(
            ActualWorkingDaysOnEmployee.employee_id,
            ActualWorkingDaysOnEmployee.year,
            ActualWorkingDaysOnEmployee.quarter,
            DepartmentsMetrics.metrics_id,
            DepartmentsMetrics.value
        )
        .join(
            DepartmentsMetrics,
            and_(
                DepartmentsMetrics.department_id == ActualWorkingDaysOnEmployee.department_id,
                DepartmentsMetrics.year == ActualWorkingDaysOnEmployee.year,
                DepartmentsMetrics.quarter == ActualWorkingDaysOnEmployee.quarter
            )
        )
    )
    result = await session.execute(stmt)
    rows = result.all()

    grouped: Dict[Tuple[int,int,int], List[MetricScore]] = {}
    for emp_id, yr, qt, m_id, score in rows:
        key = (emp_id, yr, qt)
        grouped.setdefault(key, []).append(MetricScore(metrics_id=m_id, score=score))

    return [
        EmployeesMetricsResponse(
            employee_id=emp, year=yr, quarter=qt, metrics=ms_list
        )
        for (emp, yr, qt), ms_list in grouped.items()
    ]


@router.get(
    "/employees_metrics/{employee_id}",
    response_model=List[EmployeesMetricsResponse],
    status_code=status.HTTP_200_OK
)
async def read_employee_metrics(
    employee_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve all (year, quarter) metric‐score lists for a specific employee.
    """
    stmt = (
        select(
            ActualWorkingDaysOnEmployee.employee_id,
            ActualWorkingDaysOnEmployee.year,
            ActualWorkingDaysOnEmployee.quarter,
            DepartmentsMetrics.metrics_id,
            DepartmentsMetrics.value
        )
        .where(ActualWorkingDaysOnEmployee.employee_id == employee_id)
        .join(
            DepartmentsMetrics,
            and_(
                DepartmentsMetrics.department_id == ActualWorkingDaysOnEmployee.department_id,
                DepartmentsMetrics.year == ActualWorkingDaysOnEmployee.year,
                DepartmentsMetrics.quarter == ActualWorkingDaysOnEmployee.quarter
            )
        )
    )
    result = await session.execute(stmt)
    rows = result.all()

    if not rows:
        raise HTTPException(status_code=404, detail="Employee metrics not found")

    grouped: Dict[Tuple[int,int,int], List[MetricScore]] = {}
    for emp_id, yr, qt, m_id, score in rows:
        key = (emp_id, yr, qt)
        grouped.setdefault(key, []).append(MetricScore(metrics_id=m_id, score=score))

    return [
        EmployeesMetricsResponse(
            employee_id=emp, year=yr, quarter=qt, metrics=ms_list
        )
        for (emp, yr, qt), ms_list in grouped.items()
    ]
