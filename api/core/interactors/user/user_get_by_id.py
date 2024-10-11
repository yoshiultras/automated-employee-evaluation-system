from typing import Optional

from api.core.dto import UserGetById, UserResponse
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, UserRepository


class UserGetByIdInteractor(Interactor[UserGetById, Optional[UserResponse]]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_repository: UserRepository,
    ):
        self._uow = uow
        self._user_repository = user_repository

    async def execute(self, data: UserGetById) -> Optional[UserResponse]:
        async with self._uow.pipeline():
            user = await self._user_repository.get(data.user_id)
        if user is None:
            return None

        return UserResponse.create_from_entity(user)
