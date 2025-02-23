from fastapi import APIRouter, Depends, Response, Cookie, Request
from sqlalchemy import select, insert, delete, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import (employees, roles, faculties_and_institutes,
                                                                      departments, metric_descriptions, sections,
                                                                      metrics_in_quartal, actual_working_days_on_employee,
                                                                      actual_working_days, employees_to_metrics)

from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

from api.infrastructure.storage.sqlalchemy.models.schemas import *

router = APIRouter(
)

@router.get(
    path= "/departments",
    status_code=status.HTTP_200_OK,
)
async def get_department (sessions: AsyncSession = Depends(get_async_session)):

    query = select(departments)
    result = await sessions.execute(query)
    list_departments = result.all()

    data_departments = dict()

    for depart in list_departments:
        data_departments[depart[0]] = depart[1]

    if list_departments == None:
        return {"status": "Empty department"}

    return {"status": "OK",
            "data": data_departments}

@router.get(
    path= "/employees",
    status_code=status.HTTP_200_OK,
)
async def get_employees (quarter: int, id_choise_depart: int, year: int, sessions: AsyncSession = Depends(get_async_session)):

    query = select(metrics_in_quartal).where(metrics_in_quartal.c.quartal == quarter)
    result = await sessions.execute(query)
    list_metrics = result.one_or_none()

    if list_metrics == None:
        return {"status": "Empty metrics"}

    metrics_id = list_metrics[3]
    durations = list_metrics[2]

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

    query = select(actual_working_days_on_employee.c.employee_id).where(
        actual_working_days_on_employee.c.department_id == id_choise_depart
    ).where(
        or_(and_(actual_working_days_on_employee.c.quarter <= max_quarter_this_year,
                 actual_working_days_on_employee.c.quarter >= min_quarter_this_year,
                 actual_working_days_on_employee.c.year == year),
            and_(actual_working_days_on_employee.c.quarter <= max_quarter_last_year,
                 actual_working_days_on_employee.c.quarter >= min_quarter_last_year,
                 actual_working_days_on_employee.c.year == last_year))
    ).distinct()

    result = await sessions.execute(query)
    list_employees = result.all()

    if list_employees == None:
        return {"status": "Empty employees"}

    list_id_employees = []

    for emp in list_employees:
        list_id_employees.append(emp[0])

    query = select(employees)
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

    query = select(metrics_in_quartal).where(metrics_in_quartal.c.quartal == quarter)
    result = await sessions.execute(query)
    list_metrics = result.one_or_none()

    if list_metrics == None:
        return {"status": "Empty metrics"}

    metrics_id = list_metrics[3]
    durations = list_metrics[2]

    query = select(metric_descriptions)
    result = await sessions.execute(query)
    list_metrics = result.all()

    metrics = dict()

    for metric in list_metrics:
        buf = str(metric[2])
        if buf == "None":
            buf = ""
        metrics[metric[0]] = str(metric[1]) + buf

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

    query = select(employees_to_metrics.c.id)
    result = await sessions.execute(query)
    list_res = result.all()

    list_id = list()

    for res in list_res:
        list_id.append(res[0])

    id = max(list_id) + 1

    data = {
        "id": id,
        "metrics_id": post_metrics.metrics_id,
        "value": post_metrics.value,
        "year": post_metrics.year,
        "quarter": post_metrics.quarter,
        "employee_id": post_metrics.employee_id
    }
    stmt = insert(employees_to_metrics).values(**data)
    await sessions.execute(stmt)
    await sessions.commit()


    return {"status": "OK",
            }