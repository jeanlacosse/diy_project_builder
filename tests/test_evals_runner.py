import json
from pathlib import Path

from shedguide import config
from shedguide.evals import runner


def test_T19_runner_runs_canned_case_and_plan_matches() -> None:
    cases = runner.load_cases(config.CANNED_CASES)
    (outcome,) = runner.run_cases(cases)
    assert outcome["plan_match"] is True


def test_T20_runner_writes_results_file(tmp_path: Path) -> None:
    assert runner.main(config.CANNED_CASES, tmp_path) == 0
    (f,) = list(tmp_path.glob("*.json"))
    data = json.loads(f.read_text())
    assert data["prompt_version"] == config.PROMPT_VERSION
    assert data["model_id"] == "fake-model"
    assert data["date"]
    assert data["cases"][0]["plan_match"] is True


def test_T21_malformed_or_empty_cases_exit_nonzero(tmp_path: Path) -> None:
    results = tmp_path / "results"
    for name, content in (("empty.jsonl", ""), ("bad.jsonl", "{not json")):
        p = tmp_path / name
        p.write_text(content)
        assert runner.main(p, results) == 1
    assert not results.exists()
