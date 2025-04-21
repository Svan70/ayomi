from typing import Optional

from sqlmodel import Field, SQLModel


class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    expression: str
    result: float  # Could be a dedicated model, but is stored here for simplicity
