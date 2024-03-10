from datetime import datetime
from app.database.models.base import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column


class CityAssociatedWithUser(Base):
    id = mapped_column("ID", Integer, primary_key=True)
    user_id = mapped_column("USER_ID", ForeignKey("USERS.ID"), primary_key=True)
    name = mapped_column("NAME", String(255), nullable=False)
    country = mapped_column("COUNTRY", String(255), nullable=False)
    __tablename__ = "CITY"

    def __init__(self, **kw):
        current_time = datetime.now()

        kwargs = {key: value for key, value in kw.items() if key in self.__dir__()}

        super().__init__(**kwargs, created_at=current_time, updated_at=current_time)
