# from typing import Optional, Sequence
# from api.infrastructure.storage.repositories.base import BaseRepository
# from api.core.entities import ServiceRoles, ServiceID
# from sqlalchemy.sql import select, update
# from ..sqlalchemy.models import ServiceRoles as ServiceRolesModel

# class ServiceRolesRepository(BaseRepository):
#     async def get(self, id: ServiceID) -> Optional[ServiceRoles]:
#        return await self._session.scalar(
#                 select(ServiceRolesModel).where(ServiceRolesModel.id == id)
#         )

#     async def all(self, limit: int, ofsset: int) -> Sequence[ServiceRoles]:
#         result = await self._session.execute(select(ServiceRolesModel).limit(limit).offset(ofsset))
#         return result.scalars().all()

#     async def create(self, id: Optional[ServiceID], name: str):
#         service = ServiceRoles(id=id, name=name)
#         self._session.add(service)
#         await self._try_flush()

#     async def update(self, service: ServiceRoles) -> None:
#         await self._session.execute(
#             update(ServiceRolesModel)
#             .where(ServiceRolesModel.id == service.id)
#             .values(
#                 id=service.id,
#                 name=service.name
#             )
#         )

#     async def delete(self, service: ServiceRoles) -> None:
#         await self._session.delete(service)
