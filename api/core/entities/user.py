from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import NewType, Optional
from dataclasses import dataclass


UserId = NewType("UserId", UUID)
RefreshTokenId = NewType("RefreshTokenId", UUID)


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class User:
    def __init__(
        self,
        id: UserId,
        external_id: str,
        role: UserRole,
        external_role: str,
        name: str,
        surname: str,
        patronymic: str,
        email: str,
        login: str,
        password: str,
        last_login: Optional[datetime],
        created_at: datetime,
    ):
        self.id = id
        self.external_id = external_id
        self.role = role
        self.external_role = external_role
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.email = email
        self.login = login
        self.password = password
        self.last_login = last_login
        self.created_at = created_at

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.id == other.id
        return False


@dataclass()
class AccessToken:
    user_id: UserId
    jwt_token_data: "AccessJWTTokenData"
    expires_at: datetime

@dataclass()
class AccessJWTTokenData:
    user_id: UserId
    role: UserRole
    expires_at: datetime
    token: str


@dataclass()
class RefreshToken:
    id: RefreshTokenId
    user_id: UserId
    expires_at: datetime
    issued_at: datetime
