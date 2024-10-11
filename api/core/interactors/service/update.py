import logging
from typing import Optional
from api.core.dto import ServiceCreate
from api.core.entities import Service
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRepository

logger = logging.getLogger(__name__)


class ServiceUpdateInteractor(Interactor[ServiceCreate, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        service_repo: ServiceRepository,
    ):
        self._uow = uow
        self._service_repo = service_repo

    async def execute(self, data: ServiceCreate) -> Optional[None]:
        async with self._uow.pipeline():
            await self._service_repo.update(Service(id=None, name=data.name))
