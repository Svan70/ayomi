from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .constants import Expression, InvalidExpression
from .core import compute_expression

app = FastAPI()


class ExpressionPayload(BaseModel):
    expression: Expression


@app.post("/compute-expression")
async def compute_expression_endpoint(payload: ExpressionPayload):
    try:
        result = compute_expression(payload.expression)
    except InvalidExpression as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {"result": result}
