"""
n_sql_core

Core prototype implementation of N-SQL, the Law-N network-native query language.
"""

from .parser import parse_query
from .engine import execute_query, ExecutionResult

__all__ = [
    "parse_query",
    "execute_query",
    "ExecutionResult",
]
