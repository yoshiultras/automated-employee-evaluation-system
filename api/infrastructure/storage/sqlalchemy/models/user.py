from typing import Optional
from datetime import datetime
from sqlalchemy import (
    TIMESTAMP,
    Enum,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import mapped_column, Mapped


from api.core import entities
from api.infrastructure.storage.sqlalchemy.models import BaseModel, uuidpk


class User(BaseModel, entities.User):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    external_id: Mapped[str] = mapped_column(String(), nullable=False)
    role: Mapped[entities.UserRole] = mapped_column(Enum(entities.UserRole, name="user_role"), nullable=False)  # type: ignore # noqa
    external_role: Mapped[str] = mapped_column(String(), nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    surname: Mapped[str] = mapped_column(String(), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), nullable=False)
    login: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=False)

    __table_args__ = (
        UniqueConstraint("external_id"),
        UniqueConstraint("email"),
        UniqueConstraint("login"),
    )
