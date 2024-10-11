import re
from typing import TYPE_CHECKING, List
from urllib.parse import urlparse

from api.core.exceptions import EntityAttrErr

if TYPE_CHECKING:
    from api.core.entities import UserId


def is_valid_phone_number(phone_number: str) -> bool:
    phone_number_pattern = r"^((\+7\d{10})|(\+86\d{11}))$"
    return bool(re.match(phone_number_pattern, phone_number))


def validate_phone_number(phone_number: str):
    if not is_valid_phone_number(phone_number):
        raise EntityAttrErr("phone_number", "Invalid phone number")


def validate_positive_number(number: int | float, attr_name):
    if number <= 0:
        raise EntityAttrErr(attr_name, "Must be greater than 0")


def validate_non_negative_number(number: int | float, attr_name):
    if number < 0:
        raise EntityAttrErr(attr_name, "Must be greater than or equal to 0")


def is_valid_url(url: str) -> bool:
    valid_url = False
    try:
        result = urlparse(url)
        valid_url = all([result.scheme, *result.netloc.split(".")])
    except ValueError:
        ...
    return valid_url


def validate_models_not_repeatable(models: List, attr_name):
    ids = [p.id for p in models]
    if len(set(ids)) != len(models):
        raise EntityAttrErr(attr_name, "Should be no repetitions")


def validate_link(attr_name: str, link_to_messenger: str):
    if not is_valid_url(link_to_messenger):
        raise EntityAttrErr(attr_name, "Invalid link")
