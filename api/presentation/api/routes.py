from fastapi import APIRouter

from api.config import Settings
from api.presentation.api.v1 import user

settings = Settings()

router = APIRouter()
router.include_router(user.router, prefix="/users", tags=["users"])
