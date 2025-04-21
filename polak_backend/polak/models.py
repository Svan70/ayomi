import csv
import io
from typing import Optional

from sqlmodel import Field, SQLModel


class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    expression: str
    result: float  # Could be a dedicated model, but is stored here for simplicity

    # Put here for simplicity, but could be moved to a dedicated class,
    # to separate model from its serialization
    @classmethod
    def csv_header(cls) -> list[str]:
        return ["id", "expression", "result"]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "expression": self.expression,
            "result": self.result,
        }


def convert_operations_to_csv(operations: list[Operation]) -> str:
    csv_header = Operation.csv_header()
    csv_output = io.StringIO()
    rows = [op.to_dict() for op in operations]
    writer = csv.DictWriter(csv_output, fieldnames=csv_header, delimiter=";")
    writer.writeheader()
    writer.writerows(rows)
    return csv_output.getvalue()
