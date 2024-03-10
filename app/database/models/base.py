from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    created_at = mapped_column("CREATED_AT", DateTime, nullable=False)
    updated_at = mapped_column("UPDATED_AT", DateTime, nullable=False)
