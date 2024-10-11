from api.core.dto import ServiceDelete
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRepository


class ServiceDeleteInteractor(Interactor[ServiceDelete, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        service_repo: ServiceRepository,
    ):
        self._uow = uow
        self._service_repo = service_repo

    async def execute(self, data: ServiceDelete) -> None:
        async with self._uow.pipeline():
            await self._service_repo.delete(data.id)
