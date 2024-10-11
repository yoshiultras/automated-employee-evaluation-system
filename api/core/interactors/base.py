from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DtoType = TypeVar("DtoType")
ReturnType = TypeVar("ReturnType")


class Interactor(ABC, Generic[DtoType, ReturnType]):
    @abstractmethod
    async def execute(self, data: DtoType) -> ReturnType:
        raise NotImplementedError
