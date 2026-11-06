from typing import Any

import pytest

from shedguide.extract import ExtractionError, extract
from shedguide.llm import CANNED_PAYLOAD, FakeLLM
from shedguide.spec import ShedSpec


class BadLLM:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def extract_spec(self, chat_line: str) -> dict[str, Any]:
        return self.payload


def test_T4_fakellm_same_payload_and_validates() -> None:
    llm = FakeLLM()
    assert llm.extract_spec("a") == llm.extract_spec("something else") == CANNED_PAYLOAD
    tool_input = CANNED_PAYLOAD["content"][0]["toolUse"]["input"]
    assert ShedSpec.model_validate(tool_input)


def test_T5_extract_returns_canned_spec() -> None:
    spec = extract("a 10x12 shed", FakeLLM())
    assert spec == ShedSpec(project_type="shed", width_ft=10.0, length_ft=12.0)


def test_T6_extract_raises_on_invalid_payload() -> None:
    wrong_type = {"content": [{"toolUse": {"name": "x", "input": {"width_ft": "abc"}}}]}
    no_tool = {"content": [{"text": "hello"}]}
    for payload in (wrong_type, no_tool, {}):
        with pytest.raises(ExtractionError):
            extract("x", BadLLM(payload))
