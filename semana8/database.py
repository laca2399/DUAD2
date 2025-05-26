from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            DATABASE_URL = "postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres"
            cls._instance.engine = create_engine(DATABASE_URL, echo=False)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
        return cls._instance

db = DatabaseConnection()