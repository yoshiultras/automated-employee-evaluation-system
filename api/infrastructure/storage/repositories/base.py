from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from api.core.exceptions import RepositoryErr


class BaseRepository(ABC):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def _try_flush(
        self,
    ):
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise RepositoryErr(str(e))
