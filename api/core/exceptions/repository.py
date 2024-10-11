from api.core.exceptions import EntityAttrErr

from .base import RepositoryErr


class AlreadyExistsRepErr(RepositoryErr):
    def __init__(self, model_name: str, attr_name: str) -> None:
        self.model_name = model_name
        self.attr_name = attr_name


class NotFoundRepErr(RepositoryErr):
    def __init__(self, model_name: str, attr_name: str) -> None:
        self.model_name = model_name
        self.attr_err: EntityAttrErr = EntityAttrErr(attr_name, "not found")


class ForeignConnectionRepErr(RepositoryErr):
    def __init__(self, model_name: str, attr_name="") -> None:
        self.model_name = model_name
        self.attr_name = attr_name
        self.err_msg = "foreign connection"

    def __str__(self):
        return self.model_name
