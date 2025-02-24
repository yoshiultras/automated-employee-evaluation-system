from fastapi import APIRouter, Depends, Response, Cookie, Request
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import (employees, roles, faculties_and_institutes,
                                                                      Department, MetricDescription, Section,
                                                                      metrics_in_quartal,
                                                                      actual_working_days_on_employee,
                                                                      actual_working_days, employees_to_metrics)

from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

from api.infrastructure.storage.sqlalchemy.models.schemas import *

router = APIRouter(
)

@router.get(
    path= "/metrics",
    status_code=status.HTTP_200_OK,
)
async def get_metrics (get_for_metrics: GetForMetrics, sessions: AsyncSession = Depends(get_async_session)):

    query = select(metrics_in_quartal).where(metrics_in_quartal.c.quartal == get_for_metrics.quarter)
    result = await sessions.execute(query)
    list_metrics = result.one_or_none()

    if list_metrics == None:
        return {"status": "Empty metrics"}

    metrics_id = list_metrics[3]
    durations = list_metrics[2]

    query = select(employees_to_metrics.c.value).where(employees_to_metrics.c.quarter == get_for_metrics.quarter
                                                       ).where(
                                                    employees_to_metrics.c.year == get_for_metrics.year
                                                    ).where(
                                                    employees_to_metrics.c.employee_id == get_for_metrics.employee_id
                                                    )
    result = await sessions.execute(query)
    row_metrics_value = result.one_or_none()
    list_metrics_value = list()

    if row_metrics_value == None:
        list_metrics_value = [0] * len(durations)
    else:
        list_metrics_value = row_metrics_value[0]

    query = select(MetricDescription)
    result = await sessions.execute(query)
    list_metrics = result.all()

    metrics = list()

    for metric in list_metrics:
        if metric[0] in metrics_id:
            buf = str(metric[2])
            if buf == "None":
                buf = ""
            metrics.append(str(metric[1]) + buf)

    query = select(actual_working_days).where(actual_working_days.c.year == get_for_metrics.year).order_by(actual_working_days.c.month)
    result = await sessions.execute(query)
    request_actual_work = result.all()

    if request_actual_work == None:
        return {"status": "Empty work day"}

    result_actual_work_this_year = {1: list(),
                           2: list(),
                           3: list(),
                           4: list()}

    for row in request_actual_work:

        result_actual_work_this_year[row[4]].append(row[3])
#=======================================================================================================================
    last_year = get_for_metrics.year - 1
    query = select(actual_working_days).where(actual_working_days.c.year == last_year).order_by(
        actual_working_days.c.month)
    result = await sessions.execute(query)
    request_actual_work = result.all()

    if request_actual_work == None:
        return {"status": "Empty work day"}

    result_actual_work_last_year = {1: list(),
                                     2: list(),
                                     3: list(),
                                     4: list()}

    for row in request_actual_work:
        result_actual_work_last_year[row[4]].append(row[3])

    result_actual_work = {last_year: result_actual_work_last_year,
                           get_for_metrics.year: result_actual_work_this_year}

#=======================================================================================================================
    query = select(actual_working_days_on_employee).where(
        actual_working_days_on_employee.c.year == get_for_metrics.year
                                                          ).where(
        actual_working_days_on_employee.c.department_id == get_for_metrics.department_id
                                                                  ).where(
        actual_working_days_on_employee.c.employee_id == get_for_metrics.employee_id
    ).order_by(
        actual_working_days_on_employee.c.month)
    result = await sessions.execute(query)
    request_actual_work_employee_this_year = result.all()

    result_actual_work_employee_this_year = {1: list(),
                                    2: list(),
                                    3: list(),
                                    4: list()}

    for row in request_actual_work_employee_this_year:
        buf = {
            "days": row[5],
            "jobtitle": row[2]
        }
        result_actual_work_employee_this_year[row[6]].append(buf)
#=======================================================================================================================

    query = select(actual_working_days_on_employee).where(
        actual_working_days_on_employee.c.year == last_year
    ).where(
        actual_working_days_on_employee.c.department_id == get_for_metrics.department_id
    ).where(
        actual_working_days_on_employee.c.employee_id == get_for_metrics.employee_id
    ).order_by(
        actual_working_days_on_employee.c.month)
    result = await sessions.execute(query)
    request_actual_work_employee_last_year = result.all()

    result_actual_work_employee_last_year = {1: list(),
                                             2: list(),
                                             3: list(),
                                             4: list()}

    for row in request_actual_work_employee_last_year:
        buf = {
            "days": row[5],
            "jobtitle": row[2]
        }
        result_actual_work_employee_last_year[row[6]].append(buf)

    result_actual_work_employee = {last_year: result_actual_work_employee_last_year,
                          get_for_metrics.year: result_actual_work_employee_this_year}
#=======================================================================================================================

    response_actual_work = list()
    response_actual_work_employee = list()
    response_koff = list()

    for i in range(len(durations)):

        actual_quarter = get_for_metrics.quarter - 1
        actual_year = get_for_metrics.year

        employee_work = 0.0
        employeee_day = 0
        work_day = 0

        for j in range(durations[i]):

            if actual_quarter < 1:
                actual_quarter = 4
                actual_year -= 1

            work_day += sum(result_actual_work[actual_year][actual_quarter])

            if len(result_actual_work_employee[actual_year][actual_quarter]) == 0:
                actual_quarter -= 1
                continue

            quartes_employee = result_actual_work_employee[actual_year][actual_quarter]

            for quarter_employee in quartes_employee:
                korr = 1
                if quarter_employee["jobtitle"] == "ИО" or quarter_employee["jobtitle"] == "ВРИО":
                    korr = 0.5
                employee_work += (quarter_employee["days"] * korr)
                employeee_day += quarter_employee["days"]

            actual_quarter -= 1

        koff = round(employee_work / work_day, 2)

        response_actual_work.append(work_day)
        response_actual_work_employee.append(employeee_day)
        response_koff.append(koff)

    list_metrics_value_buf_koff = list()
    for i in range(len(list_metrics_value)):
        list_metrics_value_buf_koff.append(round(list_metrics_value[i] * response_koff[i],2))

    response_data = {
        "duration": durations,
        "metrics": metrics,
        "work_day": response_actual_work,
        "employee_day": response_actual_work_employee,
        "koff": response_koff,
        "metrics_value": list_metrics_value,
        "metrics_value_koff": list_metrics_value_buf_koff,
    }

    return {"status": "OK",
            "data": response_data}
