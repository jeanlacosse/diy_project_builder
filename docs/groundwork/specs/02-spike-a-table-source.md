# Spec 02: Spike A: table source, license, envelope

_Status: approved_ · _Last updated: 2026-11-05_
Backlog row: 02 · Depends on: 01 · Size: M · Type: spike

## Outcome
A written, checked answer to the riskiest unknowns (Q5, Q6, A3, A4) inside a timebox of about 4 hours of working time (BACKLOG estimates 5 hours including writing and edits; time spent waiting for replies, such as the AWC licensing reply, does not count against the clock): which reference supplies the stud, joist and rafter tables and under what license, what envelope those tables support, and whether 5 hand-written eval examples can really be computed from them. It ends in one verdict: **PASS**, **PASS-WITH-FALLBACK**, or **FAIL (re-plan)**. This spike writes no table CSVs and no production code. It does not touch Bedrock (slice 03).

## Before you start (pre-work check)
- [x] Slice 01 is `done` in BACKLOG.md (checked 2026-11-05). Confirm it is merged before starting.
- [ ] `uv run pytest` passes on the current code.
- [ ] Nothing in "Do not touch" has changed shape since this spec was approved.
- [ ] Owner has the three PDFs in `docs/span_tables/` (git-ignored) and the draft AWC licensing request in `notes.md`. Sending that request is an owner action; do it early, since a reply may take days.

## Requirements
| ID | Requirement |
|---|---|
| R1 | The write-up names every candidate reference (title, edition, publisher, where obtained), and a plain yes / no / unknown on "values may be committed to this repo". |
| R2 | For each of wall studs, floor joists and rafters, the write-up cites the exact table(s) (table number and page) that cover it, with the inputs (species/grade, size, spacing, load) and the output (max span or height). A member with no table in any named source is marked MISSING. |
| R3 | The write-up has one envelope paragraph covering max footprint, roof style, floor type, load conditions, and species/grade, plus what is refused outside it. Each limit traces to a table coverage edge. |
| R4 | `evals/spike/examples.jsonl` holds exactly 5 hand-written examples: 3 in range, 1 `ask` (a required value missing), 1 `refuse` (a span just past a table maximum). Each line is JSON with keys `id`, `input`, `expected_spec`, `outcome` (`ok`, `ask` or `refuse`) and, as applicable, `plan`, `cite` and `reason`. In-range cases have a hand-computed `plan` and a `cite` with non-empty `table` and `page` fields. The `ask` case names the missing field in `reason`; the `refuse` case states why in `reason`. At least one in-range example sits exactly at a table's maximum span, and the refuse example is just past a maximum. The owner re-reads each cited table cell against the source once, and that is recorded in the write-up. |
| R5 | The write-up logs minutes spent per example and gives an A4 verdict (can ground truth be written by hand from these tables: yes / no). |
| R6 | Friend-case requests are sent, and the write-up records the date, how many people, and the request wording only: no names, contact details or personal information. Replies are not required for this slice. |
| R7 | Decision 006 is resolved with `/gw-decide` to match the verdict (accepted, or superseded by a new decision if the fallback applies), and the DESIGN.md decisions-table row agrees. Decision 007 is left `proposed`. |
| R8 | The write-up ends with the verdict and a gate checklist. The checklist covers only the items this slice owns (named reference and license, three member tables, envelope paragraph, 5 examples); the Bedrock and AWS Budgets items in DESIGN.md's First gate are marked "slice 03". On FAIL or FALLBACK it lists which slices (04, 05, 08) and which IDEA criteria (3, 5) change, and no later slice is specced until the owner acts. |
| R12 | Verdict definitions: **PASS** = all three members have a table and every source used is license-clean (commit permission "yes"). **PASS-WITH-FALLBACK** = a source is "no" or "unknown" on commit permission, but hand-summarized tables with row-by-row cross-checking are workable. **FAIL (re-plan)** = a member has no table in any source and the parts scope cannot simply be narrowed, or hand-summarizing is not workable. A MISSING member is never plain PASS. |
| R9 | IDEA.md marks Q5 resolved (dated, pointing at the write-up) and notes the A3 and A4 outcomes. Q6 stays open until slice 04 finalizes the envelope. |
| R10 | No source PDFs and no full copy of any table are committed. Table values appear only where an eval example needs them: while a source's commit permission is "no" or "unknown", an example cites the table and page and gives only the looked-up value(s) it needs, with no verbatim table rows or page images. `Floor-Joists.pdf` is not quoted until its origin is found. `data/tables/` still holds only the stub files. |
| R11 | The write-up records actual hours against the timebox. If the timebox runs out before a verdict, open items are listed as unresolved, not silently extended. |

## Scope
| Component / file | Change | Notes |
|---|---|---|
| `docs/groundwork/spikes/02-table-source.md` | new | The written answer: R1 to R3, R5, R6, R8, R11. Location is assumption A1 (DESIGN.md names no spike folder) |
| `evals/spike/examples.jsonl` | new | R4. Outside `evals/cases/` on purpose: the harness does not read it, and slice 04 migrates it |
| `tests/test_spike_examples.py` | new | T7 to T9. Contains its own small shape checker; slice 04 replaces this file when it migrates the examples |
| `docs/groundwork/decisions/006-csv-span-tables.md` | modify | R7, via `/gw-decide` |
| `docs/groundwork/decisions/011-*.md` | new, only if fallback | R7. A superseding decision for hand-summarized tables. 010 (Python 3.13) already exists and is not touched |
| `docs/groundwork/DESIGN.md` | modify | Decisions-table row for 006 (and 011 if created) only |
| `docs/groundwork/IDEA.md` | modify | R9: Q5 resolved cell, A3 and A4 notes only |
| `docs/groundwork/BACKLOG.md` | modify | Row 02 only. Transitions: `todo` to `specced` (with spec link) on approval, `building` at build start, `done` after gw-check |

**Out of scope:**
- Transcribing any CSV into `data/tables/` (slices 07a and 08), and the 10 source-derived gold plans (slice 05).
- The final envelope and the real `ShedSpec` models (slice 04). Spike examples use loose field names.
- Bedrock, AWS Budgets, model ID and decision 007 (slice 03).
- Retrieval corpus sources (slice 2). Only the framing tables are chosen here.
- Removing or migrating `tests/test_spike_examples.py` and `evals/spike/examples.jsonl`: slice 04 owns this, and its spec should list it.
- Legal advice. The write-up records what the terms say and what the owner decided; it does not certify compliance.

**Do not touch:** `src/`, `data/` (R10 checks `data/tables/` holds only the stub files), `pyproject.toml`, `uv.lock`, `evals/cases/`, `evals/results/`, decisions 001 to 005 and 007 to 010, the top-level `groundwork/` plugin folder, `PROJECT.md`, `notes.md`, and the contents of `docs/span_tables/` (read-only inputs, git-ignored). Files under `docs/groundwork/` are touchable only as the Scope table lists.

## Approach
This is research plus a few documents, so the "build" is reading sources and writing down findings in a fixed shape. Start from what is already on disk (checked 2026-11-05):
- `AWC_STJR2024_...pdf`: AWC *Span Tables for Joists and Rafters*, 2024 edition, 52 pages, © 2023 American Wood Council. Covers joists and rafters. It does not appear to cover wall studs (to confirm in task 1). Copyrighted; the owner has a draft licensing request in `notes.md`.
- `Floor-Joists.pdf`: one page of floor joist spans by species and spacing, with no clear publisher or license. Treat as unattributed until the origin is found.
- `MN2000_FSHE_042.pdf`: a 1982 university fact sheet on roof snow load, not a span table. Possibly useful for the envelope's load wording only.

Studs are the likeliest gap. Checked 2026-11-06: the AWC STJR 2024 PDF has no stud table (its text layer has no stud or wall-stud content). Lead stud candidate: Minnesota Rules part 1309.0602, amended Table R602.3.1 (https://www.revisor.mn.gov/rules/1309.0602/), "Official Publication of the State of Minnesota", no copyright notice on the page (check the Revisor site's general terms). Per a summarized read, to verify against the page: wall studs only; 2x4, 2x6, 2x8 at 8, 12, 16, 24 in. o.c.; wall heights 10 to 24 ft (a 7 to 9 ft shed wall may fall below the lowest row: envelope risk); roof spans to 34 ft; exposure B and C; every section is "supporting a roof only" (no floor-bearing walls); assumes SPF #2 or better and the wind and snow loads in its footnote b; footnotes a to j add sheathing, bracing, blocking, L/120 deflection and fastening conditions. Commit permission is "unknown, lower risk" (state-published law, but the values may derive from ICC or AWC content). Fallback stud candidate: IRC Table R602.3(5) "Size, Height and Spacing of Wood Studs" in the edition Minnesota adopts (Minnesota Rules chapter 1309, https://www.revisor.mn.gov/rules/1309/full; base edition 2018 IRC per the 2020/2021 rule text, to confirm current). Copyright is held by ICC, so commit permission is "unknown" until ICC answers. Chapter 1309 holds only Minnesota's amendments and incorporates the IRC by reference, so the table text itself comes from ICC's free read-only viewer (codes.iccsafe.org; terms to confirm) or a library copy. Check whether chapter 1309 amends R602.3(5). Other candidates to check, not yet verified: a stud table in a code or AWC manual (copyrighted), or an extension or building-department handout. IDEA Q5 already warns that IRC tables are copyrighted: read for reference, do not redistribute.

Decide by the DESIGN.md "First gate" rules: if a member table is missing, narrow the parts scope; if no source is license-clean, use hand-summarized tables, reword "code-checked", and cross-check each row (decision 006's consequences). Gold examples in R4 are computed by reading the source, not from any CSV, so they stay independent of later transcription.

Assumptions to confirm at approval:
- A1: The write-up lives in `docs/groundwork/spikes/` and the examples in `evals/spike/`.
- A2: "Friend cases" means asking friends for a few messy, real-sounding shed requests each. DESIGN.md says "some" friend-written inputs without a count, so how many friends to ask is the owner's decision (3 is a suggestion, not a requirement).
- A3: An unanswered AWC licensing request at the end of the timebox counts as "unknown", which is not usable. The owner may extend the wait, but then the spike stays open and nothing downstream starts.
- A4: The 5 examples are 3 in range, 1 ask, 1 refuse. DESIGN.md requires at least 4 ask and 4 refuse cases per split later, so this mix is for the spike only.

## Tasks
| # | Task | Files | Done when |
|---|---|---|---|
| 1 | Inventory sources: identify each PDF and find a stud-table candidate | spike write-up | Every candidate listed with member coverage yes / no / unknown (feeds R1, R2) |
| 2 | License check for each source used; owner sends or follows up the AWC request | spike write-up | R1 fields filled for every used source; unknowns marked as unknown (T1, T2) |
| 3 | Coverage map: table number, page, inputs, outputs per member | spike write-up | One row per member; MISSING where applicable (T3, T4) |
| 4 | Envelope paragraph | spike write-up | Limits each cite a table edge (T5, T6) |
| 5 | Write the 5 examples, timing each; add the shape-check test | `evals/spike/examples.jsonl`, `tests/test_spike_examples.py`, spike write-up | T7 to T9 pass; T10 to T12 reviewed by hand |
| 6 | Draft friend request text; owner sends it | spike write-up | Date, count and text recorded (T13) |
| 7 | Verdict and re-plan gate; resolve decision 006; update IDEA.md; hygiene check; log hours | write-up, `decisions/006-*.md` (and 011), `DESIGN.md`, `IDEA.md`, `BACKLOG.md` | T14 to T20 reviewed; `uv run pytest` and the other three DESIGN.md checks pass |

## Tests
Automated tests have T-IDs in their names. "Manual" checks are a review against the written file, recorded under "Check result".
| Test ID | Covers | Kind | What it asserts |
|---|---|---|---|
| T1 | R1 | happy (manual) | Each used source has title, edition, publisher, origin, license, date checked, and a commit-permission answer; no blank or "TBD" |
| T2 | R1 | unhappy (manual) | A source whose license is unknown is not marked usable, and the verdict reflects that |
| T3 | R2 | happy (manual) | The coverage map has a row each for studs, joists and rafters with table number, page, inputs and output |
| T4 | R2, R12 | unhappy (manual) | A member with no table is marked MISSING and the verdict is not plain PASS |
| T5 | R3 | happy (manual) | The envelope paragraph names footprint, roof style, floor type, loads, species/grade, and what is refused |
| T6 | R3 | edge (manual) | Every numeric limit in the envelope cites the table maximum or coverage edge it comes from |
| T7 | R4 | happy | `test_T7`: the file has exactly 5 parsable lines, unique ids, all required keys, and a 3 in-range / 1 ask / 1 refuse split |
| T8 | R4 | unhappy | `test_T8`: the checker rejects fixtures in `tmp_path` with unparsable JSON, a blank line, a missing key, a duplicate id, an unknown outcome value, or a wrong outcome count |
| T9 | R4 | edge | `test_T9`: in-range cases each carry a plan and a cite with non-empty `table` and `page`; ask and refuse cases carry no plan; ask and refuse cases have a non-empty `reason` |
| T10 | R4 | edge (manual) | At least one in-range example sits exactly at a table's maximum span, the refuse example is just past one, and the owner's cell re-check is recorded |
| T11 | R5 | happy (manual) | Minutes per example and an A4 yes / no verdict are recorded |
| T12 | R5 | unhappy (manual) | If any example could not be computed, A4 is "no" and the verdict is not PASS |
| T13 | R6 | happy (manual) | Send date, number of friends and request wording are recorded with no names or contact details, and the owner confirms they were sent |
| T14 | R7 | happy (manual) | Decision 006's status is no longer `proposed`, the DESIGN.md row matches, and decision 007 shows no diff |
| T15 | R8, R12 | happy (manual) | The verdict is exactly one of PASS, PASS-WITH-FALLBACK, FAIL and matches the R12 definitions; the checklist shows Bedrock and Budgets items as "slice 03" |
| T16 | R8 | unhappy (manual) | On FAIL or FALLBACK, the changes to slices 04, 05, 08 and IDEA criteria 3, 5 are listed, and BACKLOG shows no slice past 02 as `specced` |
| T17 | R9 | happy (manual) | IDEA.md Q5 has a dated resolution pointing at the write-up; A3 and A4 have outcomes; Q6 is still open |
| T18 | R10 | happy (manual) | `git ls-files` lists no `.pdf`; `docs/span_tables/` is still ignored; `data/tables/` has only the stub files |
| T19 | R10 | edge (manual) | No table in the write-up or examples has more values than the examples use; no verbatim rows or page images; the unattributed PDF is not quoted |
| T20 | R11 | happy (manual) | Actual working hours are recorded (waiting time excluded); if over the timebox, open items are listed as unresolved |

## Done when
- [ ] Every requirement has a passing automated test or a ticked manual check in "Check result".
- [ ] All DESIGN.md check commands pass (`uv run pytest`, `uv run ruff check .`, `uv run mypy src`, `uv run ruff format --check .`).
- [ ] No files outside Scope were changed.
- [ ] Decision 006 is resolved with `/gw-decide`, and the verdict is recorded.
- [ ] If the verdict is not PASS, the owner has chosen how to re-plan before any further slice is specced.

## Review notes
Deep review by gw-spec-reviewer, 2026-11-05: verdict REVISE, 12 findings. Findings 1 and 2 (decision number collision with 010; slice 01 now `done`) were fixed first. Findings 3 to 12 were applied at the owner's request: BACKLOG transitions (3), specific Do-not-touch paths (4), verdict definitions as R12 (5), friend-request privacy and count as owner decision (6), quoting rule while license is unknown (7), named keys and extra T8 cases (8), edge requirement and cell re-check moved into R4 (9), timebox excludes waiting (10), gate checklist scoped to this slice (11), slice 04 owns removing the spike test (12).

Self-check: every R1 to R12 has at least one T; every task's files appear in Scope; nothing contradicts DESIGN.md's First gate or decisions 006 and 009. 

## Check result
Filled in by gw-check.
