# Spec 01: Walking skeleton

_Status: approved_ · _Last updated: 2026-11-05_
Backlog row: 01 · Depends on: none · Size: M · Type: build

## Outcome
`uv run shedguide` reads one typed chat line, a fake LLM returns a canned `ShedSpec`, a stub 1-row table gives a `FramingPlan`, and a joist parts list prints with the planning-aid disclaimer and a loud "STUB DATA" marker. `uv run python -m shedguide.evals` runs one canned case through the same pipeline function and writes a results file. `pytest`, `ruff check`, `ruff format --check` and `mypy` are configured and pass. No Bedrock, no network, no real tables: this slice only proves the wiring.

## Before you start (pre-work check)
- [x] No dependencies (slice 01 has none).
- [ ] The backlog note says to record the "walking skeleton before the spike" ordering with `/gw-decide` before building. Do that first (it is not a spec task).
- [ ] The repo has no `pyproject.toml`, `src/`, `tests/`, `data/` or `evals/` yet (checked 2026-11-05). If any exist, stop and re-check Scope.

## Requirements
| ID | Requirement |
|---|---|
| R1 | The project is a uv-managed Python 3.13 package `shedguide` under `src/shedguide/`, with a `shedguide` console script (entry point `shedguide.cli:run`, a thin wrapper that exits with the code from `main()`), and the four DESIGN.md check commands run and pass. |
| R2 | `spec.py` defines `ShedSpec` (every field Optional, default `None`, so a missing value is never a guess), `FramingPlan` and `PartsList` as Pydantic models. `ShedSpec` has only placeholder fields: `project_type`, `width_ft`, `length_ft`. Slice 04 replaces them with the real envelope. |
| R3 | `llm.py` defines an `LLMClient` interface and a `FakeLLM` that returns a canned tool-use-shaped payload. It imports no `boto3` and makes no network call. |
| R4 | `extract.py` turns a chat line into a `ShedSpec` using an `LLMClient`. The payload is validated by Pydantic; an invalid payload raises `ExtractionError`, never a partial spec. |
| R5 | `tables.py` loads `data/tables/stub_joists.csv` into typed rows and raises `OutOfRangeError` for a missing value or a span above the table's range. |
| R6 | The stub table is one row, has a sibling `.md` provenance note, and both state in their first lines that the values are fake and not from any reference. |
| R7 | `framing.py` derives a `FramingPlan` (joist size, spacing, joist count, and the table row it came from) from a `ShedSpec` by table lookup only. |
| R8 | `parts.py` turns a `FramingPlan` into a `PartsList` (item, stock size, stock length, quantity, cut length), choosing the shortest stock length from `data/stock.csv` that covers the cut. |
| R9 | `pipeline.py` has one function, `run_pipeline(chat_line, llm)`, that does extract, plan and parts. The CLI and the eval runner both call it and nothing else does this work. |
| R10 | The CLI reads one chat line, prints the parts list, the table row it used, the disclaimer and the STUB DATA marker. An empty line prints a message and exits non-zero without calling the pipeline. A pipeline error prints a plain message and exits non-zero. |
| R11 | `python -m shedguide.evals` loads `evals/cases/canned.jsonl` (one case), runs it through `run_pipeline` with `FakeLLM`, and writes a JSON results file to `evals/results/` with prompt version, model ID (the fake's), date, and the case outcome. |
| R12 | Unit tests make no network calls and every test name includes its T-ID. |

## Scope
| Component / file | Change | Notes |
|---|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore` | new | ruff, mypy (strict on `src`), pytest config. `.gitignore` covers `.env`, `.venv`, caches |
| `src/shedguide/__init__.py`, `config.py` | new | `config.py`: model ID placeholder `fake-model`, prompt version `skeleton-0`, disclaimer text, paths |
| `src/shedguide/spec.py` | new | R2 |
| `src/shedguide/llm.py` | new | R3 |
| `src/shedguide/extract.py` | new | R4 |
| `src/shedguide/tables.py` | new | R5 |
| `src/shedguide/framing.py` | new | R7 |
| `src/shedguide/parts.py` | new | R8 |
| `src/shedguide/pipeline.py` | new | R9 |
| `src/shedguide/cli.py` | new | R10. `main()` takes injectable input and output so tests need no subprocess |
| `src/shedguide/evals/__init__.py`, `__main__.py`, `runner.py` | new | R11 |
| `data/tables/stub_joists.csv`, `stub_joists.md` | new | R5, R6 |
| `data/stock.csv` | new | Stub stock lengths for R8. Not in `data/tables/`, so the future provenance data check does not apply |
| `evals/cases/canned.jsonl` | new | One case: id, split `dev`, chat input, expected spec, expected plan |
| `tests/test_*.py` | new | See Tests |

**Out of scope:**
- Any real LLM call, boto3, AWS setup, cost logging (slice 03).
- Real span tables, the real envelope, real `ShedSpec` fields (slices 02, 04, 07a).
- Validator, `ConfirmedSpec` and the confirm gate (slices 06, 10). Here `parts` takes a `FramingPlan` straight from the pipeline; slice 06 must change the pipeline so parts accept only a `ConfirmedSpec`.
- Scorers, held-out guard and run counter (slices 04, 07a, 09, 10). The runner here only runs and records the one case.
- Property checks on parts (slice 07b), stud and rafter members, ask/refuse behaviour.
- Streamlit and any UI (decision 008).

**Do not touch:** `docs/groundwork/DESIGN.md`, `docs/groundwork/IDEA.md`, decisions 001 to 008, `groundwork/`, `PROJECT.md`, `notes.md`. (Slice 01 adds files only and edits nothing existing, apart from the BACKLOG row on approval.)

## Approach
Follow the DESIGN.md component layout and paths exactly ([001](../decisions/001-python-pydantic-uv.md) toolchain; [005](../decisions/005-own-eval-harness.md) harness shape; [006](../decisions/006-csv-span-tables.md) CSV plus provenance note). The LLM is behind a small interface so `FakeLLM` and the future Bedrock client are interchangeable. The fake returns the same payload shape the Bedrock tool-use path will, so extraction validates it the same way. Deterministic code only sees a validated `ShedSpec`. The stub table has one row (a made-up joist size, spacing and max span) so lookup, the out-of-range path and row provenance all exist; its `.md` and every CLI output say the data is fake. Parts: joists run across the width, count = `ceil(length / spacing) + 1`. These formulas are skeleton placeholders, not framing rules, and slice 07a/07b replace them (assumption A1).

Assumptions to confirm at approval:
- A1: The skeleton's joist-count and cut-length formulas are placeholders, flagged in code comments, and get replaced with real ones in 07a/07b.
- A2: Results files go in `evals/results/` and are named by date and prompt version. Later slices commit them.

## Tasks
| # | Task | Files | Done when |
|---|---|---|---|
| 1 | Scaffold the package and tooling | `pyproject.toml`, `.python-version`, `.gitignore`, `src/shedguide/__init__.py`, `config.py`, `tests/test_smoke.py` | `uv sync` works; all four check commands pass on the empty package (T1) |
| 2 | Models | `spec.py`, `tests/test_spec.py` | T2, T3 pass |
| 3 | LLM interface, fake, extractor | `llm.py`, `extract.py`, `tests/test_extract.py` | T4, T5, T6 pass |
| 4 | Stub data and table loader | `data/tables/stub_joists.csv`, `.md`, `tables.py`, `tests/test_tables.py` | T7, T8, T9, T10 pass |
| 5 | Planner and parts | `framing.py`, `parts.py`, `data/stock.csv`, `tests/test_framing.py`, `tests/test_parts.py` | T11, T12, T13, T14 pass |
| 6 | Pipeline and CLI | `pipeline.py`, `cli.py`, `tests/test_pipeline.py`, `tests/test_cli.py` | T15, T16, T17, T18 pass; `uv run shedguide` works by hand |
| 7 | Eval runner and canned case | `evals/__init__.py`, `__main__.py`, `runner.py`, `evals/cases/canned.jsonl`, `tests/test_evals_runner.py` | T19, T20, T21 pass; `uv run python -m shedguide.evals` writes a results file by hand |
| 8 | Full check run and no-network guard | `tests/conftest.py` | T22 passes; all four DESIGN.md checks pass |

## Tests
| Test ID | Covers | Kind | What it asserts |
|---|---|---|---|
| T1 | R1 | happy | The `shedguide` console script entry point resolves to `cli.run`, and the package imports on Python 3.13 |
| T2 | R2 | happy | A `ShedSpec` built with no arguments has every field `None` |
| T3 | R2 | unhappy | A `ShedSpec` rejects a wrong type (e.g. `width_ft="abc"`) and a negative width |
| T4 | R3 | happy | `FakeLLM` returns the same canned payload for any input, and the payload validates as a `ShedSpec` |
| T5 | R4 | happy | `extract("a 10x12 shed", FakeLLM())` returns the canned `ShedSpec` |
| T6 | R4 | unhappy | A fake client returning an invalid payload (wrong type, missing tool block) makes `extract` raise `ExtractionError` |
| T7 | R5 | happy | Loading the stub CSV returns one typed row with the expected fields |
| T8 | R5 | unhappy | Lookup for a span above the row's max span raises `OutOfRangeError` |
| T9 | R5 | edge | Lookup at exactly the max span succeeds; lookup with span `None` raises `OutOfRangeError` |
| T10 | R6 | happy | The stub CSV has a sibling `.md`, and both begin with a "fake / not from a reference" statement |
| T11 | R7 | happy | The canned spec gives the expected `FramingPlan`, including the table row ID |
| T12 | R7 | unhappy | A spec with `width_ft=None` raises `OutOfRangeError`; a spec wider than the table range raises it too |
| T13 | R8 | happy | The plan from T11 gives the expected parts list, with the shortest stock length that covers the cut |
| T14 | R8 | edge | A cut longer than the longest stock length raises an error rather than producing an uncovered part; a cut equal to a stock length uses that length with zero waste |
| T15 | R9 | happy | `run_pipeline("...", FakeLLM())` returns the spec, plan and parts list |
| T16 | R9 | unhappy | An `ExtractionError` or `OutOfRangeError` inside the pipeline propagates as its own type (not swallowed, not a bare `Exception`) |
| T17 | R10 | happy | `cli.main` with a typed line prints the parts list, table row, disclaimer text and STUB DATA marker, and returns 0 |
| T18 | R10 | unhappy | An empty or whitespace-only line prints a message, returns non-zero, and the pipeline is not called; a pipeline error prints a plain message with no traceback and returns non-zero |
| T19 | R11 | happy | The runner loads `canned.jsonl`, runs the case through `run_pipeline`, and the case plan matches its expected plan |
| T20 | R11 | happy | The runner writes a results JSON containing prompt version, model ID, date and the case outcome (into a temp directory in the test) |
| T21 | R11 | unhappy | A malformed or empty cases file makes the runner exit non-zero with a plain message and write no results file |
| T22 | R12 | integration | A conftest guard makes any socket connection fail the test run; the whole suite passes with it on. Reason: it is the only way to show "no network" for all tests at once without per-test faking |

## Done when
- [ ] Every requirement has a passing test that asserts it.
- [ ] All DESIGN.md check commands pass (`uv run pytest`, `uv run ruff check .`, `uv run mypy src`, `uv run ruff format --check .`).
- [ ] `uv run shedguide` and `uv run python -m shedguide.evals` both work by hand, and the results file is written.
- [ ] No files outside Scope were changed.
- [ ] The ordering decision (skeleton before spike) is recorded with `/gw-decide`.

## Review notes
Self-check (no `--deep` review): every R1 to R12 has at least one T; every task's files appear in Scope; nothing contradicts DESIGN.md's component layout or decisions 001 to 008. Not independently reviewed. The slice handles no user input beyond one typed line, no auth, money or external files, so `--deep` is not recommended.

## Check result
2026-11-05: **READY**. Re-check after R1/T1 were amended for Python 3.13 and `cli:run` (decision 010).

Check commands: `uv run pytest` 22 passed, `uv run ruff check .` pass, `uv run ruff format --check .` pass, `uv run mypy src` pass.

| R | Status | Evidence |
|---|---|---|
| R1 | met | T1; `requires-python >=3.13`, script `shedguide.cli:run`, all four checks pass |
| R2 | met | T2, T3 |
| R3 | met | T4 |
| R4 | met | T5, T6 |
| R5 | met | T7, T8, T9 |
| R6 | met | T10 |
| R7 | met | T11, T12 |
| R8 | met | T13, T14 |
| R9 | met | T15, T16 |
| R10 | met | T17, T18 |
| R11 | met | T19, T20, T21 |
| R12 | met | T22 |

Blockers: none. The first check (earlier today) was NOT READY only because R1/T1 said Python 3.12 and `cli.main`.

Notes (not blocking): `evals/results/2026-11-05_skeleton-0.json` has no Scope row (A2 covers it); `pyproject.toml` adds hatchling and a pytest `pythonpath` setting not named in DESIGN.md; `import sys` sits inside `cli.main`; T21 may not assert the printed message; the Do-not-touch list now uses the `docs/groundwork/` path; decision 001, DESIGN.md and spec 01 were edited with the owner's approval (decision 010).
