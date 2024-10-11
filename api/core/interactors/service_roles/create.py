import logging
from typing import Optional
from api.core.dto import ServiceRolesCreate, ServiceRolesResponse
from api.core.entities import ServiceRoles
from api.core.exceptions import (
    AlreadyExistsRepErr,
    ServiceRolesAlreadyExistsException,
)
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRolesRepository

logger = logging.getLogger(__name__)


class ServiceRolesCreateInteractor(
    Interactor[ServiceRolesCreate, ServiceRolesResponse]
):
    def __init__(
        self,
        uow: UnitOfWork,
        service_roles_repo: ServiceRolesRepository,
    ):
        self._uow = uow
        self._service_roles_repo = service_roles_repo

    async def execute(
        self, data: ServiceRolesCreate
    ) -> Optional[ServiceRolesResponse]:
        async with self._uow.pipeline():
            try:
                service = await self._service_roles_repo.add(
                    ServiceRoles(
                        id=None, service_id=data.service_id, role=data.role
                    )
                )
            except AlreadyExistsRepErr as e:
                logger.info(
                    f"service roles already exist: duplicated {e.attr_name}={getattr(data, e.attr_name)})"
                )
                raise ServiceRolesAlreadyExistsException(e.attr_name)

        return ServiceRolesResponse(
            service_id=service.service_id, role=service.role
        )
