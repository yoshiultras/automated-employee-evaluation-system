from typing import Optional

from api.core.dto import ServiceRolesGet, ServiceRolesResponse
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRolesRepository


class ServiceRolesGetInteractor(
    Interactor[ServiceRolesGet, Optional[ServiceRolesResponse]]
):
    def __init__(
        self,
        uow: UnitOfWork,
        service_roles_repo: ServiceRolesRepository,
    ):
        self._uow = uow
        self._service_roles_repo = service_roles_repo

    async def execute(
        self, data: ServiceRolesGet
    ) -> Optional[ServiceRolesResponse]:
        async with self._uow.pipeline():
            service = await self._service_roles_repo.get(data.id)
        if service is None:
            return None

        return ServiceRolesResponse(
            service_id=service.service_id, role=service.role
        )
