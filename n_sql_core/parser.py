from __future__ import annotations
from typing import List, Any
from .lexer import tokenize, Token
from .ast import (
    SelectQuery,
    ConditionExpr,
    Comparison,
    InExpression,
    ConditionTerm,
)


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token | None:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def match(self, *types: str) -> Token:
        tok = self.current()
        if tok is None or tok.type not in types:
            expected = " or ".join(types)
            raise ValueError(f"Expected {expected}, got {tok}")
        self.pos += 1
        return tok

    def accept(self, *types: str) -> Token | None:
        tok = self.current()
        if tok is not None and tok.type in types:
            self.pos += 1
            return tok
        return None

    # ---- entry ----

    def parse_query(self) -> SelectQuery:
        self.match("SELECT")
        columns = self.parse_column_list()
        self.match("FROM")
        table_tok = self.match("IDENT")
        table = table_tok.value

        where_expr: ConditionExpr | None = None
        if self.accept("WHERE"):
            where_expr = self.parse_condition_expr()

        # optional semicolon
        self.accept("SEMI")

        return SelectQuery(columns=columns, table=table, where=where_expr)

    # ---- columns ----

    def parse_column_list(self) -> List[str]:
        tok = self.current()
        if tok is None:
            raise ValueError("Unexpected end of input in column list")

        if tok.type == "OP" and tok.value == "*":
            self.pos += 1
            return ["*"]

        columns: List[str] = []
        ident = self.match("IDENT")
        columns.append(ident.value)

        while self.accept("COMMA"):
            ident = self.match("IDENT")
            columns.append(ident.value)

        return columns

    # ---- conditions ----

    def parse_condition_expr(self) -> ConditionExpr:
        terms: List[ConditionTerm] = [self.parse_condition_term()]
        while self.accept("AND"):
            terms.append(self.parse_condition_term())
        return ConditionExpr(terms=terms)

    def parse_condition_term(self) -> ConditionTerm:
        field_tok = self.match("IDENT")
        field = field_tok.value

        # IN (...)
        if self.accept("IN"):
            self.match("LPAREN")
            values: List[Any] = [self.parse_value()]
            while self.accept("COMMA"):
                values.append(self.parse_value())
            self.match("RPAREN")
            return InExpression(field=field, values=values)

        # comparator
        op_tok = self.accept("OP", "EQ", "LT", "GT")
        if op_tok is None:
            raise ValueError("Expected comparator after field")
        op = op_tok.value
        if op_tok.type == "EQ":
            op = "="
        value = self.parse_value()
        return Comparison(field=field, op=op, value=value)

    # ---- values ----

    def parse_value(self) -> Any:
        tok = self.current()
        if tok is None:
            raise ValueError("Unexpected end of input in value")

        if tok.type == "STRING":
            self.pos += 1
            return tok.value
        if tok.type == "NUMBER":
            self.pos += 1
            if "." in tok.value:
                return float(tok.value)
            return int(tok.value)

        raise ValueError(f"Expected literal value, got {tok}")


def parse_query(query: str) -> SelectQuery:
    tokens = tokenize(query)
    parser = Parser(tokens)
    return parser.parse_query()
