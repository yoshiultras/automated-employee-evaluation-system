from fastapi import APIRouter

from api.config import Settings
from api.presentation.api.v1 import table_maker, parameters_form, summary_table, templates_router, auth

settings = Settings()

router = APIRouter()
router.include_router(table_maker.router, prefix="/table_maker", tags=["table_maker"])
router.include_router(parameters_form.router, prefix="/parameters_form", tags=["parameters_form"])
router.include_router(summary_table.router, prefix="/summary_table", tags=["summary_table"])
router.include_router(templates_router.router, prefix="/page", tags=["page"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])