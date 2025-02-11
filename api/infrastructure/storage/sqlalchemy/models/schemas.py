from pydantic import BaseModel

class Post_Metrics (BaseModel):
    quarter: int
    year: int
    employee_id: int
    metrics: dict[int , int]

class Get_For_Metrics (BaseModel):
    quarter: int
    year: int
    employee_id: int
    department_id: int

class Get_Quarter (BaseModel):
    quarter: int

class Get_Quarter_and_Depart:
    quarter: int
    id_depart: int