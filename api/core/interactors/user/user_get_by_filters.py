from api.core.dto import UserGetByFilters, UsersPaginatedResponse
from api.core.interactors import Interactor
from api.core.protocols import UnitOfWork, UserRepository


class UserGetByFiltersInteractor(
    Interactor[UserGetByFilters, UsersPaginatedResponse]
):
    def __init__(
        self,
        uow: UnitOfWork,
        user_repository: UserRepository,
    ):
        self._uow = uow
        self._user_repository = user_repository

    async def execute(self, data: UserGetByFilters) -> UsersPaginatedResponse:
        async with self._uow.pipeline():
            users_paginated = await self._user_repository.get_by_filters(data)

        return UsersPaginatedResponse.create_from_paginated_items(
            items=users_paginated
        )
