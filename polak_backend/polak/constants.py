from enum import StrEnum


class Operators(StrEnum):
    ADD = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    POW = "**"


Expression = type[str]
