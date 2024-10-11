from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from typing import Optional

from api.core.dto.base import (
    ModelResponse,
    PaginatedItemsDto,
    PaginatedItemsResponse,
    PaginationParamsDto,
    DefaultValue,
)
from api.core.entities import User, UserId, UserRole


class UserSortFieldName(str, Enum):
    id = "id"
    external_id = "external_id"
    role = "role"
    external_role = "external_role"
    name = "name"  # type: ignore
    surname = "surname"
    patronymic = "patronymic"
    email = "email"
    login = "login"
    password = "password"
    last_login = "last_login"
    created_at = "created_at"


class UserPaginationParamsDto(PaginationParamsDto[UserSortFieldName]): ...


@dataclass()
class UserLogin:
    login: str
    raw_password: str


@dataclass
class WithUserDto:
    user: Optional["UserResponse"]


@dataclass
class UserGetAll:
    pagination_data: UserPaginationParamsDto


@dataclass
class UserGetById:
    user: Optional["UserResponse"]
    user_id: UserId


@dataclass()
class UserGetByFilters:
    pagination_data: UserPaginationParamsDto
    email: Optional[str | DefaultValue] = DefaultValue()


@dataclass()
class UserLogout: ...


@dataclass()
class UserDelete:
    user_id: UserId


@dataclass()
class UserResponse(ModelResponse[User]):
    id: UserId
    external_id: str
    role: UserRole
    external_role: str
    name: str
    surname: str
    patronymic: str
    email: str
    login: str
    password: str
    last_login: Optional[datetime]
    created_at: datetime

    @classmethod
    def create_from_entity(cls, model: User) -> "UserResponse":
        return cls(
            id=model.id,
            external_id=model.external_id,
            role=model.role,
            external_role=model.external_role,
            name=model.name,
            surname=model.surname,
            patronymic=model.patronymic,
            email=model.email,
            login=model.login,
            password=model.password,
            last_login=model.last_login,
            created_at=model.created_at,
        )


class UsersPaginated(PaginatedItemsDto[User]): ...


UsersPaginatedResponse = PaginatedItemsResponse[User, UserResponse]
