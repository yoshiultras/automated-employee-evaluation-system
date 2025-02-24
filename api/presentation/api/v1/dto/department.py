from pydantic import BaseModel

class DepartmentResponse(BaseModel):
    id: int
    name_of_department: str
    affiliation: int
    model_config = {
        "from_attributes": "true",
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "name_of_department": "Кафедра",
                    "affiliation": "1",
                }
            ]
        }
    }
