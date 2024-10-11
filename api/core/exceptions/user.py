from api.core.exceptions import (
    AlreadyExistsInteractorErr,
    InteractorErr,
    NotFoundInteractorErr,
)


class UserInteractorErr(InteractorErr):
    entity_name = "user"


class UserNotFoundException(UserInteractorErr, NotFoundInteractorErr): ...


class UserAlreadyExistsException(
    UserInteractorErr, AlreadyExistsInteractorErr
): ...


class UserInvalidPasswordException(UserInteractorErr):
    def __str__(self):
        return "bad user password"

    def __repr__(self):
        return str(self)


class UserInvalidEmailException(UserInteractorErr):
    def __str__(self):
        return "bad user email"

    def __repr__(self):
        return str(self)
