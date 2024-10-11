import logging
from typing import Optional
from api.core.dto import ServiceRolesUpdate
from api.core.entities import ServiceRoles
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRolesRepository

logger = logging.getLogger(__name__)


class ServiceRolesUpdateInteractor(Interactor[ServiceRolesUpdate, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        service_roles_repo: ServiceRolesRepository,
    ):
        self._uow = uow
        self._service_roles_repo = service_roles_repo

    async def execute(self, data: ServiceRolesUpdate) -> Optional[None]:
        async with self._uow.pipeline():
            await self._service_roles_repo.update(
                ServiceRoles(
                    id=data.id, role=data.role, service_id=data.service_id
                )
            )
