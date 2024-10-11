from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from api.core.protocols import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.__session = session

    @asynccontextmanager
    async def _transaction(self):
        has_exception = False
        try:
            if (
                not self.__session.in_transaction()
                and self.__session.is_active
            ):
                await self.__session.begin()
            yield
        except Exception as e:
            has_exception = True
            await self.rollback()
            raise e
        finally:
            if not has_exception:
                await self.commit()

    async def rollback(self):
        await self.__session.rollback()

    def pipeline(self):
        return self._transaction()

    async def commit(self):
        await self.__session.commit()
