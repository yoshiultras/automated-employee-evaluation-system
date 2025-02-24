import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import Settings
from api.presentation.api.v1.dto import HTTPException

logger = logging.getLogger(__name__)
origins = []


async def error_header(
    request: Request,
    call_next,
):
    err_content = None
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        err_content = "error"
    if err_content is not None:
        err = JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request",
                errors=err_content,
            ).model_dump(),
        )
        return err
    return response


def setup_middleware(app: FastAPI, settings: Settings):
    app.add_middleware(BaseHTTPMiddleware, dispatch=error_header)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins + ["http://" + settings.client_domain],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
