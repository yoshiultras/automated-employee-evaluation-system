from typing import List, Optional

from pydantic import BaseModel, Field

from api.core.dto import UserResponse as UserResponse_
from api.core.entities import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    link_to_messenger: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test",
                    "password": "123",
                    "link_to_messenger": "http://example.com",
                }
            ]
        }
    }


class UserLogin(BaseModel):
    login: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test",
                    "password": "123",
                }
            ]
        }
    }


class UserGetByFilters(BaseModel):
    email: str = Field(None)
    name: str = Field(None)
    surname: str = Field(None)
    patronymic: str = Field(None)
    full_name: str = Field(None)
    phone_number: Optional[str] = Field(None)
    link_to_messenger: str = Field(None)
    roles: List[UserRole] = Field(None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "email@example.com",
                    "name": "test",
                    "surname": "test",
                    "phone_number": "01",
                    "link_to_messenger": "19",
                    "role": "user",
                }
            ]
        }
    }


class UserResponse(UserResponse_, BaseModel): ...
