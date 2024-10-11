import logging
from collections import defaultdict

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from api.config.settings import Settings
from api.presentation.api.di.di import setup_di
from api.presentation.api.middlewares import setup_middleware
from api.presentation.api.routes import router
from api.presentation.api.v1.dto import HTTPException

from .open_api import set_custom_openapi

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        root_path=settings.site_api_path,
        docs_url=settings.docs_url,
    )

    app.include_router(router)
    setup_di(app, settings)
    set_custom_openapi(app, settings)
    setup_middleware(app, settings)
    logger.info("Start project")
    return app


app = create_app()


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]

        field_string = (
            loc[1] if loc[0] in ("body", "query", "path") else loc[0]
        )
        if not field_string:
            reformatted_message = "error"
            break
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request",
            errors=reformatted_message,
        ).model_dump(),
    )
