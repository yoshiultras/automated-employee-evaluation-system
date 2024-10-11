from typing import Optional, Sequence
from api.infrastructure.storage.repositories.base import BaseRepository
from api.core.entities import Service, ServiceID
from sqlalchemy.sql import select, update
from ..sqlalchemy.models import Service as ServiceModel


class ServiceRepository(BaseRepository):
    async def get(self, id: ServiceID) -> Optional[Service]:
        return await self._session.scalar(
            select(ServiceModel).where(ServiceModel.id == id)
        )

    async def all(self, limit: int, ofsset: int) -> Sequence[Service]:
        result = await self._session.execute(
            select(ServiceModel).limit(limit).offset(ofsset)
        )
        return result.scalars().all()

    async def create(self, id: Optional[ServiceID], name: str):
        service = Service(id=id, name=name)
        self._session.add(service)
        await self._try_flush()

    async def update(self, service: Service) -> None:
        await self._session.execute(
            update(ServiceModel)
            .where(ServiceModel.id == service.id)
            .values(id=service.id, name=service.name)
        )

    async def delete(self, service: Service) -> None:
        await self._session.delete(service)
