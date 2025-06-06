from datetime import datetime
from sqlalchemy import MetaData, Boolean, TIMESTAMP, JSON, Table, Column, Integer, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base()


class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    subname = Column(String(255))


class Role(Base):
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True)
    role = Column(String)


class Employee(Base):
    __tablename__ = 'employees'
    
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    surname = Column(String)
    mail_box = Column(String)
    number_phone = Column(String)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    login = Column(String)
    password = Column(String)


class CommissionMember(Base):
    __tablename__ = 'commissionmembers'
    
    commission_member_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))


class FacultyAndInstitute(Base):
    __tablename__ = 'faculties_and_institutes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name_of_department = Column(String, nullable=False)
    affiliation = Column(Integer)
    id_facultet = Column(Integer, ForeignKey("faculties_and_institutes.id"))


class Section(Base):
    __tablename__ = 'sections'
    
    id = Column(Integer, primary_key=True)
    description = Column(String)


class MetricDescription(Base):
    __tablename__ = 'metric_descriptions'
    
    metric_id = Column(Integer, primary_key=True)
    metric_number = Column(Integer)
    metric_subnumber = Column(String)
    description = Column(String)
    unit_of_measurement = Column(String)
    base_level = Column(String)
    average_level = Column(String)
    goal_level = Column(String)
    measurement_frequency = Column(String)
    conditions = Column(String)
    notes = Column(String)
    points = Column(Integer)
    section_id = Column(Integer, ForeignKey('sections.id'))
    date_start = Column(Date)
    date_end = Column(Date)
    is_active = Column(Boolean)

    def to_array(self):
        fields_order = [
            'metric_number', 'metric_subnumber', 'description',
            'unit_of_measurement', 'base_level', 'average_level',
            'goal_level', 'measurement_frequency', 'conditions',
            'notes', 'points', 'section_id'
        ]
        return [getattr(self, field) for field in fields_order]
        
    def to_dict(self):
        return {
            "metric_id": self.metric_id,
            "metric_number": self.metric_number,
            "metric_subnumber": self.metric_subnumber,
            "description": self.description,
            "unit_of_measurement": self.unit_of_measurement,
            "base_level": self.base_level,
            "average_level": self.average_level,
            "goal_level": self.goal_level,
            "measurement_frequency": self.measurement_frequency,
            "conditions": self.conditions,
            "notes": self.notes,
            "points": self.points,
            "section_id": self.section_id,
        }


class MetricsInQuartal(Base):
    __tablename__ = 'metrics_in_quartal'
    
    id = Column(Integer, primary_key=True)
    quartal = Column(Integer)
    duration = Column(ARRAY(Integer))
    metrics_id = Column(ARRAY(Integer))


class Responsibility(Base):
    __tablename__ = 'responsibilities'
    
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    letter = Column(String(255))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    indicator = Column(String)


class EmployeeResponsibility(Base):
    __tablename__ = 'employee_responsibility'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    responsibility_id = Column(Integer, ForeignKey("responsibilities.id"))


class ActualWorkingDays(Base):
    __tablename__ = 'actual_working_days'
    
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    count_day = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)


class ActualWorkingDaysOnEmployee(Base):
    __tablename__ = 'actual_working_days_on_employee'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    jobtitle = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    count_day = Column(Integer)
    quarter = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))


class DepartmentsMetrics(Base):
    __tablename__ = 'departments_metrics'
    
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    value = Column(Integer)
    year = Column(Integer)
    quarter = Column(Integer)
    period_date = Column(Date)
    metrics_id = Column(Integer, ForeignKey("metric_descriptions.metric_id"))
    author_id = Column(Integer, ForeignKey("employees.employee_id"))
    status = Column(Integer)


class EmployeesToMetrics(Base):
    __tablename__ = 'employees_to_metrics'
    
    id = Column(Integer, primary_key=True)
    metrics_id = Column(ARRAY(Integer))
    year = Column(Integer)
    quarter = Column(Integer)
    date_start = Column(Date)
    date_end = Column(Date)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))