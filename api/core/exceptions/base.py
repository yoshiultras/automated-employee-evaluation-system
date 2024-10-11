class EntityErr(Exception):
    ...


class EntityAttrErr(EntityErr):
    def __init__(self, attr_name: str, err_msg: str):
        self.attr_name = attr_name
        self.err_msg = err_msg

    def __str__(self):
        return "bad field data"


class InteractorErr(Exception):
    entity_name = ""


class AlreadyExistsInteractorErr(InteractorErr):
    def __init__(self, attr_name: str):
        self.attr_err: EntityAttrErr = EntityAttrErr(
            attr_name, "duplicated in other records"
        )

    def __str__(self):
        return f"{self.entity_name} already exists"

    def __repr__(self):
        return str(self)


class NotFoundInteractorErr(InteractorErr):
    def __str__(self):
        return f"{self.entity_name} not found"

    def __repr__(self):
        return str(self)


class RepositoryErr(Exception):
    ...
