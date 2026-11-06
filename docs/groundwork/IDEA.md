# AI Build Guide App

> A chat app that turns a plain-English small-shed project into a validated spec, a code-checked parts and cut list, and a cited build guide, for the owner and a few DIY friends.

_Status: agreed_ · _Last updated: 2026-11-05_

## Problem
DIYers planning a shed have to turn a vague idea into correct dimensions, lumber counts and steps. Framing rules (floor joist and rafter spans and spacing, header and post sizing, fasteners) make mistakes costly. Existing AI woodworking planners (Woodplans.ai, Crafti, TimberTinker) focus on furniture, and their cut-list correctness is unverified (see A2). This project is also the vehicle for the 14-month AI-engineer plan (`ai-engineer-recipe-book.md`), so measured results matter as much as the app.

## Users
| Who | What they're trying to do | How often |
|---|---|---|
| Owner (builder of the app) | Plan a real shed, and produce measured portfolio results | Per project, plus weekly dev time (2-4 hrs/week) |
| A few DIY friends | Describe a shed and get a trustworthy parts list and guide | Occasional |

## Smallest first version (Artifact #1, slice order)
1. **Core:** Pydantic shed spec, 50-example eval set (25 dev, 25 held-out), chat to validated spec, deterministic cut and parts list for framing members (studs, joists, rafters). Headers, posts and fasteners are guidance only in Artifact #1. No RAG, no guide.
2. **Retrieval:** RAG over reference material, measured by recall@k.
3. **Guide:** LLM-written build steps from the validated spec, with citations.
CAD, drawings and the physical build are outside Artifact #1. The owner builds a real shed on their own time.

## Success criteria
Artifact #1 (months 1-3). Each is checkable.
1. **Eval set.** 50 examples (chat input plus hand-written expected spec), written before the pipeline is tuned. Split into dev and held-out. Includes messy, ambiguous and out-of-scope inputs, and some inputs written by a friend. Tuning uses dev only; reported numbers come from held-out.
2. **Spec extraction.** Metric: per-field match against the expected spec, with a stated tolerance on dimensions (for example ±0.5 in), plus full-spec exact-match rate. Record a baseline and a final number on held-out. Target: a gain of at least 15 points per-field match over baseline, or at least 90% per-field match, whichever is reached first (adjust after the baseline is seen).
3. **Structural correctness.** For the eval cases, the joist/rafter/stud size and spacing that code derives (the framing plan) match a deterministic table lookup from the chosen reference. Scored from the gold (hand-written) spec into the framing plan, so it measures the lookup and not extraction errors; the end-to-end result from chat is reported separately. Target: 100% on cases in range.
4. **Refusal on out-of-range.** Inputs outside the table range (for example a span beyond the table) or out of scope are refused rather than guessed, and a missing required value is asked for rather than guessed. Either `ask` or `refuse` counts as correct handling when it matches the case's expected outcome. Covered by dedicated eval cases and tests; target: 100%.
5. **Parts and cut list.** Chat produces a schema-valid spec, and deterministic code turns it into a parts and cut list that pass code checks (lengths fit stock sizes, totals match the spec: cut lengths cover the required member lengths, waste is never negative, counts match spacing). Artifact #1 covers framing members (studs, joists, rafters); headers, posts, fasteners, sheathing and foundations are guidance only.
6. **Retrieval.** Recall@k is measured separately from answer quality. Define k (for example 5), a relevant chunk (contains the fact needed to answer, labeled by the owner), and a before/after from one deliberate change (chunking or reranker).
7. **Guide.** Each guide step cites its source and agrees with the validated spec (checked by code where possible, LLM judge only for readability).
8. **Resume bullet.** Writable as: "Improved spec-extraction accuracy from X% to Y% and retrieval recall@k from A to B on a 50-example eval set (25 held out)."

## Non-goals
- No LLM-generated CAD. The LLM only fills the spec and writes guide steps.
- No 3D CAD or 2D drawings in Artifact #1 (later phases).
- No physical-build milestone in the plan; the owner builds on their own time.
- No project types other than a small shed in v1 (no decks, furniture, or larger framing).
- No accounts, sharing, mobile app, or store cart/pricing in Artifact #1.
- No proprietary work data or code.
- Not a code-compliance authority: output is a planning aid, not a permit-ready design.

## Constraints
- About 2-4 hrs/week of personal time (roughly 25-50 hours in 3 months), which is why slices are ordered above.
- Python, Pydantic schema as the contract between LLM and deterministic code.
- Public, non-confidential data only. Bedrock vs. direct Anthropic API is a design decision.
- A few DIY friends only, so no real hosting or support burden.

## Assumptions
- A1: One narrow shed sub-type (small, single-story, simple gable or shed roof, wood-framed) is enough to define a useful schema. Confirm in design.
- A2: Existing tools get cut lists wrong on projects I know well. Unchecked; not pursued for now.
- A3: Span and lumber-size tables are available from a public source whose license allows use. Checked in the first spike.
- A4: Eval ground truth can be written by hand from those tables. Checked in the first spike by writing 5 examples.
- A5: Friends will tolerate a CLI or simple web chat. In Artifact #1 they run the CLI on their own machines with their own model credentials; tested by one friend session at the end of slice 1 (see DESIGN.md, Slice 1 order). If setup is too hard, build the UI sooner.
- A6: Span and sizing values come from deterministic table lookup (a CSV/JSON file read by code), not from RAG. RAG runs over prose (fastener and connector schedules, anchoring and foundation guidance, sheathing and roofing practice, rule text) and supplies citations for spec values plus guidance for the guide. A harder variant, where RAG retrieves the applicable table and footnotes and code then does the lookup, is an option for slice 2 or later (decide in design).

## Risks
| Risk | Likelihood | Impact | What would reduce it |
|---|---|---|---|
| Hand-written ground truth is slow, so the eval set stalls | Med | High | Narrow shed sub-type; hand-compute from one reference; spike 5 examples first |
| Wrong structural output misleads a friend into an unsafe build | Med | High | Deterministic table lookup; refuse out-of-range or missing values (criterion 4); sources shown; spec reviewed by a human before generation; disclaimer |
| Eval set is too clean and the gains don't carry to real messages | Med | Med | Dev/held-out split; messy and out-of-scope cases; friend-written inputs |
| RAG forced onto a problem where lookup is better | Med | Med | A6: RAG limited to citations and guidance |
| Scope creep into CAD, accounts, other project types | High | Med | Non-goals; slice order; park everything else |
| Limited weekly time slows the 3-month artifact | High | Med | Eval set first, thin slices, guide last |
| Reference licensing or quality problems | Med | Med | Spike on A3 early; fall back to synthetic or hand-summarized tables |

## Open questions
| # | Question | Blocking? | Recommended answer | Resolved |
|---|---|---|---|---|
| Q1 | Which project type is v1? | yes | Small shed | Resolved 2026-11-04: small shed |
| Q2 | How to handle requirements not in the schema (e.g. snow load, size limits)? | no | Add explicit fields for the few that drive structure; others become notes | |
| Q3 | Stack: Bedrock vs. Anthropic API, pgvector vs. other, interface type | no (design) | Decide in gw-design | |
| Q4 | Spec versioning once projects are saved | no | Defer past Artifact #1 | |
| Q5 | Which published framing reference supplies the tables, and what are its license terms? | yes (before the corpus and eval set) | Start with a university extension shed/framing guide or an American Wood Council guide; check license and write 5 eval examples by hand in the first spike. Other sources: local building department accessory-structure handouts, US Forest Products Lab Wood Handbook. IRC is copyrighted: read for reference, don't redistribute its tables. | |
| Q6 | What is the supported envelope (max footprint, roof style, floor type, load conditions)? It is not a limit on user input: it is what the system can verify. Outside it the app flags and refuses. | yes (for schema and eval set) | Decide in design, from what the chosen reference tables cover | |

## Critic notes
Review by gw-critic on 2026-11-04. Verdict: needs work.
| # | Finding | Outcome |
|---|---|---|
| 1 | Real-build criterion had no pass bar or time budget | Applied: removed from the gate; owner builds on own time |
| 2 | Accuracy and recall@k undefined | Applied: criteria 2 and 6 |
| 3 | No structural-correctness criterion | Applied: criterion 3 |
| 4 | RAG role unclear | Applied: A6, criterion 7, slice order |
| 5 | Scope exceeds the time budget | Applied: "Smallest first version" section |
| 6 | Q1/Q5 undecided, A3/A4 untested | Applied: Q1 resolved (shed), Q5/Q6 stated, spike in A3/A4 |
| 7 | Eval set realism and no held-out split | Applied: criterion 1 |
| 8 | Safety mitigation vague | Applied: criterion 4 and risk row |
| 9 | No evidence friends have the problem; A2 untested | Ignored by owner |
| 10 | PROJECT.md out of sync | Deferred: update PROJECT.md after IDEA.md is agreed |
