from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Optional, Type, TypeVar, NewType

Model = TypeVar("Model")
ModelResp = TypeVar("ModelResp")
ModelItems = TypeVar("ModelItems")
SortFieldName = TypeVar("SortFieldName")

class DefaultValue(str):
    ...

class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class TypeCompare(str, Enum):
    full = "full"
    partial = "partial"


@dataclass
class PaginationParamsDto(Generic[SortFieldName]):
    page: int = 1
    size: int = 50
    sort_by: Optional[SortFieldName] = None
    sort_order: SortOrder = SortOrder.DESC


@dataclass
class PaginatedItemsDto(Generic[Model]):
    data: List[Model]
    page: int
    size: int
    total: int


class ModelResponse(Generic[Model]):
    @classmethod
    def create_from_entity(cls, model: Model) -> "ModelResponse":
        raise NotImplementedError


class PaginatedItemsResponse(Generic[Model, ModelResp]):

    def __init__(
        self, data: List[ModelResp], page: int, size: int, total: int
    ):
        self.data = data
        self.page = page
        self.size = size
        self.total = total

    @classmethod
    def create_from_paginated_items(
        cls, items: PaginatedItemsDto[Model]
    ) -> "PaginatedItemsResponse[Model, ModelResp]":
        return cls(
            data=[
                cls.response_class.create_from_entity(item)  # type: ignore
                for item in items.data
            ],
            page=items.page,
            size=items.size,
            total=items.total,
        )

