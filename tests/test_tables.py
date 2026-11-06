import pytest

from shedguide.config import STUB_TABLE
from shedguide.tables import JoistRow, OutOfRangeError, load_joist_table, lookup_joist


def test_T7_stub_csv_loads_one_typed_row() -> None:
    rows = load_joist_table()
    assert rows == [JoistRow(row_id="STUB-1", joist_size="2x8", spacing_in=16, max_span_ft=10)]


def test_T8_lookup_above_max_span_raises() -> None:
    with pytest.raises(OutOfRangeError):
        lookup_joist(10.5)


def test_T9_lookup_at_max_ok_and_none_raises() -> None:
    assert lookup_joist(10).row_id == "STUB-1"
    with pytest.raises(OutOfRangeError):
        lookup_joist(None)


def test_T10_stub_has_provenance_note_saying_fake() -> None:
    note = STUB_TABLE.with_suffix(".md")
    assert note.exists()
    assert "fake" in STUB_TABLE.read_text().splitlines()[0].lower()
    assert "fake" in note.read_text().splitlines()[0].lower()
