# 005. Own eval harness with JSONL cases

_Status: accepted_ · _Date: 2026-11-05_

## Context
Success criteria 1-4 and 6 need a 50-example eval set, a dev/held-out split, per-field and exact-match scoring with tolerances, and recall@k. The eval pipeline and tracing platform belong to Artifact #2 (months 4-6).

## Decision
Eval cases live in `evals/cases/*.jsonl` (chat input, expected spec, split, tags). A small Python scorer in `src/shedguide/evals/` computes per-field match with tolerance, full-spec exact match, refusal correctness and recall@k, and writes a results file per run. Tuning reads only the `dev` split; the `held-out` split is run for reported numbers.

## Alternatives considered
| Option | Why not |
|---|---|
| Braintrust or Langfuse now | Planned for Artifact #2; adds setup against a tight budget |

## Consequences
Full control over metrics and tolerance rules, and easy to unit test. Results are files in the repo, so baseline vs final is a diff. Migration to a platform later means writing an exporter.
