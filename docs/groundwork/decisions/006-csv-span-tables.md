# 006. Span and sizing tables as CSV with provenance

_Status: proposed (becomes accepted when the spike passes)_ · _Date: 2026-11-05_

## Context
This decision's format is firm, but the source reference is not chosen yet (Q5); see the first-gate spike in DESIGN.md. A6: structural values (joist, rafter, stud size and spacing) come from deterministic lookup, not from the LLM or RAG. The tables must be checkable by eye against the source, and a wrong value is a safety risk.

## Decision
One CSV per table in `data/tables/`, hand-transcribed from the chosen public reference (Q5), each with a sibling `.md` provenance note (source, edition, license, date transcribed). A loader returns typed rows and raises a `OutOfRangeError` for any input outside the table range or with a missing value. The caller turns that into a refusal.

## Alternatives considered
| Option | Why not |
|---|---|
| JSON files | Harder to eyeball and diff against the source |
| Let RAG retrieve the table | Harder variant from A6; reconsider in slice 2 or later |

## Consequences
Easy to review and unit test; range limits are explicit data. Transcription errors are possible, so the owner re-checks every row against the source once, and tests check monotonicity and spot-check rows. If the reference's license forbids redistribution (IRC), only hand-summarized values go in the repo.
