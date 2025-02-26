from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import MetricDescription, Section
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session
from api.presentation.api.v1.table_maker_3.excelScript import TableMaker3
from fastapi import APIRouter, Body, Response, Depends
from fastapi.responses import FileResponse
router = APIRouter()

@router.get(
    path= "/metrics",
    status_code=status.HTTP_200_OK,
    )
async def table_maker_3(sessions: AsyncSession = Depends(get_async_session)):
    query = select(MetricDescription).order_by(MetricDescription.metric_number, MetricDescription.metric_subnumber)
    result = await sessions.execute(query)
    metrics = result.scalars().all()

    query = select(Section)
    result = await sessions.execute(query)
    sections = result.scalars().all()
    TableMaker3.make_excel(metrics, sections)
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}
    return FileResponse("api/infrastructure/excel/table_maker_3.xlsx", filename="table_maker_3.xlsx", headers=headers)
