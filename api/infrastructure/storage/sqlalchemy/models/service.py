from sqlalchemy import String
from api.core import entities
from sqlalchemy.orm import mapped_column, Mapped
from api.infrastructure.storage.sqlalchemy.models import BaseModel, uuidpk


class Service(BaseModel, entities.Service):
    __tablename__ = "service"

    id: Mapped[uuidpk]
    name: Mapped[str] = mapped_column(String(), nullable=False)
