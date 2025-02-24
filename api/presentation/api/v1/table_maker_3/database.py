import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from api.infrastructure.storage.sqlalchemy.models.asos_models import MetricDescription, Section

load_dotenv()

class Database:
    # Логика подключения к БД
    _engine = None
    _session = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            try:
                cls._engine = create_engine(
                    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
                )
                print("Соединение с PostgreSQL установлено")
            except Exception as error:
                print("Ошибка при подключении к PostgreSQL", error)
                cls._engine = None
        return cls._engine

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls._session = sessionmaker(bind=cls.get_engine())()
        return cls._session

    @classmethod
    def close_session(cls):
        if cls._session:
            cls._session.close()
            print("Соединение с PostgreSQL закрыто")
            cls._session = None

    # Метод получения метрик
    @classmethod
    def get_metrics(cls):
        session = cls.get_session()
        results = session.query(MetricDescription).order_by(MetricDescription.metric_number, MetricDescription.metric_subnumber).all()
        return results

    # Метод получения секций
    @classmethod
    def get_sections(cls):
        session = cls.get_session()
        results = session.query(Section).all()
        return results
