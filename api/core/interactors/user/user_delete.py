from api.core.dto import UserDelete
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, UserRepository


class UserDeleteInteractor(Interactor[UserDelete, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_repository: UserRepository,
    ):
        self._uow = uow
        self._user_repository = user_repository

    async def execute(self, data: UserDelete) -> None:
        async with self._uow.pipeline():
            await self._user_repository.delete(user_id=data.user_id)
