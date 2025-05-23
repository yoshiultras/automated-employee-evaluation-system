from fastapi import APIRouter

from api.config import Settings
from api.presentation.api.v1 import employees_to_metrics, table_maker, parameters_form, summary_table, templates_router, \
    auth, metrics, faculty_and_department, employees, kpi, auth_polytech, employees_to_department, employees_to_scores

settings = Settings()

router = APIRouter()
router.include_router(table_maker.router, prefix="/table_maker", tags=["table_maker"])
router.include_router(parameters_form.router, prefix="/parameters_form", tags=["parameters_form"])
router.include_router(summary_table.router, prefix="/summary_table", tags=["summary_table"])
router.include_router(templates_router.router, prefix="/page", tags=["page"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
router.include_router(faculty_and_department.router, prefix="/faculty_and_department", tags=["faculty_and_department"])
router.include_router(employees_to_metrics.router, tags=["employees_to_metrics"])
router.include_router(employees.router, tags=["employees"])
router.include_router(employees_to_scores.router, tags=["employees_to_scores"])
router.include_router(kpi.router, prefix="/kpi", tags=["table"])
router.include_router(auth_polytech.router, tags=["auth_polytech"])
router.include_router(employees_to_department.router, tags=["employees_to_department"])