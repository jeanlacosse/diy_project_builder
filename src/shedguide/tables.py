"""Load CSV span tables. Raises OutOfRangeError rather than guessing."""

import csv
from pathlib import Path

from pydantic import BaseModel

from shedguide.config import STUB_TABLE


class OutOfRangeError(Exception):
    """A value is missing or outside the table's range."""


class JoistRow(BaseModel):
    row_id: str
    joist_size: str
    spacing_in: float
    max_span_ft: float


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def load_joist_table(path: Path = STUB_TABLE) -> list[JoistRow]:
    return [JoistRow.model_validate(r) for r in read_csv_rows(path)]


def lookup_joist(span_ft: float | None, rows: list[JoistRow] | None = None) -> JoistRow:
    """Return the first row whose max span covers span_ft."""
    if span_ft is None:
        raise OutOfRangeError("Span is missing, so no table row can be chosen.")
    table = rows if rows is not None else load_joist_table()
    for row in sorted(table, key=lambda r: r.max_span_ft):
        if span_ft <= row.max_span_ft:
            return row
    raise OutOfRangeError(f"A span of {span_ft} ft is beyond the table's range.")
