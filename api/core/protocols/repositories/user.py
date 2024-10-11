from typing import Optional, Protocol

from api.core.dto import UserGetAll, UserGetByFilters, UsersPaginated
from api.core.entities import User, UserId


class UserRepository(Protocol):
    async def get(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def get_all(self, data: UserGetAll) -> UsersPaginated:
        raise NotImplementedError

    async def get_by_filters(
        self, filters: UserGetByFilters
    ) -> UsersPaginated:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    async def add(self, new_user: User) -> User:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError

    async def delete(self, user_id: UserId) -> None:
        raise NotImplementedError
