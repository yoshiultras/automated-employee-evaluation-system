from api.core.exceptions import (
    AlreadyExistsInteractorErr,
    InteractorErr,
    NotFoundInteractorErr,
)


class ServiceInteractorErr(InteractorErr):
    entity_name = "service"


class ServiceNotFoundException(
    ServiceInteractorErr, NotFoundInteractorErr
): ...


class ServiceAlreadyExistsException(
    ServiceInteractorErr, AlreadyExistsInteractorErr
): ...
