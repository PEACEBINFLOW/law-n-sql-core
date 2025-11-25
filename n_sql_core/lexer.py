from __future__ import annotations
from dataclasses import dataclass
from typing import List, Iterator


@dataclass
class Token:
    type: str
    value: str

    def __repr__(self) -> str:
        return f"Token({self.type!r}, {self.value!r})"


KEYWORDS = {
    "SELECT",
    "FROM",
    "WHERE",
    "AND",
    "IN",
}

SYMBOLS = {
    ",": "COMMA",
    "(": "LPAREN",
    ")": "RPAREN",
    ";": "SEMI",
    "=": "EQ",
    "!": "BANG",
    "<": "LT",
    ">": "GT",
}


def tokenize(query: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(query)

    while i < n:
        ch = query[i]

        # whitespace
        if ch.isspace():
            i += 1
            continue

        # string literal
        if ch == "'":
            i += 1
            start = i
            while i < n and query[i] != "'":
                i += 1
            if i >= n:
                raise ValueError("Unterminated string literal")
            value = query[start:i]
            tokens.append(Token("STRING", value))
            i += 1  # skip closing '
            continue

        # number literal
        if ch.isdigit():
            start = i
            i += 1
            while i < n and (query[i].isdigit() or query[i] == "."):
                i += 1
            value = query[start:i]
            tokens.append(Token("NUMBER", value))
            continue

        # identifiers / keywords
        if ch.isalpha() or ch == "_":
            start = i
            i += 1
            while i < n and (query[i].isalnum() or query[i] in "._"):
                i += 1
            ident = query[start:i]
            upper = ident.upper()
            if upper in KEYWORDS:
                tokens.append(Token(upper, upper))
            else:
                tokens.append(Token("IDENT", ident))
            continue

        # symbols / operators
        if ch in SYMBOLS:
            if ch in ("<", ">", "!") and i + 1 < n and query[i + 1] == "=":
                op = ch + "="
                tokens.append(Token("OP", op))
                i += 2
                continue

            tok_type = SYMBOLS[ch]
            tokens.append(Token(tok_type, ch))
            i += 1
            continue

        raise ValueError(f"Unexpected character in query: {ch!r}")

    return tokens
