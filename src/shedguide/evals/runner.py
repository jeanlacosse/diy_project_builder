"""Run canned eval cases through run_pipeline and write a results file."""

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from shedguide import config
from shedguide.llm import FakeLLM
from shedguide.pipeline import run_pipeline
from shedguide.spec import FramingPlan, ShedSpec


class CaseFileError(Exception):
    """The cases file is missing, empty or malformed."""


def load_cases(path: Path) -> list[dict[str, Any]]:
    try:
        cases = [json.loads(ln) for ln in path.read_text().splitlines() if ln.strip()]
        for c in cases:
            ShedSpec.model_validate(c["expected_spec"])
            FramingPlan.model_validate(c["expected_plan"])
            c["id"], c["split"], c["input"]  # noqa: B018
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValidationError) as exc:
        raise CaseFileError(f"Bad cases file {path}: {exc}") from exc
    if not cases:
        raise CaseFileError(f"No cases found in {path}")
    return cases


def run_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    llm = FakeLLM()
    outcomes = []
    for c in cases:
        result = run_pipeline(c["input"], llm)
        outcomes.append(
            {
                "id": c["id"],
                "split": c["split"],
                "spec_match": result.spec == ShedSpec.model_validate(c["expected_spec"]),
                "plan_match": result.plan == FramingPlan.model_validate(c["expected_plan"]),
            }
        )
    return outcomes


def main(cases_path: Path = config.CANNED_CASES, results_dir: Path = config.RESULTS_DIR) -> int:
    try:
        cases = load_cases(cases_path)
        outcomes = run_cases(cases)
    except Exception as exc:  # noqa: BLE001
        print(f"Eval run failed: {exc}", file=sys.stderr)
        return 1
    today = date.today().isoformat()
    results = {
        "prompt_version": config.PROMPT_VERSION,
        "model_id": FakeLLM.model_id,
        "date": today,
        "cases": outcomes,
    }
    results_dir.mkdir(parents=True, exist_ok=True)
    out = results_dir / f"{today}_{config.PROMPT_VERSION}.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Wrote {out}")
    return 0 if all(o["plan_match"] and o["spec_match"] for o in outcomes) else 1
