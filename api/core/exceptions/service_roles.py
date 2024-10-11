from api.core.exceptions import (
    AlreadyExistsInteractorErr,
    InteractorErr,
    NotFoundInteractorErr,
)


class ServiceRolesInteractorErr(InteractorErr):
    entity_name = "service"


class ServiceRolesNotFoundException(
    ServiceRolesInteractorErr, NotFoundInteractorErr
): ...


class ServiceRolesAlreadyExistsException(
    ServiceRolesInteractorErr, AlreadyExistsInteractorErr
): ...
