from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlmodel import select

from .constants import Expression, InvalidExpression, Settings
from .core import compute_expression
from .database import SessionDep, create_db_and_tables
from .models import Operation, convert_operations_to_csv

settings = Settings()
app = FastAPI()


class ExpressionPayload(BaseModel):
    expression: Expression


@app.post("/compute-expression")
async def compute_expression_endpoint(payload: ExpressionPayload, session: SessionDep):
    try:
        result = compute_expression(payload.expression)
    except InvalidExpression as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    operation = Operation(expression=payload.expression, result=result)
    session.add(operation)
    session.commit()

    return {"result": result}


@app.get("/operations")
async def get_operations(session: SessionDep):
    operations = session.exec(select(Operation)).all()
    response = StreamingResponse(
        iter([convert_operations_to_csv(operations)]), media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=operations.csv"
    return response


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
