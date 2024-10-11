from typing import Optional, Type

from fastapi import Query

from api.core.dto import PaginationParamsDto, SortOrder


def get_pagination_fields(
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=10),
):
    return page, size


def get_pagination_fields_depends(
    pagination_dto_class: Type[PaginationParamsDto],
    sort_by: Type,
):
    def get_pagination_fields(
        page: int = Query(ge=1, default=1),
        size: int = Query(ge=1, le=100, default=10),
        sort_by: Optional[sort_by] = Query(None),
        sort_order: SortOrder = Query(SortOrder.DESC),
    ):
        return pagination_dto_class(
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    return get_pagination_fields
