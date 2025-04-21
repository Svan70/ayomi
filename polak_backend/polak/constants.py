from enum import StrEnum

from pydantic_settings import BaseSettings


class Operators(StrEnum):
    ADD = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    POW = "**"


type Expression = str


class InvalidExpression(Exception):
    pass

class Settings(BaseSettings):
    db_url: str = f"sqlite:///test_database.db" # Default value for testing
