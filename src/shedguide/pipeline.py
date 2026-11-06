"""The one place that does extract, plan and parts."""

from dataclasses import dataclass

from shedguide.extract import extract
from shedguide.framing import plan_framing
from shedguide.llm import LLMClient
from shedguide.parts import build_parts
from shedguide.spec import FramingPlan, PartsList, ShedSpec


@dataclass(frozen=True)
class PipelineResult:
    spec: ShedSpec
    plan: FramingPlan
    parts: PartsList


def run_pipeline(chat_line: str, llm: LLMClient) -> PipelineResult:
    # Slice 06 must change this so parts accept only a ConfirmedSpec.
    spec = extract(chat_line, llm)
    plan = plan_framing(spec)
    parts = build_parts(plan)
    return PipelineResult(spec=spec, plan=plan, parts=parts)
