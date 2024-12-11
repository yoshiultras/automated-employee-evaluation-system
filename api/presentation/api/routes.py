from fastapi import APIRouter

from api.config import Settings
from api.presentation.api.v1 import user, table_maker

settings = Settings()

router = APIRouter()
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(table_maker.router, prefix="/table_maker", tags=["table_maker"])
