from api.presentation.api.v1.table_maker_3.excelScript import TableMaker3
from api.presentation.api.v1.table_maker_3.database import Database
from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.responses import FileResponse
router = APIRouter()

@router.get(
    path= "/metrics", 
    status_code=status.HTTP_200_OK,
    )
async def table_maker_3():
    TableMaker3.make_excel()
    return FileResponse("api/infrastructure/excel/table_maker_3.xlsx")