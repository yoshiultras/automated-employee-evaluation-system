from typing import Optional, Protocol

from api.core.entities import Service, ServiceID


class ServiceRepository(Protocol):
    async def get(self, id: ServiceID) -> Optional[Service]:
        raise NotImplementedError

    async def all(self) -> list[Service]:
        raise NotImplementedError

    async def add(self, service: Service) -> Service:
        raise NotImplementedError

    async def update(self, service: Service) -> None:
        raise NotImplementedError

    async def delete(self, id: ServiceID) -> None:
        raise NotImplementedError
