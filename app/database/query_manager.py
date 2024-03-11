import sqlalchemy.exc
from sqlalchemy.orm import Session
from sqlalchemy import delete, update

from app.database.database_engine import DatabaseEngine
from app.database.models.base import Base
from app.database.models.user import User
from app.database.models.city import CityAssociatedWithUser


database_engine = DatabaseEngine.create_mysql_db_engine()
Base.metadata.create_all(database_engine)

def insert_single_object(db_object) -> None:
    with Session(database_engine) as session:
        try:
            session.merge(db_object)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(f"Error in inserting object to database. {e.args}")
            raise e

def query_with_filter(model, filters):
    with Session(database_engine) as session:
        try:
            result = session.query(model).filter(filters).one_or_none()
            value = result

            session.expunge_all()
            session.commit()

        except Exception as e:
            print(
                f"No object found in database for model={model} and filter={filter}. Error = {e.args}"
            )
            return None

    return value

def query_all_with_filter(model, filters):
    with Session(database_engine) as session:
        try:
            result = session.query(model).filter(filters).all()
            value = result

            session.expunge_all()
            session.commit()

        except Exception as e:
            print(
                f"No object found in database for model={model} and filter={filter}. Error = {e.args}"
            )
            return None

    return value

def update_objects(model, filters, updates):
    with Session(database_engine) as session:
        try:
            statement = update(model).where(filters).values(updates)
            result = session.execute(statement)
            session.commit()

            return result.rowcount
        except Exception as e:
            print(f"Error in updating objects in the database. {e.args}")
            raise e

def delete_objects(model, filters):
    with Session(database_engine) as session:
        try:
            statement = delete(model).where(filters)
            result = session.execute(statement)
            session.commit()
        except Exception as e:
            print(f"Error in deleting object in the database. {e.args}")
