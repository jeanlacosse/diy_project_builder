"""Chat line to validated ShedSpec."""

from pydantic import ValidationError

from shedguide.llm import LLMClient
from shedguide.spec import ShedSpec


class ExtractionError(Exception):
    """The LLM payload was not a valid ShedSpec."""


def extract(chat_line: str, llm: LLMClient) -> ShedSpec:
    payload = llm.extract_spec(chat_line)
    try:
        blocks = payload["content"]
        tool_input = next(b["toolUse"]["input"] for b in blocks if "toolUse" in b)
        return ShedSpec.model_validate(tool_input)
    except (KeyError, TypeError, StopIteration, ValidationError) as exc:
        raise ExtractionError(f"Could not read a valid spec from the model output: {exc}") from exc
