from fastapi import Depends

from api.core.interactors import (
    UserDeleteInteractor,
    UserGetByFiltersInteractor,
    UserGetByIdInteractor,
    UserLoginInteractor,
    UserLogoutInteractor,
)
from api.config import Settings
from api.core.protocols import EmailSender, UnitOfWork, UserRepository
from api.core.services import AuthService, UserService
from api.infrastructure.storage.repositories import UserRepositoryImpl
from api.presentation.api.di.provides.shared import get_repository
from api.presentation.api.di.stubs import (
    provide_email_sender_stub,
    provide_uow_stub,
    provide_settings_stub,
)


def provide_auth_service(
    cfg: Settings = Depends(provide_uow_stub),
):
    return AuthService(
        secret_key=cfg.secret_key,
        access_token_min=cfg.access_token_min,
        refresh_token_days=cfg.refresh_token_days,
    )


def provide_user_get_by_id_interactor(
    uow: UnitOfWork = Depends(provide_uow_stub),
    user_repository: UserRepository = Depends(
        get_repository(UserRepositoryImpl)
    ),
) -> UserGetByIdInteractor:
    return UserGetByIdInteractor(
        uow=uow,
        user_repository=user_repository,
    )


def provide_user_get_by_filters_interactor(
    uow: UnitOfWork = Depends(provide_uow_stub),
    user_repository: UserRepository = Depends(
        get_repository(UserRepositoryImpl)
    ),
) -> UserGetByFiltersInteractor:
    return UserGetByFiltersInteractor(
        uow=uow,
        user_repository=user_repository,
    )


def provide_user_login_interactor(
    uow: UnitOfWork = Depends(provide_uow_stub),
    user_repository: UserRepository = Depends(
        get_repository(UserRepositoryImpl)
    ),
    auth_service: AuthService = Depends(provide_auth_service),
    email_sender: EmailSender = Depends(provide_email_sender_stub),
) -> UserLoginInteractor:
    return UserLoginInteractor(
        uow=uow,
        user_repository=user_repository,
        auth_service=auth_service,
        email_sender=email_sender,
    )


def provide_user_logout_interactor(
    uow: UnitOfWork = Depends(provide_uow_stub),
) -> UserLogoutInteractor:
    return UserLogoutInteractor(
        uow=uow,
    )


def provide_user_delete_interactor(
    uow: UnitOfWork = Depends(provide_uow_stub),
    user_repository: UserRepository = Depends(
        get_repository(UserRepositoryImpl)
    ),
) -> UserDeleteInteractor:
    return UserDeleteInteractor(
        uow=uow,
        user_repository=user_repository,
    )
