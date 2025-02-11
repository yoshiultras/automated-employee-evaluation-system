from datetime import datetime

from sqlalchemy import MetaData, Boolean, TIMESTAMP, JSON, Table, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

metadata = MetaData()

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

departments = Table(

    "departments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name_of_department", String, nullable=False),
    Column("affiliation", Integer,ForeignKey("faculties_and_institutes.id"), nullable=False),

)

metric_descriptions = Table(

    "metric_descriptions",
    metadata,
    Column("metric_id", Integer, primary_key=True, autoincrement=True),
    Column("metric_number", Integer, nullable=False),
    Column("metric_subnumber", String, nullable=False),
    Column("description", String, nullable=False),
    Column("unit_of_measurement", String, nullable=False),
    Column("base_level", String, nullable=False),
    Column("average_level", String, nullable=False),
    Column("goal_level", String, nullable=False),
    Column("measurement_frequency", String, nullable=False),
    Column("conditions", String, nullable=False),
    Column("notes", String, nullable=False),
    Column("points", Integer, nullable=False),
    Column("section_id", Integer,ForeignKey("sections.id"), nullable=False),

)

sections = Table(

    "sections",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String, nullable=False),

)

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
