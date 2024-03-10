from app.database.models.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from datetime import datetime

class User(Base):
    id = mapped_column("ID", Integer, primary_key=True)
    uuid = mapped_column("UUID", String(255), nullable=False, unique=True)
    username = mapped_column("username", String(255), nullable=False)

    __tablename__ = "USERS"

    def __init__(self, **kw):
        current_time = datetime.now()

        kwargs = {key: value for key, value in kw.items() if key in self.__dir__()}

        super().__init__(**kwargs, created_at=current_time, updated_at=current_time)
