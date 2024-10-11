from typing import Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import Settings
from api.core.protocols import UnitOfWork
from api.infrastructure.email import EmailSenderImpl
from api.infrastructure.storage import UnitOfWorkImpl
from api.infrastructure.storage.repositories import BaseRepository
from api.presentation.api.di.stubs import (
    provide_settings_stub,
    provide_sqlalchemy_session_stub,
)


def get_repository(
    repository_type: Type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repository(
        session: AsyncSession = Depends(provide_sqlalchemy_session_stub),
    ) -> BaseRepository:
        return repository_type(session)

    return _get_repository


def provide_uow(
    session: AsyncSession = Depends(provide_sqlalchemy_session_stub),
) -> UnitOfWork:
    return UnitOfWorkImpl(session)


def provide_email_sender(
    settings: Settings = Depends(provide_settings_stub),
):
    return EmailSenderImpl(settings)
