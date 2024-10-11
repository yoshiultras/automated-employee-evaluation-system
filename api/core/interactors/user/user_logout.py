import logging

from api.core.dto import UserLogout
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork

logger = logging.getLogger(__name__)


class UserLogoutInteractor(Interactor[UserLogout, None]):
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self._uow = uow

    async def execute(self, data: UserLogout) -> None:
        async with self._uow.pipeline():
            await self._user_session_repository.delete(session.id)  # type: ignore # noqa
