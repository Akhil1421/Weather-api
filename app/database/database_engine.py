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

        DB_URI= os.getenv("DB_URI")

        cls.engine = create_engine(
            f"{DB_URI}"
        )

        return cls.engine
