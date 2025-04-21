from enum import StrEnum


class Operators(StrEnum):
    ADD = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    POW = "**"


type Expression = str


class InvalidExpression(Exception):
    pass
