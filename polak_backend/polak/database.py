from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from .constants import Settings

settings = Settings()

connect_args = {"check_same_thread": False}
engine = create_engine(settings.db_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if settings.test_env:
    # Ensure the test DB is always set up correctly
    # The following function won't erase data
    create_db_and_tables()
