from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Union, Any


@dataclass
class SelectQuery:
    columns: List[str]  # ["*"] or specific column names
    table: str          # e.g. "network.routes"
    where: "ConditionExpr | None"


# ---- Conditions ----

Comparator = Literal["=", "!=", "<", "<=", ">", ">="]


@dataclass
class Comparison:
    field: str
    op: Comparator
    value: Any


@dataclass
class InExpression:
    field: str
    values: List[Any]


ConditionTerm = Union[Comparison, InExpression]


@dataclass
class ConditionExpr:
    # Simple AND-only expression: term AND term AND term ...
    terms: List[ConditionTerm]
