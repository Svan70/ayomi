from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .constants import Expression, InvalidExpression, Settings
from .core import compute_expression
from .database import SessionDep
from .models import Operation

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
