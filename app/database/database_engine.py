from typing import Optional
from sqlalchemy import create_engine, Engine
import os
from dotenv import load_dotenv


class DatabaseEngine:
    engine: Optional[Engine] = None

    @classmethod
    def create_mysql_db_engine(cls) -> Engine:
        if cls.engine is not None:
            return cls.engine

        load_dotenv()

        DB_HOST= os.getenv("MYSQL_HOST")
        DB_USER = os.getenv("MYSQL_USER")
        DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
        DB_NAME = 'flask'
        
        cls.engine = create_engine(
            f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )

        return cls.engine
