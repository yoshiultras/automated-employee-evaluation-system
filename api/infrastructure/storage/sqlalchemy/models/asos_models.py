from datetime import datetime

from sqlalchemy import MetaData, Boolean, TIMESTAMP, JSON, Table, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'
    
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    mail_box = Column(Boolean, default=False, nullable=False)
    number_phone = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)


class Role(Base):
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)


class FacultyAndInstitute(Base):
    __tablename__ = 'faculties_and_institutes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_of_department = Column(String, nullable=False)
    affiliation = Column(Integer, ForeignKey("faculties_and_institutes.id"), nullable=False)

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


class MetricsInQuartal(Base):
    __tablename__ = 'metrics_in_quartal'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quartal = Column(Integer, nullable=False)
    duration = Column(ARRAY(Integer), nullable=False)
    metrics_id = Column(ARRAY(Integer), nullable=False)


class ActualWorkingDaysOnEmployee(Base):
    __tablename__ = 'actual_working_days_on_employee'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    jobtitle = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    count_day = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)


class ActualWorkingDays(Base):
    __tablename__ = 'actual_working_days'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    count_day = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)


class EmployeesToMetrics(Base):
    __tablename__ = 'employees_to_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    metrics_id = Column(ARRAY(Integer), nullable=False)
    value = Column(ARRAY(Integer), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
