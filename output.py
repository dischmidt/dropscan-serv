import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List

import click
from rich.console import Console
from rich.table import Table
from tabulate import tabulate


class OutputHandler:
    def __init__(self) -> None:
        raw_format = os.getenv("FORMATTNG") or os.getenv("FORMATTING") or "rich"
        self.format = raw_format.strip().lower()
        if self.format not in {"json", "rich", "txt", "markdown"}:
            raise click.ClickException(
                "Invalid output format in FORMATTNG/FORMATTING. "
                "Use one of: json, rich, txt, markdown."
            )
        self.console = Console()

    def message(self, text: str) -> None:
        if self.format == "rich":
            self.console.print(text)
            return
        click.echo(text)

    def warn(self, text: str) -> None:
        self.message(f"WARNING: {text}")

    def table(self, rows: List[Dict[str, Any]]) -> None:
        if not rows:
            self.message("No results.")
            return

        columns = list(rows[0].keys())

        if self.format == "json":
            click.echo(json.dumps(rows, indent=2, default=str))
            return

        if self.format == "rich":
            table = Table(show_header=True, header_style="bold cyan")
            for col in columns:
                table.add_column(col)
            for row in rows:
                table.add_row(*(self._stringify(row.get(col)) for col in columns))
            self.console.print(table)
            return

        tablefmt = "simple" if self.format == "txt" else "github"
        matrix = [[self._stringify(row.get(col)) for col in columns] for row in rows]
        click.echo(tabulate(matrix, headers=columns, tablefmt=tablefmt))

    def detail(self, data: Dict[str, Any]) -> None:
        if self.format == "json":
            click.echo(json.dumps(data, indent=2, default=str))
            return

        if self.format == "rich":
            table = Table(show_header=False)
            table.add_column("field", style="bold cyan")
            table.add_column("value")
            for key, value in data.items():
                table.add_row(str(key), self._stringify(value))
            self.console.print(table)
            return

        if self.format == "markdown":
            rows = [[k, self._stringify(v)] for k, v in data.items()]
            click.echo(tabulate(rows, headers=["field", "value"], tablefmt="github"))
            return

        for key, value in data.items():
            click.echo(f"{key}: {self._stringify(value)}")

    def save_binary(self, data: bytes, path: str | None, default_name: str) -> str:
        target = Path(path) if path else Path(default_name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        self.message(f"Saved file to: {target}")
        return str(target)

    @staticmethod
    def _stringify(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (dict, list, tuple, set)):
            return json.dumps(value, default=str)
        return str(value)


output = OutputHandler()
