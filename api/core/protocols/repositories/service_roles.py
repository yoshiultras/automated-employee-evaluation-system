from typing import Optional, Protocol

from api.core.entities import ServiceRolesID, ServiceRoles


class ServiceRolesRepository(Protocol):
    async def get(self, id: ServiceRolesID) -> Optional[ServiceRoles]:
        raise NotImplementedError

    async def all(self) -> list[ServiceRoles]:
        raise NotImplementedError

    async def add(self, service: ServiceRoles) -> ServiceRoles:
        raise NotImplementedError

    async def update(self, service: ServiceRoles) -> None:
        raise NotImplementedError

    async def delete(self, id: ServiceRolesID) -> None:
        raise NotImplementedError
