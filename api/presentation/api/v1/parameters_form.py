from fastapi import APIRouter, Depends, Response, Cookie, Request
from sqlalchemy import select, insert, delete, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import (Employee, Role, FacultyAndInstitute,
                                                                      MetricsInQuartal,
                                                                      ActualWorkingDaysOnEmployee,
                                                                      ActualWorkingDays, EmployeesToMetrics,
                                                                      Department, MetricDescription)


from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

from api.infrastructure.storage.sqlalchemy.models.schemas import *
from api.presentation.api.v1.dto.department import DepartmentResponse

router = APIRouter(
)

@router.get(
    path="/departments",
    status_code=status.HTTP_200_OK,
    response_model=list[DepartmentResponse],  # Указываем модель ответа
)
async def get_department (sessions: AsyncSession = Depends(get_async_session)):
    query = select(Department)
    result = await sessions.execute(query)
    list_departments = result.scalars().all()

    # Если данные отсутствуют
    if not list_departments:
        return []

    # Преобразуем результаты SQLAlchemy в Pydantic-модели
    departments_response = [
        DepartmentResponse.model_validate(department)  # Преобразование ORM -> Pydantic
        for department in list_departments
    ]

    return departments_response

@router.get(
    path= "/employees",
    status_code=status.HTTP_200_OK,
)
async def get_employees (quarter: int, id_choise_depart: int, year: int, sessions: AsyncSession = Depends(get_async_session)):

    query = select(MetricsInQuartal).where(MetricsInQuartal.quartal == quarter)
    result = await sessions.execute(query)
    list_metrics = result.scalars().all()

    if list_metrics == None:
        return {"status": "Empty metrics"}

    metrics_id = list_metrics[0].metrics_id
    durations = list_metrics[0].duration

    max_duration = max(durations)

    last_year = year - 1

    min_quarter_last_year = 0
    max_quarter_last_year = 0

    min_quarter_this_year = 0
    max_quarter_this_year = quarter - 1

    if max_quarter_this_year == 0 :
        max_quarter_last_year = 4
        min_quarter_last_year = max(1, max_quarter_last_year - max_duration)

    else:
        min_quarter_this_year = max(1, max_quarter_this_year - max_duration)

        if max_quarter_this_year - max_duration < 0:
            max_quarter_last_year = 4
            min_quarter_last_year = max(1, max_quarter_last_year - max_duration)

    query = select(ActualWorkingDaysOnEmployee.employee_id).where(
        ActualWorkingDaysOnEmployee.department_id == id_choise_depart
    ).where(
        or_(and_(ActualWorkingDaysOnEmployee.quarter <= max_quarter_this_year,
                 ActualWorkingDaysOnEmployee.quarter >= min_quarter_this_year,
                 ActualWorkingDaysOnEmployee.year == year),
            and_(ActualWorkingDaysOnEmployee.quarter <= max_quarter_last_year,
                 ActualWorkingDaysOnEmployee.quarter >= min_quarter_last_year,
                 ActualWorkingDaysOnEmployee.year == last_year))
    ).distinct()

    result = await sessions.execute(query)
    list_employees = result.all()

    if list_employees == None:
        return {"status": "Empty employees"}

    list_id_employees = []

    for emp in list_employees:
        list_id_employees.append(emp[0])

    query = select(Employee)
    result = await sessions.execute(query)
    list_employees = result.all()

    if list_employees == None:
        return {"status": "Empty employees"}

    return_employees = dict()

    for emp in list_employees:
        if emp[0] in list_id_employees:
            fio = emp[2] + " " + emp[1] + " " + emp[3]
            return_employees[emp[0]] = fio

    return {"status": "OK",
            "data": return_employees}

@router.get(
    path= "/metrics",
    status_code=status.HTTP_200_OK,
)
async def get_metrics (quarter: int, sessions: AsyncSession = Depends(get_async_session)):

    query = select(MetricsInQuartal).where(MetricsInQuartal.quartal == quarter)
    result = await sessions.execute(query)
    list_metrics = result.scalars().all()
    if list_metrics == None:
        return {"status": "Empty metrics"}

    metrics_id = list_metrics[0].metrics_id
    durations = list_metrics[0].duration

    query = select(MetricDescription).where(MetricDescription.is_active == True)
    result = await sessions.execute(query)
    list_metrics = result.scalars().all()

    metrics = dict()

    for metric in list_metrics:
        buf = str(metric.metric_subnumber)
        if buf == "None":
            buf = ""
        metrics[metric.metric_id] = str(metric.metric_number) + buf

    data_metrics = list()

    for i in range(len(metrics_id)):
        metric = {
            "id" : metrics_id[i],
            "duration": durations[i],
            "name_metric": metrics[metrics_id[i]]
        }
        data_metrics.append(metric)


    return {"status": "OK",
            "data": data_metrics}

@router.post(
    path= "/metrics",
    status_code=status.HTTP_200_OK,
)
async def post_metrics (post_metrics: PostMetrics, sessions: AsyncSession = Depends(get_async_session)):

    query = select(EmployeesToMetrics.id)
    result = await sessions.execute(query)
    list_res = result.all()

    id = max(res[0] for res in list_res) + 1 if list_res else 0

    data = {
        "id": id,
        "metrics_id": post_metrics.metrics,
        "year": post_metrics.year,
        "quarter": post_metrics.quarter,
        "employee_id": post_metrics.employee_id
    }
    stmt = insert(EmployeesToMetrics).values(**data)
    await sessions.execute(stmt)
    await sessions.commit()


    return {"status": "OK",
            }