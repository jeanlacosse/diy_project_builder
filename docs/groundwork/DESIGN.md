# Design: AI Build Guide App

_Status: agreed_ · _Last updated: 2026-11-05_ · Built from [IDEA.md](IDEA.md)

## First gate: table-source spike
Q5 (which public reference supplies the tables, and its license), Q6 (supported envelope) and assumptions A3/A4 are unresolved. **The Data and Components sections below are provisional until the spike passes.** The spike is the first slice, time-boxed to about 4 hours. It passes when all of these exist:
- a named reference and its license, checked;
- tables exist in that reference for all three member types (wall studs, floor joists, rafters). If one is missing, narrow the parts scope and reword IDEA criteria 3 and 5 before going on;
- the supported envelope written in one paragraph;
- 5 hand-written eval examples;
- one successful Bedrock tool-use call, confirming the exact Sonnet 5.5 model ID, model access and region (or, if unavailable, the fallback in [007](decisions/007-sonnet-5-5-default-model.md));
- an AWS Budgets alert set.

Decisions [006](decisions/006-csv-span-tables.md) and [007](decisions/007-sonnet-5-5-default-model.md) stay `proposed` until it passes, then become `accepted` (or are superseded). Record the result with `/gw-decide`. Fallback if no source is license-clean: hand-summarized or synthetic tables. Then the "code-checked" claim is reworded to say the tables are the owner's summary of the reference, every row is cross-checked against the source one by one, and the output disclaimer says so.

## Slice 1 order
1. Spike (above).
2. Finalize the envelope. Spike examples may be edited until the freeze.
3. Write all 50 cases, including at least 10 source-derived `FramingPlan`s written **before** the CSV tables are transcribed.
4. Freeze: record the case-file hash.
5. Run the baseline (minimal prompt) on dev, and commit its results file.
6. Tune on dev only.
7. Final numbers: held-out, run only for the baseline and the final (see Conventions).
8. Friend check (assumption A5): one friend installs and runs the CLI on their own machine with their own model credentials; record whether it worked and what broke.

## Overview
A Python pipeline turns a chat into a validated `ShedSpec` (LLM via Bedrock tool use), checks it against the supported envelope, has code derive a `FramingPlan` from deterministic span/size tables, and generates a parts and cut list for framing members in plain code. Slice 2 adds RAG over prose references for citations; slice 3 adds an LLM-written, cited build guide checked against the spec. Slice 1 runs from a CLI or notebook; a Streamlit chat is added later as a thin UI over the pipeline. Evals run from the same pipeline with no UI.

## Scope of the parts list (Artifact #1)
Framing members only: wall studs, floor joists and rafters, with sizes and spacing from the framing plan. Headers, posts, fasteners, sheathing, roofing and foundations are not sized or listed by code; they appear as cited guidance in slice 2 and 3 only.

## Stack
| Layer | Choice | Decision |
|---|---|---|
| Language / runtime | Python 3.12, uv, Pydantic | [001](decisions/001-python-pydantic-uv.md) |
| LLM | Claude Sonnet 5.5 on Amazon Bedrock (boto3 Converse, tool use) | [002](decisions/002-bedrock-llm-access.md), [007](decisions/007-sonnet-5-5-default-model.md) |
| Framework / UI | CLI or notebook for slice 1; Streamlit chat added after the criteria 1-5 numbers exist | [003](decisions/003-streamlit-chat-ui.md), [008](decisions/008-defer-ui-cli-first.md) |
| Storage | Files: CSV tables, JSONL evals; Chroma local index (slice 2 dependency only, not installed before then) | [004](decisions/004-local-vector-store.md), [006](decisions/006-csv-span-tables.md) |
| Evals | Own harness, JSONL cases | [005](decisions/005-own-eval-harness.md) |
| Hosting / packaging | Runs locally. Friends install and run the CLI on their own machines with their own model credentials, so the owner's AWS account is never exposed. No tunnel or public hosting until a password, per-day call cap and an AWS Budgets alert exist | [008](decisions/008-defer-ui-cli-first.md) |

## Components
| Component | Responsibility | Lives in |
|---|---|---|
| Spec schema | `ShedSpec` Pydantic model; the LLM/code contract. Fields are Optional with no defaults, so a missing value is `None`, never a guess. Also `ValidationResult`, `ConfirmedSpec`, `FramingPlan` | `src/shedguide/spec.py` |
| LLM client | Single Bedrock wrapper; fakeable in tests | `src/shedguide/llm.py` |
| Extractor | Chat to `ShedSpec` via tool use; reports which fields are missing | `src/shedguide/extract.py` |
| Tables | Load CSV span/size tables; raise `OutOfRangeError` | `src/shedguide/tables.py`, `data/tables/` |
| Validator | Returns a `ValidationResult` with reasons: **ask** (required field missing), **refuse** (out-of-scope project type, or value outside envelope/table range), **flag** (in range but near a limit or unusual) | `src/shedguide/validate.py` |
| Framing planner | Derives joist, rafter and stud size and spacing from span, loads and species by table lookup; user-requested sizes are notes it checks. If the table requires a larger size than requested, the plan uses the table size and the output carries a flag naming the requested size, the required size and the table row | `src/shedguide/framing.py` |
| Confirm gate | `confirm(spec) -> ConfirmedSpec`; Parts and Guide accept only a `ConfirmedSpec`. The UI prompts the user; evals auto-confirm | `src/shedguide/confirm.py` |
| Parts engine | `ConfirmedSpec` + `FramingPlan` to parts and cut list for framing members; stock-length checks against `data/stock.csv` (available stock sizes and lengths) | `src/shedguide/parts.py`, `data/stock.csv` |
| Parts checks | Property checks run on every eval case: cut lengths cover the required member lengths, waste is never negative, member counts equal the spacing-derived counts, every cut fits a stock length | `src/shedguide/parts_check.py` |
| Retrieval (slice 2) | Chunk, embed, `retrieve(query, k)` over the prose corpus; corpus has a provenance note like the tables | `src/shedguide/retrieval/`, `data/corpus/` |
| Guide (slice 3) | Produces structured `GuideStep`s from the validated spec | `src/shedguide/guide.py` |
| Guide checker (slice 3) | Code check that each step has a citation (a step with none fails), agrees with the spec fields it references, and that any dimension or size in the step text matches the spec or `FramingPlan` (text is scanned, not only the declared fields) | `src/shedguide/guide_check.py` |
| Judge (slice 3, final numbers) | LLM judge for readability only; not built before slice 3 | `src/shedguide/evals/judge.py` |
| Evals | Cases, scorers, run reports, held-out guard | `evals/cases/`, `src/shedguide/evals/` |
| CLI / output | Slice 1 entry point (chat loop and eval runs). Shows the planning-aid disclaimer and the sources for every output | `src/shedguide/cli.py` |
| UI (later) | Streamlit chat after criteria 1-5 numbers exist; no business logic; the Confirm gate prompt moves here | `app.py` |

```
chat -> Extractor --(LLM)--> ShedSpec -> Validator --> ask / refuse / flag
                                  |
                           Confirm gate (UI asks; evals auto-confirm)
                                  v
              Framing planner <- Tables (CSV) -> FramingPlan
                                  v
                            Parts engine -> parts + cut list
                                  v
                    Guide (slice 3) <- Retrieval (slice 2)
```

## Data
- **ShedSpec** (all fields Optional, no defaults): project type, footprint (width, length), wall height, roof style (gable or shed), floor type, door/window openings, load conditions (snow/wind as the few structural fields per Q2), species/grade, requested sizes (notes only), free-form notes. Supported envelope (Q6) is set from the chosen reference tables and recorded in `data/tables/` provenance and in the validator; it is decided in the first spike.
- **FramingPlan** (derived by code, never by the LLM): stud, joist and rafter size and spacing, each with the table row it came from. Eval cases expect a spec plus the plan a table lookup gives, which is what makes criterion 3 a real check.
- **ValidationResult**: outcome (`ok`, `ask`, `refuse`, `flag`) and a list of reasons naming the field or rule.
- **Table rows**: size, spacing, species/grade, max span, with source note.
- **Eval case**: id, split (`dev` or `held-out`), tags (messy, ambiguous, out-of-scope, refusal, friend-written), chat input, expected spec and expected `FramingPlan`, or expected outcome (`ask` or `refuse`) with reason. A subset (at least 5 cases) also carries a hand-computed expected parts list. At least 10 expected `FramingPlan`s are written from the source document, before the CSV is transcribed, so a transcription mistake can't also appear in the gold answer.
- **Scoring (criteria 3 and 4)**: criterion 3 is scored from the gold spec into `FramingPlan` (lookup only); the end-to-end result from chat is reported separately. For criterion 4, an `ask` or `refuse` outcome counts as correct when it matches the case's expected outcome.
- **Retrieval case** (slice 2): id, query, relevant chunk IDs (labeled by the owner). Metric is recall@k with k=5 unless changed; the deliberate before/after change is chunking or a reranker.
- **GuideStep** (slice 3): step text, citations (corpus chunk or table row IDs), referenced spec fields. The guide checker needs these to verify citation presence and spec agreement.
- **Parts list**: item, stock size, stock length, quantity, cuts.
- **Field comparators** (used by the eval scorer):

| Field kind | Rule |
|---|---|
| Dimensions (feet/inches) | Numeric, within ±0.5 in |
| Enums (roof style, floor type, species) | Exact |
| Openings list | Compared as a set; each opening's size by the dimension rule |
| Loads | Numeric, exact unless the reference uses ranges |
| Free-form notes | Ignored |

"Full-spec exact match" means every non-ignored field passes its comparator. Split is 25 `dev` and 25 `held-out` cases, and each split has at least 4 refusal and 4 ask cases. That leaves about 17 extraction cases per split, so a result is noisy: report per-field counts and the spread alongside percentages. The retrieval set (slice 2) has at least 20 queries.

## Integrations
- Amazon Bedrock via boto3, using a personal AWS profile. No work resources. Default model Claude Sonnet 5.5; Haiku 5.5 may be used for dev-split iteration, switched in `config.py`. The embedding model (slice 2) is chosen in the spike or slice 2 spec. The spike confirms exact Bedrock model IDs, model access and region.
- **Budget:** start with a $10 cap. Set an AWS Budgets alarm on the personal account before the first Bedrock call. Raise it deliberately only when needed.
- Public reference documents for tables and corpus (source and license per Q5/A3).

## Check commands
| Purpose | Command |
|---|---|
| Test | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Type check | `uv run mypy src` |
| Format check | `uv run ruff format --check .` |

Unit tests never call Bedrock (the LLM client is faked). Eval runs (`uv run python -m shedguide.evals`) call Bedrock and cost money, so they are run separately and are **not** part of the checks above. The test suite includes a data check: every CSV in `data/tables/` and every corpus file has a provenance `.md` and passes a schema check. Table tests also check monotonicity (a larger member or tighter spacing never allows a shorter span), and the owner re-checks every transcribed row against the source once.

Test naming rule: every test name includes its spec test ID (each slice's spec assigns the T-IDs), for example `test_T3_rejects_joist_span_beyond_table`, so results can be traced back to requirements.

## Conventions
Project-wide rules the build must follow.
- No secrets in source. Config comes from: environment variables and a git-ignored `.env`; AWS auth via the standard boto3 profile chain; model IDs and region in `config.py`.
- `src/shedguide/` layout; tests in `tests/`; data in `data/`.
- Deterministic code never trusts raw LLM output: it receives only a validated `ShedSpec`.
- Structural values come only from table lookup in the Framing planner, never from the LLM. Out-of-range or missing values raise, and the app asks or refuses rather than guesses. The LLM must leave unknown fields empty.
- Every output carries a planning-aid disclaimer; the user confirms the spec (the Confirm gate) before parts or guide generation.
- Eval discipline: tune on `dev` only; report from `held-out`. Eval cases are written before the pipeline is tuned. The eval runner prints held-out results only with an explicit flag, and records how many times held-out has been run. Held-out is run only for the baseline and the final numbers (3 runs each count as one look per run), and the counter is reported alongside the results.
- Baseline: a minimal prompt, run before any iteration, with its results file committed. Record the case-file hash before the first tuning run, so cases can't change quietly afterwards.
- Eval reproducibility: temperature 0; each results file records the prompt version, model ID and date. During tuning, single runs on `dev`. For the final reported numbers (and the baseline), the mean of 3 runs with the spread shown, so a claimed gain exceeds the noise. Estimate the cost of one full run against the $10 cap before the first run.
- Log each LLM call's model, tokens and estimated cost, and stop an eval run if cumulative cost would pass a configured limit (default well under the $10 budget). AWS Budgets only sends alerts, so this in-app stop is the real cap.

## Decisions
| # | Title | Status |
|---|---|---|
| [001](decisions/001-python-pydantic-uv.md) | Python, Pydantic contract, uv toolchain | accepted |
| [002](decisions/002-bedrock-llm-access.md) | Bedrock for LLM access | accepted |
| [003](decisions/003-streamlit-chat-ui.md) | Streamlit web chat | accepted; deferred by 008 (timing only) |
| [004](decisions/004-local-vector-store.md) | Local file-based vector store (Chroma) | accepted |
| [005](decisions/005-own-eval-harness.md) | Own eval harness with JSONL cases | accepted |
| [006](decisions/006-csv-span-tables.md) | Span and sizing tables as CSV with provenance | proposed (until the spike passes) |
| [007](decisions/007-sonnet-5-5-default-model.md) | Start with Claude Sonnet 5.5 on Bedrock | proposed (until the spike passes) |
| [008](decisions/008-defer-ui-cli-first.md) | Defer the UI; slice 1 runs from a CLI or notebook | accepted |
