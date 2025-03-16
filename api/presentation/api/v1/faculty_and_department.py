from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import FacultyAndInstitute, Department
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

# Pydantic схемы
class FacultyAndInstituteBase(BaseModel):
    name: str

class FacultyAndInstituteCreate(FacultyAndInstituteBase):
    pass

class FacultyAndInstituteResponse(FacultyAndInstituteBase):
    id: int

    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    name_of_department: str
    affiliation: int

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

router = APIRouter()

# FacultyAndInstitute Endpoints
@router.get(
    path="/faculties/",
    response_model=List[FacultyAndInstituteResponse],
    status_code=status.HTTP_200_OK
)
async def read_faculties(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(FacultyAndInstitute).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get(
    path="/faculties/{faculty_id}",
    response_model=FacultyAndInstituteResponse,
    status_code=status.HTTP_200_OK
)
async def read_faculty(
        faculty_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(FacultyAndInstitute).where(FacultyAndInstitute.id == faculty_id)
    )
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty

@router.post(
    path="/faculties/",
    response_model=FacultyAndInstituteResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_faculty(
        faculty: FacultyAndInstituteCreate,
        session: AsyncSession = Depends(get_async_session)
):
    db_faculty = FacultyAndInstitute(**faculty.dict())
    session.add(db_faculty)
    await session.commit()
    await session.refresh(db_faculty)
    return db_faculty

@router.put(
    path="/faculties/{faculty_id}",
    response_model=FacultyAndInstituteResponse,
    status_code=status.HTTP_200_OK
)
async def update_faculty(
        faculty_id: int,
        faculty: FacultyAndInstituteCreate,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(FacultyAndInstitute).where(FacultyAndInstitute.id == faculty_id)
    )
    db_faculty = result.scalar_one_or_none()
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    for key, value in faculty.dict().items():
        setattr(db_faculty, key, value)

    session.add(db_faculty)
    await session.commit()
    await session.refresh(db_faculty)
    return db_faculty

@router.delete(
    path="/faculties/{faculty_id}",
    status_code=status.HTTP_200_OK
)
async def delete_faculty(
        faculty_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(FacultyAndInstitute).where(FacultyAndInstitute.id == faculty_id)
    )
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    await session.delete(faculty)
    await session.commit()
    return {"message": "Faculty deleted successfully"}

# Department Endpoints
@router.get(
    path="/departments/",
    response_model=List[DepartmentResponse],
    status_code=status.HTTP_200_OK
)
async def read_departments(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Department).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get(
    path="/departments/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK
)
async def read_department(
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post(
    path="/departments/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_department(
        department: DepartmentCreate,
        session: AsyncSession = Depends(get_async_session)
):
    db_department = Department(**department.dict())
    session.add(db_department)
    await session.commit()
    await session.refresh(db_department)
    return db_department

@router.put(
    path="/departments/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK
)
async def update_department(
        department_id: int,
        department: DepartmentCreate,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Department).where(Department.id == department_id)
    )
    db_department = result.scalar_one_or_none()
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")

    for key, value in department.dict().items():
        setattr(db_department, key, value)

    session.add(db_department)
    await session.commit()
    await session.refresh(db_department)
    return db_department

@router.delete(
    path="/departments/{department_id}",
    status_code=status.HTTP_200_OK
)
async def delete_department(
        department_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    await session.delete(department)
    await session.commit()
    return {"message": "Department deleted successfully"}