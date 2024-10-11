from typing import Optional
from dataclasses import dataclass
from api.core.entities import ServiceID, ServiceRolesID


@dataclass()
class ServiceDelete:
    id: ServiceID


@dataclass()
class ServiceResponse:
    id: Optional[ServiceID]
    name: str


@dataclass()
class ServiceGet:
    id: ServiceID


@dataclass
class ServiceCreate:
    id: ServiceID
    name: str
