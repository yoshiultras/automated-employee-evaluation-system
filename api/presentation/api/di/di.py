from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.settings import Settings
from api.infrastructure.storage.sqlalchemy.factories import (
    build_sa_engine,
    build_sa_session_factory,
)
from api.presentation.api.di.provides import (  # noqa: E501; noqa: E501, F401
    provide_uow,
    provide_user_delete_interactor,
    provide_user_get_by_filters_interactor,
    provide_user_get_by_id_interactor,
    provide_user_login_interactor,
    provide_user_logout_interactor,
)
from api.presentation.api.di.stubs import (  # noqa: E501, F401
    provide_settings_stub,
    provide_sqlalchemy_session_stub,
    provide_uow_stub,
    provide_user_delete_interactor_stub,
    provide_user_get_by_filters_interactor_stub,
    provide_user_get_by_id_interactor_stub,
    provide_user_login_interactor_stub,
    provide_user_logout_interactor_stub,
)


def get_sqlalchemy_session_factory(settings: Settings):
    engine = build_sa_engine(settings)
    session_factory = build_sa_session_factory(engine)

    async def sesstion_generator() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return sesstion_generator


def setup_di(app: FastAPI, settings: Settings):
    sqlalchemy_session_factory = get_sqlalchemy_session_factory(settings)

    app.dependency_overrides.update(
        {
            provide_settings_stub: lambda: settings,
            provide_sqlalchemy_session_stub: sqlalchemy_session_factory,
        }
    )
    shared_dependency = {
        provide_uow_stub: provide_uow,
    }
    app.dependency_overrides.update(shared_dependency)

    user_interactors = {
        provide_user_get_by_id_interactor_stub: provide_user_get_by_id_interactor,
        provide_user_get_by_filters_interactor_stub: provide_user_get_by_filters_interactor,
        provide_user_login_interactor_stub: provide_user_login_interactor,
        provide_user_logout_interactor_stub: provide_user_logout_interactor,
        provide_user_delete_interactor_stub: provide_user_delete_interactor,
    }
    app.dependency_overrides.update(user_interactors)
