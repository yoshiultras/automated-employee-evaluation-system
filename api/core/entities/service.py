from enum import Enum
from uuid import UUID
from typing import NewType, Optional

ServiceID = NewType("ServiceID", UUID)
ServiceRolesID = NewType("ServiceRolesID", UUID)

class ServiceRole(str, Enum):
    user = "user"
    admin = "admin"


class Service:
    def __init__(
        self,
        id: Optional[ServiceID],
        name: str
    ):
        self.id = id
        self.name = name


class ServiceRoles:
    def __init__(
        self,
        id: Optional[ServiceRolesID],
        service_id: ServiceID,
        role: ServiceRole,
    ):
        self.id = id
        self.service_id = service_id
        self.role = role