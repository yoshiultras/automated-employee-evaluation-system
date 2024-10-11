from typing import AsyncContextManager, Protocol


class UnitOfWork(Protocol):
    def pipeline(self) -> AsyncContextManager:
        raise NotImplementedError
