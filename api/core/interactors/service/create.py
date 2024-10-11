import logging
from typing import Optional
from api.core.dto import ServiceCreate, ServiceResponse
from api.core.entities import Service
from api.core.exceptions import (
    AlreadyExistsRepErr,
    ServiceAlreadyExistsException,
)
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRepository

logger = logging.getLogger(__name__)


class ServiceCreateInteractor(Interactor[ServiceCreate, ServiceResponse]):
    def __init__(
        self,
        uow: UnitOfWork,
        service_repo: ServiceRepository,
    ):
        self._uow = uow
        self._service_repo = service_repo

    async def execute(self, data: ServiceCreate) -> Optional[ServiceResponse]:
        async with self._uow.pipeline():
            try:
                service = await self._service_repo.add(
                    Service(id=None, name=data.name)
                )
            except AlreadyExistsRepErr as e:
                logger.info(
                    f"service already exist: duplicated {e.attr_name}={getattr(data, e.attr_name)})"
                )
                raise ServiceAlreadyExistsException(e.attr_name)

        return ServiceResponse(id=service.id, name=service.name)
