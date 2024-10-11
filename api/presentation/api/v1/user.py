import datetime
import logging
from dataclasses import asdict

import pytz
from fastapi import APIRouter, Body, Depends, Response, status

from api.config import Settings
from api.core.dto import (
    UserDelete,
    UserGetByFilters,
    UserGetById,
    UserLogin,
    UserLogout,
    UserPaginationParamsDto,
    UserSortFieldName,
)
from api.core.entities import UserId
from api.core.exceptions import (
    UserInvalidEmailException,
    UserInvalidPasswordException,
)
from api.core.interactors import (
    UserDeleteInteractor,
    UserGetByFiltersInteractor,
    UserGetByIdInteractor,
    UserLoginInteractor,
    UserLogoutInteractor,
)
from api.presentation.api.di.stubs import (  # Импорт провайдера
    provide_settings_stub,
    provide_user_delete_interactor_stub,
    provide_user_get_by_filters_interactor_stub,
    provide_user_get_by_id_interactor_stub,
    provide_user_login_interactor_stub,
    provide_user_logout_interactor_stub,
)
from api.presentation.api.v1 import dto as api_dto
from .field_templates import get_pagination_fields_depends

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    path="/{id:int}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": api_dto.UserResponse},
    },
)
async def get_by_id_countapiarty(
    id: UserId,
    interactor: UserGetByIdInteractor = Depends(
        provide_user_get_by_id_interactor_stub
    ),
):
    logger.info(f"Start handle get user by id")
    dto = UserGetById(user_id=id, user=None)
    logger.debug(f"data: {asdict(dto)}")

    user_return = await interactor.execute(dto)

    logger.debug(
        f"response: {asdict(user_return) if user_return is not None else None}"
    )
    return user_return


@router.post(
    path="/filters",
    status_code=status.HTTP_200_OK,
)
async def get_by_filters_order(
    pagination_data: UserPaginationParamsDto = Depends(
        get_pagination_fields_depends(
            UserPaginationParamsDto, UserSortFieldName
        )
    ),
    data: api_dto.UserGetByFilters = Body(),
    interactor: UserGetByFiltersInteractor = Depends(
        provide_user_get_by_filters_interactor_stub
    ),
):
    logger.info(f"Start handle get users by filters")
    dto = UserGetByFilters(
        pagination_data=pagination_data,
        email=data.email,
    )
    logger.debug(f"data: {asdict(dto)}")

    users_return = await interactor.execute(dto)

    logger.debug(f"response: {users_return}")
    logger.info(f"Stop handle get users by filters")
    return users_return


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    responses={
        201: {"model": api_dto.UserResponse},
        400: {"model": api_dto.HTTPException},
    },
)
async def login_user(
    response: Response,
    data: api_dto.UserLogin = Body(),
    settings: Settings = Depends(provide_settings_stub),
    interactor: UserLoginInteractor = Depends(
        provide_user_login_interactor_stub
    ),
):
    logger.info("Start handle login user")

    dto = UserLogin(
        login=data.login,
        raw_password=data.password,
    )
    logger.debug(f"data: {asdict(dto)}")

    try:
        user, session_id = await interactor.execute(dto)
    except UserInvalidEmailException as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return api_dto.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            errors=str(e),
        )
    except UserInvalidPasswordException as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return api_dto.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            errors=str(e),
        )

    # response.set_cookie(
    #     "session_id",
    #     session_id,
    #     httponly=True,
    #     secure=settings.https,
    # )

    logger.info("Stop handle login user")
    return user


@router.post(
    path="/logout", status_code=status.HTTP_200_OK, response_model=None
)
async def logout_User(
    response: Response,
    interactor: UserLogoutInteractor = Depends(
        provide_user_logout_interactor_stub
    ),
):
    logger.info(f"Start logout create user")
    dto = UserLogout()
    logger.debug(f"data: {asdict(dto)}")

    await interactor.execute(dto)

    expires = datetime.datetime.now() - datetime.timedelta(days=1)
    expires_str = expires.astimezone(pytz.utc).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    response.set_cookie("session_id", value="", expires=expires_str)

    logger.info(f"Stop logout create user")
    return "success"


@router.delete(path="", status_code=status.HTTP_200_OK, response_model=None)
async def delete_User(
    id: UserId,
    interactor: UserDeleteInteractor = Depends(
        provide_user_delete_interactor_stub
    ),
):
    logger.info(f"Start handle delete user")
    dto = UserDelete(user_id=id)
    logger.debug(f"data: {asdict(dto)}")

    await interactor.execute(dto)

    logger.info(f"Stop handle delete user")
    return "success"
