from http.client import HTTPException
from sqlalchemy import select, any_, func, literal_column, true, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import Department, DepartmentsMetrics, Employee, \
    MetricDescription, EmployeesToMetrics
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from fastapi import APIRouter, Body, Response, Depends, Query
from fastapi.responses import FileResponse
from passlib.context import CryptContext
from datetime import date
from sqlalchemy import select


router = APIRouter()

@router.get(
    path="/table",
    status_code=status.HTTP_200_OK,
)
async def get_kpi_table(
    employee_id: int,
    year: int | None = None, 
    quarter: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    unnested = aliased(
        select(
            EmployeesToMetrics.employee_id.label("employee_id"),
            EmployeesToMetrics.year,
            EmployeesToMetrics.quarter,
            func.unnest(EmployeesToMetrics.metrics_id).label("metric_id")
        )
            .where(EmployeesToMetrics.employee_id == employee_id)
            .alias("unnested_metrics")
    )

    # Шаг 2 — LEFT JOIN с departments_metrics по metric_id и author_id
    query = select(
        MetricDescription,
        DepartmentsMetrics.value.label("score"),
        DepartmentsMetrics.year.label("dm_year"),
        DepartmentsMetrics.quarter.label("dm_quarter"),
        Department
    ).select_from(unnested) \
        .join(
        MetricDescription,
        MetricDescription.metric_id == unnested.c.metric_id
    ) \
        .outerjoin(
        DepartmentsMetrics,
        and_(
            DepartmentsMetrics.metrics_id == unnested.c.metric_id,
            DepartmentsMetrics.author_id == unnested.c.employee_id
        )
    ) \
        .outerjoin(
        Department,
        DepartmentsMetrics.department_id == Department.id
    )

    # Дополнительная фильтрация по году и кварталу
    if year is not None:
        query = query.where(DepartmentsMetrics.year == year)
    if quarter is not None:
        query = query.where(DepartmentsMetrics.quarter == quarter)

    result = await session.execute(query)

    # Формируем полный ответ
    response_data = []
    for row in result:
        department_data = {
            'id': row.Department.id if row.Department is not None else 0,
            'name': row.Department.id if row.Department is not None else 0,
            'affiliation': row.Department.id if row.Department is not None else 0,
            'faculty_id': row.Department.id if row.Department is not None else 0,
        }

        metric_data = {
            'id': row.MetricDescription.metric_id,
            'number': row.MetricDescription.metric_number,
            'subnumber': row.MetricDescription.metric_subnumber,
            'description': row.MetricDescription.description,
            'points': row.MetricDescription.points
        }


        response_data.append({
            'department': department_data,
            'metric': metric_data,
            'score': row.score
        })

    return {
        "status": "OK",
        "year": year,
        "quarter": quarter,
        "data": response_data
    }
    

@router.post(
    path="/table",
    status_code=status.HTTP_200_OK,
)
async def create_department_metric(
    data: dict,  # Принимаем весь объект данных
    year: int,
    quarter: int,
    employee_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # 1. Извлечение данных из входного объекта
        department_data = data.get("department", {})
        metric_data = data.get("metric", {})
        score = data.get("score")
        
        # 2. Валидация обязательных полей
        if not department_data or not metric_data or score is None:
            raise HTTPException(status_code=400, detail="Missing required fields in data")
        
        if not isinstance(score, (int, float)):
            raise HTTPException(status_code=400, detail="Score must be a number")
        
        # 3. Проверка существования сущностей в БД
        department = await session.get(Department, department_data.get("id"))
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {department_data.get('id')} not found")
        
        metric = await session.get(MetricDescription, metric_data.get("id"))
        if not metric:
            raise HTTPException(status_code=404, detail=f"Metric with id {metric_data.get('id')} not found")
        
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
        
        # 4. Создание новой записи
        new_metric = DepartmentsMetrics(
            department_id=department_data["id"],
            metrics_id=metric_data["id"],
            value=score,
            year=year,
            quarter=quarter,
            period_date=date.today(),
            author_id=employee_id,
            status=1  # Статус "активно"
        )
        
        session.add(new_metric)
        await session.commit()
        await session.refresh(new_metric)
        
        # 5. Формирование ответа
        return {
            "status": "success",
            "data": {
                "id": new_metric.id,
                "department_id": new_metric.department_id,
                "metric_id": new_metric.metrics_id,
                "value": new_metric.value,
                "year": new_metric.year,
                "quarter": new_metric.quarter,
                "created_at": new_metric.period_date.isoformat()
            }
        }
        
    except HTTPException:
        raise  # Пробрасываем уже обработанные ошибки
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")