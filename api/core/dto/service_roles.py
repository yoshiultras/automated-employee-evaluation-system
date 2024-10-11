from typing import Optional
from dataclasses import dataclass
from api.core.entities import ServiceRole, ServiceID, ServiceRolesID


@dataclass()
class ServiceRolesDelete:
    id: ServiceRolesID


@dataclass()
class ServiceRolesCreate:
    service_id: ServiceID
    role: ServiceRole


@dataclass()
class ServiceRolesResponse:
    service_id: ServiceID
    role: ServiceRole


@dataclass()
class ServiceRolesUpdate:
    id: ServiceRolesID
    role: ServiceRole
    service_id: ServiceID


@dataclass()
class ServiceRolesGet:
    id: ServiceRolesID
