from fastapi import Request, Response, APIRouter, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(

)

templates = Jinja2Templates(directory="api/config/jinja_templates")

@router.get("/table_maker")
def get_table_maker_page (request: Request):
    return templates.TemplateResponse("table_maker/document_table.html", {"request": request})

@router.get("/parameter")
def get_parameters_form (request: Request):
    return templates.TemplateResponse("parameters_form/parameters_from.html", {"request": request})

@router.get("/summary_table")
def get_summary_table (request: Request):
    return templates.TemplateResponse("summary_table/summary_table.html", {"request": request})
