"""Command line entry point. Input and output are injectable for tests."""

from collections.abc import Callable
from typing import TextIO

from shedguide import config
from shedguide.extract import ExtractionError
from shedguide.llm import FakeLLM, LLMClient
from shedguide.parts import StockError
from shedguide.pipeline import PipelineResult, run_pipeline
from shedguide.tables import OutOfRangeError


def _format(result: PipelineResult) -> str:
    plan = result.plan
    lines = [config.STUB_MARKER, "", "Parts list:"]
    for p in result.parts.items:
        lines.append(
            f"  {p.quantity} x {p.item}: {p.stock_size}, buy {p.stock_length_ft:g} ft stock, "
            f"cut to {p.cut_length_ft:g} ft"
        )
    lines += [
        "",
        f"Table row used: {plan.table_row_id} ({plan.joist_size} at {plan.spacing_in:g} in "
        f"spacing, span {plan.span_ft:g} ft)",
        "",
        config.DISCLAIMER,
        config.STUB_MARKER,
    ]
    return "\n".join(lines)


def main(
    input_fn: Callable[[str], str] = input,
    out: TextIO | None = None,
    llm: LLMClient | None = None,
    pipeline: Callable[[str, LLMClient], PipelineResult] = run_pipeline,
) -> int:
    import sys

    stream = out if out is not None else sys.stdout
    client: LLMClient = llm if llm is not None else FakeLLM()
    try:
        line = input_fn("Describe your shed: ").strip()
    except EOFError:
        line = ""
    if not line:
        print("Please type a description of your shed.", file=stream)
        return 1
    try:
        result = pipeline(line, client)
    except (ExtractionError, OutOfRangeError, StockError) as exc:
        print(f"Sorry, I couldn't produce a parts list: {exc}", file=stream)
        return 1
    print(_format(result), file=stream)
    return 0


def run() -> None:
    raise SystemExit(main())
