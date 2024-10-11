from api.core.dto import ServiceRolesDelete
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, ServiceRolesRepository


class ServiceRolesDeleteInteractor(Interactor[ServiceRolesDelete, None]):
    def __init__(
        self,
        uow: UnitOfWork,
        service_roles_repo: ServiceRolesRepository,
    ):
        self._uow = uow
        self._service_roles_repo = service_roles_repo

    async def execute(self, data: ServiceRolesDelete) -> None:
        async with self._uow.pipeline():
            await self._service_roles_repo.delete(data.id)
