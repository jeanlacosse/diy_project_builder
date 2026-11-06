from typing import Any

import pytest

from shedguide.extract import ExtractionError
from shedguide.llm import FakeLLM
from shedguide.pipeline import run_pipeline
from shedguide.tables import OutOfRangeError


class Fixed:
    def __init__(self, tool_input: dict[str, Any]) -> None:
        self.tool_input = tool_input

    def extract_spec(self, chat_line: str) -> dict[str, Any]:
        return {"content": [{"toolUse": {"name": "x", "input": self.tool_input}}]}


def test_T15_pipeline_returns_spec_plan_parts() -> None:
    r = run_pipeline("a shed", FakeLLM())
    assert r.spec.width_ft == 10.0
    assert r.plan.table_row_id == "STUB-1"
    assert r.parts.items


def test_T16_errors_propagate_as_own_type() -> None:
    with pytest.raises(ExtractionError):
        run_pipeline("x", Fixed({"width_ft": "abc"}))
    with pytest.raises(OutOfRangeError):
        run_pipeline("x", Fixed({"width_ft": 30, "length_ft": 12}))
