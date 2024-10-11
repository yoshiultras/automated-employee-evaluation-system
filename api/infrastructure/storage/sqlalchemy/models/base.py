import uuid
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, registry
from datetime import datetime
from typing_extensions import Annotated
from sqlalchemy.orm import DeclarativeBase, mapped_column, registry
from sqlalchemy import UUID, TIMESTAMP


uuidpk = Annotated[
    uuid.UUID,
    UUID(as_uuid=True),
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True),
]

uuidParam = Annotated[
    uuid.UUID,
    UUID(as_uuid=True),
    mapped_column(default=uuid.uuid4),
]

convention = {
    "ix": "ix_%(column_0_label)s",  # INDEX
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",  # UNIQUE
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # CHECK
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # FOREIGN KEY
    "pk": "pk_%(table_name)s",  # PRIMARY KEY
}

mapper_registry = registry(
        type_annotation_map={
            datetime: TIMESTAMP(timezone=True),
            uuid.UUID: UUID(as_uuid=True),
        },
        metadata=MetaData(naming_convention=convention)
    )


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata
