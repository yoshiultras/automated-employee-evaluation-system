from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from api.infrastructure.storage.sqlalchemy.models.asos_models import (
    MetricsInQuartal,
    ActualWorkingDays,
    ActualWorkingDaysOnEmployee,
    EmployeesToMetrics,
    MetricDescription
)
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

router = APIRouter()


async def get_metrics_in_quarter(
        session: AsyncSession,
        quarter: int
) -> MetricsInQuartal:
    """Get metrics configuration for specified quarter and year"""
    result = await session.execute(
        select(MetricsInQuartal).where(
            and_(
                MetricsInQuartal.quartal == quarter
            )
        )
    )
    return result.scalar_one_or_none()


async def get_employee_metrics_values(
        session: AsyncSession,
        employee_id: int,
        quarter: int,
        year: int
) -> List[int]:
    """Get employee's metrics values for specified quarter"""
    result = await session.execute(
        select(EmployeesToMetrics.value).where(
            and_(
                EmployeesToMetrics.employee_id == employee_id,
                EmployeesToMetrics.quarter == quarter,
                EmployeesToMetrics.year == year
            )
        )
    )
    row = result.scalar_one_or_none()
    return row if row else [0]


async def get_work_days_data(
        session: AsyncSession,
        year: int
) -> Dict[int, List[int]]:
    """Get actual working days data for year by quarters"""
    result = await session.execute(
        select(ActualWorkingDays).where(
            ActualWorkingDays.year == year
        ).order_by(ActualWorkingDays.month)
    )
    quarters_data = {1: [], 2: [], 3: [], 4: []}
    for record in result.scalars():
        quarters_data[record.quarter].append(record.count_day)
    return quarters_data


async def get_employee_work_days(
        session: AsyncSession,
        employee_id: int,
        department_id: int,
        year: int
) -> Dict[int, List[Dict]]:
    """Get employee's working days data by quarters"""
    result = await session.execute(
        select(ActualWorkingDaysOnEmployee).where(
            and_(
                ActualWorkingDaysOnEmployee.employee_id == employee_id,
                ActualWorkingDaysOnEmployee.department_id == department_id,
                ActualWorkingDaysOnEmployee.year == year
            )
        ).order_by(ActualWorkingDaysOnEmployee.month)
    )
    quarters_data = {1: [], 2: [], 3: [], 4: []}
    for record in result.scalars():
        quarters_data[record.quarter].append({
            "days": record.count_day,
            "jobtitle": record.jobtitle
        })
    return quarters_data


async def calculate_work_coefficients(
        durations: List[int],
        work_days: Dict[int, Dict[int, List[int]]],
        employee_days: Dict[int, Dict[int, List[Dict]]],
        target_year: int,
        target_quarter: int
) -> tuple:
    """Calculate work coefficients for metrics"""
    coefficients = []
    total_work_days = []
    employee_total_days = []

    for duration in durations:
        # Определяем год и квартал для расчета
        quarter = target_quarter
        year = target_year

        # Если duration выходит за пределы текущего года, корректируем год и квартал
        if duration > 4:
            year -= 1
            quarter = 4 - (duration - 4)

        # Проверяем, есть ли данные для этого года и квартала
        if year not in work_days or quarter not in work_days[year]:
            coefficients.append(0)
            total_work_days.append(0)
            employee_total_days.append(0)
            continue

        # Суммируем рабочие дни
        work_days_sum = sum(work_days[year][quarter])

        # Суммируем дни сотрудника с учетом коэффициента для должности
        employee_days_sum = 0
        for day_data in employee_days.get(year, {}).get(quarter, []):
            korr = 0.5 if day_data["jobtitle"] in ["ИО", "ВРИО"] else 1
            employee_days_sum += day_data["days"] * korr

        # Рассчитываем коэффициент
        coefficient = round(employee_days_sum / work_days_sum, 2) if work_days_sum else 0

        coefficients.append(coefficient)
        total_work_days.append(work_days_sum)
        employee_total_days.append(employee_days_sum)

    return total_work_days, employee_total_days, coefficients


@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_metrics_summary(
        quarter: int = Query(..., description="Квартал"),
        year: int = Query(..., description="Год"),
        employee_id: int = Query(..., description="ID сотрудника"),
        department_id: int = Query(..., description="ID отдела"),
        session: AsyncSession = Depends(get_async_session),
):

    # Получаем базовые данные
    metrics_config = await get_metrics_in_quarter(session, quarter)
    if not metrics_config:
        return {"status": "Empty metrics configuration"}

    # Получаем значения метрик сотрудника
    metrics_values = await get_employee_metrics_values(
        session, employee_id, quarter, year
    )

    # Получаем данные по рабочим дням
    current_year_work_days = await get_work_days_data(session, year)
    last_year_work_days = await get_work_days_data(session, year - 1)

    # Получаем данные сотрудника
    current_year_employee_days = await get_employee_work_days(
        session, employee_id, department_id, year
    )
    last_year_employee_days = await get_employee_work_days(
        session, employee_id, department_id, year - 1
    )

    # Рассчитываем коэффициенты
    work_days, employee_days, coefficients = await calculate_work_coefficients(
        metrics_config.duration,
        {year: current_year_work_days, year - 1: last_year_work_days},
        {year: current_year_employee_days, year - 1: last_year_employee_days},
        year,  # Передаем целевой год
        quarter  # Передаем целевой квартал
    )

    # Формируем список метрик
    result = await session.execute(select(MetricDescription).where(MetricDescription.is_active == True))
    metrics = [
        f"{m.metric_number}{m.metric_subnumber or ''}"
        for m in result.scalars()
        if m.metric_id in metrics_config.metrics_id
    ]

    # Рассчитываем значения с коэффициентами
    adjusted_values = [
        round(value * coeff, 2)
        for value, coeff in zip(metrics_values, coefficients)
    ]

    return {
        "status": "OK",
        "data": {
            "duration": metrics_config.duration,
            "metrics": metrics,
            "work_day": work_days,
            "employee_day": employee_days,
            "koff": coefficients,
            "metrics_value": metrics_values,
            "metrics_value_koff": adjusted_values,
        }
    }