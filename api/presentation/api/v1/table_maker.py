from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import MetricDescription, Section, EmployeesToMetrics, \
    EmployeeResponsibility, Responsibility, Employee, Role
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from api.presentation.api.v1.table_maker_3.expertsTableMaker import ExpertTableMaker
from api.presentation.api.v1.table_maker_3.metricsTableMaker import TableMaker3
from fastapi import APIRouter, Body, Response, Depends
from fastapi.responses import FileResponse
router = APIRouter()

@router.get(
    path= "/metrics",
    status_code=status.HTTP_200_OK,
    )
async def metrics(sessions: AsyncSession = Depends(get_async_session)):
    query = select(MetricDescription).where(MetricDescription.is_active == True).order_by(MetricDescription.metric_number, MetricDescription.metric_subnumber)
    result = await sessions.execute(query)
    metrics = result.scalars().all()

    query = select(Section)
    result = await sessions.execute(query)
    sections = result.scalars().all()
    TableMaker3.make_excel(metrics, sections)
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}
    return FileResponse("api/infrastructure/excel/table_maker_3.xlsx", filename="table_maker_3.xlsx", headers=headers)

@router.get(
    path="/experts",
    status_code=status.HTTP_200_OK,
)
async def experts(session: AsyncSession = Depends(get_async_session)):
    # 1. Загружаем MetricDescription и Section
    metrics_q = select(
        MetricDescription
    ).where(MetricDescription.is_active == True).order_by(
        MetricDescription.metric_number,
        MetricDescription.metric_subnumber
    )
    res_metrics = await session.execute(metrics_q)
    metrics = res_metrics.scalars().all()

    sections_q = select(Section)
    res_sections = await session.execute(sections_q)
    sections = res_sections.scalars().all()

    # 2. Загружаем EmployeesToMetrics, чтобы получить связь metric_id -> employee_id
    etm_q = select(EmployeesToMetrics)
    res_etm = await session.execute(etm_q)
    etm_list = res_etm.scalars().all()

    metric_employee_map = {}
    for etm in etm_list:
        emp_id = etm.employee_id
        for m_id in etm.metrics_id:
            if m_id not in metric_employee_map:
                metric_employee_map[m_id] = emp_id

    # 3. Загружаем всех сотрудников и их роли
    emp_q = select(Employee)
    res_emp = await session.execute(emp_q)
    emp_list = res_emp.scalars().all()

    # Загружаем роли
    role_q = select(Role)
    res_role = await session.execute(role_q)
    role_list = res_role.scalars().all()
    role_map = {r.role_id: r.role for r in role_list}

    emp_name_map = {}
    emp_role_map = {}

    for e in emp_list:
        emp_name_map[e.employee_id] = f"{e.last_name} {e.first_name} {e.surname}"
        emp_role_map[e.employee_id] = role_map.get(e.role_id, "")

    # 4. Вызываем генерацию Excel
    ExpertTableMaker.make_excel(metrics, sections, metric_employee_map, emp_name_map, emp_role_map)

    # 4. Возвращаем созданный файл пользователю
    file_path = "api/infrastructure/excel/experts.xlsx"
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}
    return FileResponse(file_path, filename="experts.xlsx", headers=headers)