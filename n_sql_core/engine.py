from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List

from .ast import SelectQuery, ConditionExpr, Comparison, InExpression, ConditionTerm
from .demo_data import get_demo_routes


@dataclass
class ExecutionResult:
    columns: List[str]
    rows: List[List[Any]]


_ALLOWED_COLUMNS = {
    "device",
    "channel",
    "frequency",
    "g_layer",
    "tower_id",
    "latency_ms",
    "signal_quality",
}


def execute_query(query: SelectQuery) -> ExecutionResult:
    if query.table != "network.routes":
        raise ValueError(f"Only 'network.routes' is supported in this prototype, got {query.table!r}")

    routes = get_demo_routes()

    filtered = [
        row for row in routes
        if query.where is None or _row_matches(row, query.where)
    ]

    if query.columns == ["*"]:
        columns = sorted(_ALLOWED_COLUMNS)
    else:
        for col in query.columns:
            if col not in _ALLOWED_COLUMNS:
                raise ValueError(f"Unknown column in SELECT: {col}")
        columns = query.columns

    result_rows = [[row[col] for col in columns] for row in filtered]

    return ExecutionResult(columns=columns, rows=result_rows)


def _row_matches(row: Dict[str, Any], cond: ConditionExpr) -> bool:
    return all(_term_matches(row, term) for term in cond.terms)


def _term_matches(row: Dict[str, Any], term: ConditionTerm) -> bool:
    if isinstance(term, Comparison):
        value = row.get(term.field)
        op = term.op
        target = term.value

        if op == "=":
            return value == target
        if op == "!=":
            return value != target
        if op == "<":
            return value < target
        if op == "<=":
            return value <= target
        if op == ">":
            return value > target
        if op == ">=":
            return value >= target

        raise ValueError(f"Unsupported operator: {op}")

    if isinstance(term, InExpression):
        value = row.get(term.field)
        return value in term.values

    raise TypeError(f"Unknown condition term type: {type(term)}")
