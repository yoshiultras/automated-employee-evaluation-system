from typing import Optional
from sqlalchemy import String, ForeignKey, Enum
from api.core import entities
from sqlalchemy.orm import mapped_column, Mapped
from api.infrastructure.storage.sqlalchemy.models import (
    BaseModel,
    uuidpk,
    uuidParam,
)


class ServiceRoles(BaseModel, entities.ServiceRoles):
    __tablename__ = "service_roles"

    id: Mapped[uuidpk]
    name: Mapped[str] = mapped_column(String(), nullable=False)
    service_id: Mapped[Optional[uuidParam]] = mapped_column(
        ForeignKey("service.id", ondelete="CASCADE", use_alter=True)
    )
    role: Mapped[entities.ServiceRole] = mapped_column(Enum(entities.ServiceRole, name="service_role"), nullable=False)  # type: ignore # noqa
