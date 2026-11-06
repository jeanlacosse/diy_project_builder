"""LLM client interface and a fake. No boto3, no network."""

from typing import Any, Protocol

CANNED_PAYLOAD: dict[str, Any] = {
    "content": [
        {
            "toolUse": {
                "name": "record_shed_spec",
                "input": {"project_type": "shed", "width_ft": 10.0, "length_ft": 12.0},
            }
        }
    ]
}


class LLMClient(Protocol):
    def extract_spec(self, chat_line: str) -> dict[str, Any]:
        """Return a tool-use-shaped payload for the chat line."""
        ...


class FakeLLM:
    """Returns the same canned payload for any input."""

    model_id = "fake-model"

    def extract_spec(self, chat_line: str) -> dict[str, Any]:
        return CANNED_PAYLOAD
