from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from api.infrastructure.storage.sqlalchemy.models.asos_models import Department
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

router = APIRouter()

# Pydantic models
class DepartmentBase(BaseModel):
    name_of_department: str
    affiliation: int
    id_facultet: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name_of_department": "Инфокогнитивные технологии",
                "affiliation": 6,
                "id_facultet": 6
            }
        }

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name_of_department": "Инфокогнитивные технологии",
                "affiliation": 6,
                "id_facultet": 6
            }
        }

# Endpoints
@router.get("/departments", response_model=List[DepartmentResponse])
async def get_departments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get list of departments with pagination.
    """
    result = await session.execute(
        select(Department).offset(skip).limit(limit)
    )
    departments = result.scalars().all()
    return departments

@router.get("/departments/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get department by ID.
    """
    result = await session.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found."
        )
    
    return department

@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department: DepartmentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new department.
    """
    db_department = Department(**department.dict())
    session.add(db_department)
    await session.commit()
    await session.refresh(db_department)
    return db_department

@router.put("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department: DepartmentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update department by ID.
    """
    result = await session.execute(
        select(Department).where(Department.id == department_id)
    )
    db_department = result.scalar_one_or_none()
    
    if not db_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found."
        )
    
    for key, value in department.dict().items():
        setattr(db_department, key, value)
    
    session.add(db_department)
    await session.commit()
    await session.refresh(db_department)
    return db_department

@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete department by ID.
    """
    result = await session.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID {department_id} not found."
        )
    
    await session.delete(department)
    await session.commit()
    return None