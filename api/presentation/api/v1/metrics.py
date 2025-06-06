from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import Dict, List, Optional

from sqlalchemy import nulls_last, update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.infrastructure.storage.sqlalchemy.models.asos_models import Section, MetricDescription
from api.infrastructure.storage.sqlalchemy.session_maker import get_async_session

from datetime import date

# Pydantic схемы
class SectionBase(BaseModel):
    description: str
    model_config = {
        "from_attributes": "true",
        "json_schema_extra": {
            "examples": [
                {
                    "description": "Секция"
                }
            ]
        }
    }

class SectionCreate(SectionBase):
    pass

class SectionResponse(SectionBase):
    id: int

    class Config:
        orm_mode = True
        model_config = {
            "from_attributes": "true",
            "json_schema_extra": {
                "examples": [
                    {
                        "id": "1"
                    }
                ]
            }
        }

class MetricDescriptionBase(BaseModel):
    metric_number: Optional[int]
    metric_subnumber: Optional[str]
    description: Optional[str]
    unit_of_measurement: Optional[str] = None
    base_level: Optional[str] = None
    average_level: Optional[str] = None
    goal_level: Optional[str] = None
    measurement_frequency: Optional[str] = None
    conditions: Optional[str] = None
    notes: Optional[str] = None
    points: Optional[int] = None
    section_id: int
    model_config = {
        "from_attributes": "true",
        "json_schema_extra": {
            "examples": [
                {
                    "metric_number": "1",
                    "metric_subnumber": "a",
                    "description": "Описание",
                    "unit_of_measurement": "шт.",
                    "base_level": "от 20 до 40",
                    "average_level": "от 40 до 60",
                    "goal_level": "от 60 до 80",
                    "measurement_frequency": "1 раз в год, март",
                    "conditions": "Данные внутреннего мониторинга Московского Политеха.",
                    "notes": "Итоговый балл определяется как произведение балла на коэффициент достигнутого уровня",
                    "points": "10",
                    "section_id": "1"
                }
            ]
        }
    }

class MetricDescriptionCreate(MetricDescriptionBase):
    pass

class MetricDescriptionResponse(MetricDescriptionBase):
    metric_id: int
    section: Optional[Dict[str, str]] 
    class Config:
        orm_mode = True
        model_config = {
            "from_attributes": "true",
            "json_schema_extra": {
                "examples": [
                    {
                        "id": "1"
                    }
                ]
            }
        }


router = APIRouter()



# Section Endpoints
@router.get(
    path="/sections/",
    response_model=List[SectionResponse],
    status_code=status.HTTP_200_OK
)
async def read_sections(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Section).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get(
    path="/sections/{section_id}",
    response_model=SectionResponse,
    status_code=status.HTTP_200_OK
)
async def read_section(
        section_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Section).where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.post(
    path="/sections/",
    response_model=SectionResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_section(
        section: SectionCreate,
        session: AsyncSession = Depends(get_async_session)
):
    db_section = Section(**section.dict())
    session.add(db_section)
    await session.commit()
    await session.refresh(db_section)
    return db_section


@router.put(
    path="/sections/{section_id}",
    response_model=SectionResponse,
    status_code=status.HTTP_200_OK
)
async def update_section(
        section_id: int,
        section: SectionCreate,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Section).where(Section.id == section_id)
    )
    db_section = result.scalar_one_or_none()
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")

    for key, value in section.dict().items():
        setattr(db_section, key, value)

    session.add(db_section)
    await session.commit()
    await session.refresh(db_section)
    return db_section


@router.delete(
    path="/sections/{section_id}",
    status_code=status.HTTP_200_OK
)
async def delete_section(
        section_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Section).where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    await session.delete(section)
    await session.commit()
    return {"message": "Section deleted successfully"}


# MetricDescription Endpoints
@router.get(
    path="/",
    response_model=List[MetricDescriptionResponse],
    status_code=status.HTTP_200_OK
)
async def read_metrics(
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем метрики вместе с секциями
        stmt = (
            select(MetricDescription, Section.description.label("section_description"))
            .join(Section, MetricDescription.section_id == Section.id).where(MetricDescription.is_active == True)
            .order_by(
                MetricDescription.section_id.asc(),
                MetricDescription.metric_number.asc(),
                MetricDescription.metric_subnumber.asc()
            )
            .offset(skip)
            .limit(limit)
        )
        
        result = await session.execute(stmt)
        
        # Формируем ответ с включением информации о секции
        metrics = []
        for metric, section_desc in result:
            metric_dict = metric.__dict__
            # Удаляем внутренние атрибуты SQLAlchemy
            metric_dict.pop('_sa_instance_state', None)
            # Добавляем информацию о секции
            metric_dict["section"] = {"description": section_desc}
            metrics.append(metric_dict)
            
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении метрик: {str(e)}"
        )


@router.get(
    path="/{metric_id}",
    response_model=MetricDescriptionResponse,
    status_code=status.HTTP_200_OK
)
async def read_metric(
        metric_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(MetricDescription).where(MetricDescription.metric_id == metric_id and MetricDescription.is_active == True)
    )
    metric = result.scalar_one_or_none()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.post(
    path="/",
    response_model=MetricDescriptionResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_metric(
        metric: MetricDescriptionCreate,
        session: AsyncSession = Depends(get_async_session)
):
    db_metric = MetricDescription(**metric.dict())
    session.add(db_metric)
    await session.commit()
    await session.refresh(db_metric)
    return db_metric


@router.put(
    path="/{metric_id}",
    response_model=MetricDescriptionResponse,
    status_code=status.HTTP_200_OK
)
async def update_metric(
        metric_id: int,
        metric: MetricDescriptionCreate,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(MetricDescription).where(MetricDescription.metric_id == metric_id)
    )
    db_metric = result.scalar_one_or_none()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    for key, value in metric.dict().items():
        setattr(db_metric, key, value)

    session.add(db_metric)
    await session.commit()
    await session.refresh(db_metric)
    return db_metric


@router.delete(
    path="/{metric_id}",
    status_code=status.HTTP_200_OK
)
async def delete_metric(
        metric_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(MetricDescription).where(MetricDescription.metric_id == metric_id)
    )
    metric = result.scalar_one_or_none()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    await session.delete(metric)
    await session.commit()
    return {"message": "Metric deleted successfully"}

@router.put(
    path="/",
    status_code=status.HTTP_200_OK
)
async def update_metrics(
    data: List[Dict],
    session: AsyncSession = Depends(get_async_session)
):
    current_date = date.today()
    
    METRIC_FIELDS = {
        'metric_number', 'metric_subnumber', 'description',
        'unit_of_measurement', 'base_level', 'average_level', 'goal_level',
        'measurement_frequency', 'conditions', 'notes', 'points',
        'section_id', 'date_start', 'date_end', 'is_active'
    }

    try:
        for metric_data in data:
            # 1. Обрабатываем раздел (section) если он есть в данных
            if 'section' in metric_data:
                section_data = metric_data['section']
                section_id = metric_data.get('section_id')
                
                if not section_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Metric is missing 'section_id' field"
                    )
                
                # Проверяем существование раздела
                result = await session.execute(
                    select(Section)
                    .where(Section.id == section_id)
                )
                section = result.scalar_one_or_none()
                
                if section:
                    # Обновляем описание раздела, если оно изменилось
                    if section.description != section_data['description']:
                        await session.execute(
                            update(Section)
                            .where(Section.id == section_id)
                            .values(description=section_data['description'])
                        )
                else:
                    # Создаем новый раздел (если вдруг не существует)
                    await session.execute(
                        insert(Section)
                        .values(
                            id=section_id,
                            description=section_data['description']
                        )
                    )
            
            # 2. Обновляем метрику
            old_metric_id = metric_data.get('metric_id')
            
            if not old_metric_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Metric is missing 'metric_id' field"
                )
            
            # Деактивируем старую запись метрики
            await session.execute(
                update(MetricDescription)
                .where(MetricDescription.metric_id == old_metric_id)
                .values(
                    date_end=current_date,
                    is_active=False
                )
            )
            
            # Создаем новую запись метрики
            new_metric_data = {
                k: v for k, v in metric_data.items() 
                if k in METRIC_FIELDS  # Убрана проверка k != 'metric_id'
            }
            
            # Убедимся, что metric_id не попадает в новые данные
            new_metric_data.pop('metric_id', None)
            
            new_metric_data.update({
                'date_start': current_date,
                'is_active': True,
                'date_end': None
            })
            
            await session.execute(
                insert(MetricDescription)
                .values(**new_metric_data)
            )
        
        await session.commit()
        return {"status": "success", "message": "Metrics and sections updated successfully"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )