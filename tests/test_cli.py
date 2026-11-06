import io

from shedguide import cli, config
from shedguide.llm import LLMClient
from shedguide.pipeline import PipelineResult
from shedguide.tables import OutOfRangeError


def test_T17_cli_prints_parts_row_disclaimer_marker() -> None:
    out = io.StringIO()
    assert cli.main(input_fn=lambda _: "a 10x12 shed", out=out) == 0
    text = out.getvalue()
    assert "Floor joist" in text
    assert "STUB-1" in text
    assert config.DISCLAIMER in text
    assert "STUB DATA" in text


def test_T18_cli_empty_line_and_pipeline_error() -> None:
    calls: list[str] = []

    def spy(line: str, llm: LLMClient) -> PipelineResult:
        calls.append(line)
        raise OutOfRangeError("too wide")

    out = io.StringIO()
    assert cli.main(input_fn=lambda _: "   ", out=out, pipeline=spy) == 1
    assert calls == []
    assert out.getvalue().strip()

    out = io.StringIO()
    assert cli.main(input_fn=lambda _: "big shed", out=out, pipeline=spy) == 1
    assert "too wide" in out.getvalue()
    assert "Traceback" not in out.getvalue()
