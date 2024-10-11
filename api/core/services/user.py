import logging
from datetime import datetime
from typing import Optional
from uuid import uuid4

from api.core.entities import User, UserRole, UserId

logger = logging.getLogger(__name__)


class UserService:
    def create(
        self,
        external_id: str,
        role: UserRole,
        external_role: str,
        name: str,
        surname: str,
        patronymic: str,
        email: str,
        login: str,
        password: str,
    ) -> User:
        logger.debug(
            f"Creating user with name: {name}, surname: {surname}, patronymic: {patronymic}"
        )
        id = UserId(uuid4())

        new_user = User(
            id=id,
            external_id=external_id,
            role=role,
            external_role=external_role,
            name=name,
            surname=surname,
            patronymic=patronymic,
            email=email,
            login=login,
            password=password,
            last_login=None,
            created_at=datetime.now(),
        )
        return new_user
