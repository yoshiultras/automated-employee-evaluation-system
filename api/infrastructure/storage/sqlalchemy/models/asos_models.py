from datetime import datetime

from sqlalchemy import MetaData, Boolean, TIMESTAMP, JSON, Table, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base()

#TODO Переделать все модели в классы в соответствии с Departments

# departments = Table(
#
#     "departments",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("name_of_department", String, nullable=False),
#     Column("affiliation", Integer,ForeignKey("faculties_and_institutes.id"), nullable=False),
#
# )
class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_of_department = Column(String, nullable=False)
    affiliation = Column(Integer, ForeignKey("faculties_and_institutes.id"), nullable=False)
employees = Table(

    "employees",
    metadata,
    Column("employee_id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("mail_box", Boolean, default=False, nullable=False),
    Column("number_phone", String, nullable=False),
    Column("role_id", Integer,ForeignKey("roles.id"), nullable=False),
)

roles = Table(

    "roles",
    metadata,
    Column("role_id", Integer, primary_key=True, autoincrement=True),
    Column("role", String, nullable=False),

)

faculties_and_institutes = Table(

    "faculties_and_institutes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),

)

class MetricDescription(Base):
    __tablename__ = 'metric_descriptions'

    metric_id = Column(Integer, primary_key=True)
    metric_number = Column(Integer)
    metric_subnumber = Column(Integer)
    description = Column(String)
    unit_of_measurement = Column(String)
    base_level = Column(Integer)
    average_level = Column(Integer)
    goal_level = Column(Integer)
    measurement_frequency = Column(String)
    conditions = Column(String)
    notes = Column(String)
    points = Column(Integer)
    section_id = Column(Integer, ForeignKey('sections.id'))

    def to_array(self):
        fields_order = [
            'metric_number', 'metric_subnumber', 'description',
            'unit_of_measurement', 'base_level', 'average_level',
            'goal_level', 'measurement_frequency', 'conditions',
            'notes', 'points', 'section_id'
        ]
        return [getattr(self, field) for field in fields_order]

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    description = Column(String)

    def to_array(self):
        fields_order = ['id', 'description']
        return [getattr(self, field) for field in fields_order]

metrics_in_quartal = Table(

    "metrics_in_quartal",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("quartal", Integer, nullable=False),
    Column("duration", ARRAY(Integer), nullable=False),
    Column("metrics_id", ARRAY(Integer), nullable=False),

)

actual_working_days_on_employee = Table(

    "actual_working_days_on_employee",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("employee_id", Integer,ForeignKey("employees.employee_id"), nullable=False),
    Column("jobtitle", String, nullable=False),
    Column("year", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("count_day", Integer, nullable=False),
    Column("quarter", Integer, nullable=False),
    Column("department_id", Integer,ForeignKey("departments.id"), nullable=False),


)

actual_working_days = Table(
    "actual_working_days",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("year", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("count_day", Integer, nullable=False),
    Column("quarter", Integer, nullable=False),
)

employees_to_metrics = Table(
    "employees_to_metrics",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("metrics_id", ARRAY(Integer), nullable=False),
    Column("value", ARRAY(Integer), nullable=False),
    Column("year", Integer, nullable=False),
    Column("quarter", Integer, nullable=False),
    Column("employee_id", Integer,ForeignKey("employees.employee_id"), nullable=False),
)
