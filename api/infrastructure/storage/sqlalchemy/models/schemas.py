from pydantic import BaseModel

class PostMetrics (BaseModel):
    quarter: int
    year: int
    employee_id: int
    metrics: dict[int , int]

class GetForMetrics (BaseModel):
    quarter: int
    year: int
    employee_id: int
    department_id: int

class GetQuarter (BaseModel):
    quarter: int

class GetQuarterAndDepartment:
    quarter: int
    department_id: int