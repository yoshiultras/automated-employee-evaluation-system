from typing import NoReturn, Optional

from sqlalchemy import (
    Select,
    and_,
    asc,
    delete,
    desc,
    func,
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped

from api.core.dto import (
    SortOrder,
    UserGetAll,
    UserGetByFilters,
    UserSortFieldName,
    UsersPaginated,
    DefaultValue,
)
from api.core.entities import User, UserId
from api.core.exceptions import (
    AlreadyExistsRepErr,
    ForeignConnectionRepErr,
    RepositoryErr,
)
from api.core.protocols import UserRepository
from api.infrastructure.storage.repositories.base import BaseRepository
from api.infrastructure.storage.sqlalchemy.models import (
    User as UserDbModel,
)


def add_sortings(
    query: Select, field: Optional[UserSortFieldName], order: SortOrder
) -> Select:
    db_field: Mapped = UserDbModel.id
    if field == UserSortFieldName.email:
        db_field = UserDbModel.email
    elif field == UserSortFieldName.password:
        db_field = UserDbModel.password
    elif field == UserSortFieldName.name:
        db_field = UserDbModel.name
    elif field == UserSortFieldName.surname:
        db_field = UserDbModel.surname
    elif field == UserSortFieldName.role:
        db_field = UserDbModel.role
    elif field == UserSortFieldName.last_login:
        db_field = UserDbModel.last_login
    elif field == UserSortFieldName.created_at:
        db_field = UserDbModel.created_at

    db_order = None
    if order == SortOrder.ASC:
        db_order = asc(db_field)
    elif order == SortOrder.DESC:
        db_order = desc(db_field)

    return query.order_by(db_order)


class UserRepositoryImpl(BaseRepository, UserRepository):
    model_name = "user"

    async def get(self, user_id: UserId) -> Optional[User]:
        return await self._session.scalar(
            select(UserDbModel).where(UserDbModel.id == user_id)
        )

    async def get_all(self, data: UserGetAll) -> UsersPaginated:
        pagination_data = data.pagination_data
        offset = max((pagination_data.page - 1) * pagination_data.size, 0)
        stmt = select(UserDbModel)
        stmt = add_sortings(
            stmt, pagination_data.sort_by, pagination_data.sort_order
        )
        stmt = stmt.limit(pagination_data.size).offset(offset)

        result = await self._session.scalars(stmt)
        count = await self._get_count()

        return UsersPaginated(
            data=[c.to_entity() for c in result],
            page=pagination_data.page,
            size=pagination_data.size,
            total=count,
        )

    async def get_by_filters(self, data: UserGetByFilters) -> UsersPaginated:
        pagination_data = data.pagination_data
        offset = (pagination_data.page - 1) * pagination_data.size
        stmt = select(UserDbModel)
        stmt = self._add_filters_for_stmt(stmt, data)
        stmt = add_sortings(
            stmt, pagination_data.sort_by, pagination_data.sort_order
        )
        stmt = stmt.limit(pagination_data.size).offset(offset)

        result = await self._session.execute(stmt)

        return UsersPaginated(
            data=list(result.scalars().all()),
            page=pagination_data.page,
            size=pagination_data.size,
            total=await self._get_count(data),
        )

    async def _get_count(self, filters=None) -> int:
        stmt = select(func.count(UserDbModel.id))

        if filters:
            stmt = self._add_filters_for_stmt(stmt, filters)

        count = await self._session.scalar(stmt)
        if count is None:
            count = 0

        return count

    def _add_filters_for_stmt(self, stmt, filters: UserGetByFilters):
        sql_filters = []
        if not isinstance(filters.email, DefaultValue):
            sql_filters.append(UserDbModel.email.like(f"%{filters.email}%"))

        if sql_filters:
            stmt = stmt.where(and_(*sql_filters))

        return stmt

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._session.scalar(
            select(UserDbModel).where(UserDbModel.email == email)
        )

    async def add(self, new_user: User) -> User:
        insert_query = (
            insert(UserDbModel)
            .values(
                email=new_user.email,
                password=new_user.password,
                name=new_user.name,
                surname=new_user.surname,
                patronymic=new_user.patronymic,
                role=new_user.role,
                last_login=new_user.last_login,
                created_at=new_user.created_at,
            )
            .returning(UserDbModel.id)
        )

        try:
            result = await self._session.execute(insert_query)
            new_user_db_id = result.scalar()
        except IntegrityError as e:
            self._parse_error(e)

        new_user.id = new_user_db_id  # type: ignore
        return new_user

    async def update(self, user: User) -> None:
        try:
            await self._session.execute(
                update(UserDbModel)
                .where(UserDbModel.id == user.id)  # type: ignore
                .values(
                    email=user.email,
                    password=user.password,
                    name=user.name,
                    surname=user.surname,
                    role=user.role,
                    last_login=user.last_login,
                    created_at=user.created_at,
                )
            )
        except IntegrityError as e:
            self._parse_error(e)

    async def delete(self, user_id: UserId) -> None:
        try:
            await self._session.execute(
                delete(UserDbModel).where(UserDbModel.id == user_id)
            )
        except IntegrityError as e:
            self._parse_error(e)

    def _parse_error(self, err: IntegrityError) -> NoReturn:
        db_api_err = err.__cause__.__cause__  # type: ignore
        constraint_name = db_api_err.constraint_name  # type: ignore
        error_map = {
            "uq_users_email": (
                AlreadyExistsRepErr,
                "email",
            ),
            "uq_users_link_to_messenger": (
                AlreadyExistsRepErr,
                "link_to_messenger",
            ),
            "uq_users_phone_number": (
                AlreadyExistsRepErr,
                "phone_number",
            ),
            "fk_files_creator_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_unidentified_cargo_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_unidentified_delivery_co_executors_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_unidentified_delivery_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_order_co_executors_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_order_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_shipment_co_executors_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_shipment_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_delivery_co_executors_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_delivery_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_customer_cargo_co_executors_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_customer_cargo_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_product_co_executors_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
            "fk_product_responsible_user_id_users": (
                ForeignConnectionRepErr,
                "",
            ),
        }

        if constraint_name in error_map:
            error_cls, attr_name = error_map[constraint_name]
            raise error_cls(
                model_name=self.model_name, attr_name=attr_name
            ) from err
        else:
            raise RepositoryErr from err
