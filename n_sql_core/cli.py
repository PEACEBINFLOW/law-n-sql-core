from __future__ import annotations

import sys
from textwrap import indent

from .parser import parse_query
from .engine import execute_query, ExecutionResult


def format_table(result: ExecutionResult) -> str:
    if not result.rows:
        return "(no rows)"

    col_widths = [len(col) for col in result.columns]

    for row in result.rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def fmt_row(values) -> str:
        cells = [
            str(v).ljust(col_widths[i]) for i, v in enumerate(values)
        ]
        return " | ".join(cells)

    lines = [
        fmt_row(result.columns),
        "-+-".join("-" * w for w in col_widths),
    ]
    for row in result.rows:
        lines.append(fmt_row(row))

    return "\n".join(lines)


def run_query(q: str) -> None:
    try:
        ast = parse_query(q)
        res = execute_query(ast)
        print(format_table(res))
    except Exception as e:
        print("Error:", e, file=sys.stderr)


def repl() -> None:
    print("N-SQL REPL (Law-N prototype)")
    print("Type a query and press Enter. Ctrl+C or Ctrl+D to exit.\n")

    while True:
        try:
            line = input("n-sql> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        run_query(line)


def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        run_query(query)
    else:
        repl()


if __name__ == "__main__":
    main()
