from collections import deque

from .constants import Expression, InvalidExpression, Operators


def compute_expression(expression: Expression) -> float:
    stack: deque[Operators | float] = deque()
    expression_as_list = parse_expression(expression)
    for index, token in enumerate(expression_as_list):
        if isinstance(token, float):
            stack.append(token)
        else:
            try:
                ope_2, ope_1 = stack.pop(), stack.pop()
            except IndexError:
                raise InvalidExpression(
                    f"The given expression is not valid. Error detected on token {index + 1}"
                )
            res = _compute_operator(token, ope_1, ope_2)
            stack.append(res)

    if len(stack) > 1:
        raise InvalidExpression(f"Missing {len(stack) - 1} operators")
    return stack.pop()


def parse_expression(expression: Expression) -> list[str | float]:
    if not expression:
        raise InvalidExpression("Empty expression")
    final_list: list[str | float] = []
    for elem in expression.split(" "):
        match elem:
            case "*":
                final_list.append(Operators.MUL)
            case "+":
                final_list.append(Operators.ADD)
            case "/":
                final_list.append(Operators.DIV)
            case "-":
                final_list.append(Operators.MINUS)
            case "**":
                final_list.append(Operators.POW)
            case _:
                try:
                    operande = float(elem)
                except ValueError:
                    raise InvalidExpression(f"Unknow value : {elem}")
                else:
                    final_list.append(operande)

    return final_list


def _compute_operator(operator: str, *operandes):
    op1, op2 = operandes
    match operator:
        case Operators.ADD:
            return op1 + op2
        case Operators.MINUS:
            return op1 - op2
        case Operators.MUL:
            return op1 * op2
        case Operators.DIV:
            return op1 / op2
        case Operators.POW:
            return op1**op2
        case _:
            raise ValueError(f"Invalid operator {operator}")
