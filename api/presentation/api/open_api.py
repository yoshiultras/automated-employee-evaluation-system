from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api.config.settings import Settings


def set_custom_openapi(app: FastAPI, settings: Settings):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ADMIN API",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    openapi_schema["servers"] = [{"url": settings.site_api_path}]

    app.openapi_schema = openapi_schema
