# Backlog: AI Build Guide App

_Status: approved_ · _Last updated: 2026-11-05_ · Built from [DESIGN.md](DESIGN.md)

Priority order: (1) unblockers first, following dependencies; (2) risky unknowns next, as spikes; (3) then highest value for effort.

Status values: `todo` → `specced` → `building` → `done` (or `dropped`).

Legend: Size is how big the slice is (S = one sitting, M = a few sittings). Value and Effort are H/M/L, so Effort `L` means low effort. Est hrs are rough planning guesses by the planner, not measurements. Replace them with actuals as slices finish.

Note: IDEA.md and DESIGN.md call the whole core "slice 1" (retrieval = slice 2, guide = slice 3). Backlog IDs below are separate and cover only IDEA "slice 1" (core, criteria 1-5 plus the A5 friend check).

Note: DESIGN.md calls the spike "the first slice". This backlog puts a fakes-only walking skeleton before it, so the spikes have a project to run in. Recorded in [decision 009](decisions/009-skeleton-before-spike.md).

| ID | Slice | Outcome (what you can demo) | Type | Size | Est hrs | Value | Effort | Depends on | Status | Spec |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Walking skeleton | `uv run shedguide` takes a typed chat line, a fake LLM returns a canned `ShedSpec`, a stub 1-row table gives a `FramingPlan`, a parts list prints with the disclaimer. `python -m shedguide.evals` runs one canned case through the same path and writes a results file. ruff, mypy, pytest and format checks are configured and pass. | build | M | 4 | H | M | none | done | [01](specs/01-walking-skeleton.md) |
| 02 | Spike A: table source, license, envelope | Timebox about 4 hours. Written answer: named reference and license, tables exist for studs, joists and rafters, envelope paragraph, 5 hand-written eval examples. Friend-case requests sent out. Decision 006 resolved. If a table is missing or no source is license-clean, work stops for a re-plan (see Why this order). | spike | M | 5 | H | M | 01 | specced | [02](specs/02-spike-a-table-source.md) |
| 03 | Spike B: budget and Bedrock | AWS Budgets alert set first. Then one real Bedrock tool-use call from the skeleton's LLM client, with the exact Sonnet 5.5 model ID, model access and region confirmed (or fallback chosen), and per-call cost logging with a stop limit. Cost of one full eval run estimated against the $10 cap. Decision 007 resolved. | spike | S | 2 | H | L | 01 | todo | |
| 04 | Envelope, real models, eval harness | Final envelope written down and the 5 spike examples migrated to the real `ShedSpec`/`FramingPlan`/`ValidationResult` models. `python -m shedguide.evals` loads JSONL cases, scores extraction per-field (with tolerances) and full-spec match, writes a results file (prompt version, model ID, date), and guards held-out behind a flag with a run counter. | build | M | 5 | H | M | 02, 03 | todo | |
| 05 | Source-derived gold plans | 10 `FramingPlan`s computed from the source document by hand, across studs, joists and rafters, plus 3 hand-computed parts lists, all written before any CSV is transcribed. Split stated up front: 5 go to dev and 5 to held-out. Load cleanly in the harness. | build | M | 5 | H | M | 04 | todo | |
| 06 | Real extractor and confirm gate | Bedrock extractor with a minimal prompt, a chat loop that ends in a validated `ShedSpec` or asks for a missing value or refuses an out-of-scope project type, and `confirm()` yielding `ConfirmedSpec` (evals auto-confirm). An end-to-end-from-chat eval runner (chat to outcome or plan) that reports separately from the gold-spec scorers. The minimal prompt is pinned as the baseline prompt version at the end of this slice. | build | M | 6 | H | M | 03, 04 | todo | |
| 07a | Joist table and planner | Transcribed joist CSV with provenance, joist `FramingPlan` output, `OutOfRangeError` for out-of-range spans. The plan-match scorer (criterion 3) is built here and scores dev against the slice 05 joist plans (100% on in-range). Monotonicity and provenance tests pass. Owner re-checks each transcribed row once. | build | M | 4 | H | M | 05 | todo | |
| 07b | Joist parts list and first real demo | Joist-only parts list with `data/stock.csv` rows and its property checks (cuts cover lengths, waste is never negative, counts match spacing, every cut fits stock), then the full CLI path. Demo: describe a shed, get a question, a refusal for an out-of-range span (via the planner's `OutOfRangeError`, shown as a plain refusal), or a joist list. Ends with an owner-only fresh-clone install and run, noted in writing, only after the checks pass. The friend waits for slice 15. | build | M | 5 | H | M | 06, 07a | todo | |
| 08 | Stud and rafter tables and planner | Stud and rafter CSVs with provenance, planner covering all three members. Plan-match (built in 07a) scored on dev against slice 05 gold plans. Monotonicity and provenance tests pass. Owner re-checks each transcribed row once. | build | M | 5 | H | M | 07a | todo | |
| 09 | Extend parts engine to studs and rafters; criterion 5 scorer | Parts engine and `stock.csv` extended from joists to studs and rafters. A parts-check runner (criterion 5) runs on every eval case, and the plan-match scorer from 07a runs on all three members. Both reach 100% on the dev cases written so far. | build | M | 5 | H | M | 07b, 08 | todo | |
| 10 | Full validator and criterion 4 scorer | ok/ask/refuse/flag outcomes with reasons, `OutOfRangeError` mapped to refuse, requested-size-too-small flag. Outcome-match scorer (criterion 4) built. Writes at least 2 ask, 2 refuse and 1 out-of-range dev case by hand (counted toward the 4 ask and 4 refuse required in slice 11), and reaches 100% on them. | build | M | 6 | H | M | 06, 08 | todo | |
| 11 | Write eval cases: dev to 25 | Remaining dev cases written (messy, ambiguous, out-of-scope, at least 4 ask and 4 refuse in total, including slice 10's), reusing slice 05's dev plans. | build | M | 8 | H | M | 05 | todo | |
| 12 | Write eval cases: held-out (25) and freeze | 25 held-out cases (including friend-written inputs, at least 4 ask and 4 refuse, 2 more hand-computed parts lists), then the case-file hash recorded. Friend-written inputs depend on the requests sent in slice 02; if no friend replies by the start of this slice, the owner writes messy inputs in a friend's style and notes it. | build | M | 8 | H | M | 11 | todo | |
| 13 | Baseline runs | Cost estimate for one full run checked. Baseline prompt (pinned in 06) run on dev and on held-out (3 runs, which counts as 3 held-out looks), results files committed. Criteria 3, 4 and 5 scored from gold specs, and the end-to-end-from-chat result reported separately. Criterion 2's target reviewed against the baseline. **Held-out miss rule:** a miss on criteria 3, 4 or 5 on held-out is fixed in code only after it is first reproduced with a new dev case. The fix is disclosed in the results and each re-score counts in the look counter. Gold answers are re-derived from the source, never from the CSV. | build | M | 6 | H | M | 09, 10, 12 | todo | |
| 14 | Tune on dev and final numbers | Prompt, extractor and (under the held-out miss rule) code changes judged on dev only, capped by a stated number of dev iterations (set in the spec) as well as the cost limit. Final held-out run (3 runs, 3 more looks, counter reported, 6 in total). Criteria 2 to 5 numbers and the end-to-end report recorded. Extraction half of the resume bullet drafted (retrieval half waits for slice 2). | build | M | 8 | H | M | 13 | todo | |
| 15 | Packaging and friend check (A5) | README, credential and region setup, and a clean install from a fresh clone, tested by the owner. Then one friend installs and runs the CLI on their own machine with their own model credentials. Written note on what worked and what broke. If setup was too hard, the UI moves up the Later list. | spike | M | 5 | M | M | 14 | todo | |

Estimated total: about 87 hours (see "Time check").

## Why this order
- 01: proves uv, Pydantic, CLI, fake LLM, stub lookup, the eval harness path and the check commands connect before any real data or cost. Uses fakes, so the spikes do not change it.
- 02: the riskiest unknown (A3, A4, Q5, Q6). **Re-plan gate:** if a member-type table is missing or no source is license-clean, stop and revise before slice 04. Under the fallback of hand-summarized tables, slices 05 and 08 change (row-by-row cross-check, reworded "code-checked" claim) and IDEA criteria 3 and 5 may be reworded.
- 03: independent of 02 and small. Budget alert comes before the first Bedrock call. Puts AWS setup before any real model use in 06.
- 04: needs 02's envelope to fix the schema, and 03's client for cost logging in later runs.
- 05: the source-derived plans must exist before any table is transcribed, so a transcription slip cannot also appear in the gold answer.
- 06: real Bedrock path and the confirm gate, before any parts list, because the parts engine accepts only a `ConfirmedSpec`. The baseline prompt is pinned here, with no tuning against cases before 13.
- 07a, 07b: the first demoable real vertical path, with one member type. Tests the riskiest wiring (Bedrock tool use into deterministic lookup). The parts checks arrive in 07b before anyone else sees a parts list. An owner fresh-clone run here surfaces setup problems early.
- 08, 09: widen the proven path to the other members, then extend the parts engine and add the criteria 3 and 5 scorers, reaching 100% on dev first.
- 10: full validator after all tables can raise `OutOfRangeError`, with the criterion 4 scorer and the first ask/refuse dev cases, reaching 100% on dev first.
- 11, 12: finish and freeze the eval set before the baseline, so cases cannot drift after results are seen. Slices 08 to 10 score on dev only until then.
- 13: the baseline is committed before tuning. First full-run spend, and the first place criteria 3, 4 and 5 are scored on held-out. The held-out miss rule is stated here.
- 14: open-ended by nature, so after the baseline and capped.
- 15: DESIGN puts the friend check at the end of Artifact #1. Packaging comes first, because friend setup is the likeliest failure.

## Time check
IDEA allows about 2-4 hrs/week for 3 months, so roughly 25-50 hours. The estimate above is about 87 hours, so the plan does not fit the 3-month window as written. M0 alone fills the window.
| Milestone | Est hrs | At 3 hrs/week |
|---|---|---|
| M0 (01-07b) | 36 | about 12 weeks |
| M0b (01-12) | 68 | about 23 weeks |
| M1 (01-15) | 87 | about 29 weeks |

The planner has not cut scope. Options for the owner to choose: shrink the eval set, defer a member type, or accept a longer timeline. Decide before slices are specced.

## Milestones
| Milestone | Slices | What's true when it's done |
|---|---|---|
| M0: first real demo | 01-07b | Spikes answered. A real chat to joist list path works from the CLI with property checks, and the owner has run it from a fresh clone. Model spend limited to the spike and demo. |
| M0b: deterministic core and frozen eval set | 01-12 | All three members planned and listed by code. Validator done. Criteria 3, 4 and 5 scorers at 100% on the dev cases so far. 50 cases written and the hash recorded. No tuning yet. |
| M1: core complete (IDEA slice 1) | 01-15 | Baseline and final held-out numbers recorded and reported, including the end-to-end figure. A friend has run the packaged CLI. Criteria 1-5 measured and reported (targets or wording may change per the spike fallback or the baseline review). Criteria 6 and 7 belong to retrieval and guide, which are not planned here. Criterion 8 is half done (extraction only). |

M1 has 16 slices (counting 07a and 07b), over the usual 4-10. The extra come from splitting the spike, the thin path, the parts and validator work, and the eval-case writing, each to keep slices at S or M.

## Later / maybe
Not planned yet; each needs its own slicing pass after M1.
- Retrieval (IDEA slice 2): corpus, chunking, `retrieve(query, k)`, recall@k with a before/after change, the embedding model decision, and the retrieval half of the resume bullet.
- Guide (IDEA slice 3): cited `GuideStep`s, guide checker, readability judge.
- Streamlit chat UI (decisions 003 and 008), only with password, per-day call cap and budget alert if shared on the owner's account.
- Headers, posts and fasteners sizing in code.
