from typing import Optional

from api.core.dto import ServiceGet, ServiceResponse
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRepository


class ServiceGetInteractor(Interactor[ServiceGet, Optional[ServiceResponse]]):
    def __init__(
        self,
        uow: UnitOfWork,
        service_repo: ServiceRepository,
    ):
        self._uow = uow
        self._service_repo = service_repo

    async def execute(self, data: ServiceGet) -> Optional[ServiceResponse]:
        async with self._uow.pipeline():
            service = await self._service_repo.get(data.id)
        if service is None:
            return None

        return ServiceResponse(id=service.id, name=service.name)
