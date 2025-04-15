from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import Department, DepartmentsMetrics, Employee, MetricDescription
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from fastapi import APIRouter, Body, Response, Depends, Query
from fastapi.responses import FileResponse
from passlib.context import CryptContext


router = APIRouter()

@router.get(
    path="/table",
    status_code=status.HTTP_200_OK,
)
async def get_kpi_table(
    year: int | None = None, 
    quarter: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # Основной запрос с JOIN всех таблиц
        query = select(
            DepartmentsMetrics.value.label("score"),
            DepartmentsMetrics.year,
            DepartmentsMetrics.quarter,
            Department,  # Полный объект отдела
            MetricDescription  # Полный объект метрики
        ).select_from(DepartmentsMetrics)\
         .join(
            MetricDescription,
            DepartmentsMetrics.metrics_id == MetricDescription.metric_id
         ).join(
            Department,
            DepartmentsMetrics.department_id == Department.id
         )
        
        # Фильтрация по году и кварталу
        if year is not None:
            query = query.where(DepartmentsMetrics.year == year)
        if quarter is not None:
            query = query.where(DepartmentsMetrics.quarter == quarter)
        
        result = await session.execute(query)
        
        # Формируем ответ с вложенными структурами
        response_data = []
        for row in result:
            department_data = {
                'id': row.Department.id,
                'name': row.Department.name_of_department,
                'affiliation': row.Department.affiliation,
                'faculty_id': row.Department.id_facultet
            }
            
            metric_data = {
                'id': row.MetricDescription.metric_id,
                'number': row.MetricDescription.metric_number,
                'subnumber': row.MetricDescription.metric_subnumber,
                'description': row.MetricDescription.description,
                'points': row.MetricDescription.points
            }
            
            response_data.append({
                'score': row.score,
                'year': row.year,
                'quarter': row.quarter,
                'department': row.Department,  # Полные данные об отделе
                'metric': row.MetricDescription  # Полные данные о метрике
            })
        
        return {
            "status": "OK",
            "year": year,
            "quater": quarter,
            "data": response_data
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }