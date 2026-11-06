# 009. Fakes-only walking skeleton before the table-source spike

_Status: accepted_ · _Date: 2026-11-05_

## Context
DESIGN.md's "First gate" section calls the table-source spike "the first slice". The spike needs a project to run in (uv, tests, an LLM client for the Bedrock call, an eval harness for the 5 examples). The BACKLOG puts a fakes-only walking skeleton (slice 01) ahead of the spike (slices 02 and 03) and asked for this to be recorded before building.

## Decision
Slice 01, a walking skeleton that uses a fake LLM and a stub 1-row table and makes no real calls, is built before the spikes (02 table source, 03 budget and Bedrock). The spikes remain the first gate for anything real: no real table, real model call or real eval case is added until they pass. DESIGN.md's "spike is the first slice" now means the first slice that touches real data or services.

## Alternatives considered
| Option | Why not |
|---|---|
| Spike first, no project | The spike's outputs (5 eval examples, Bedrock call, cost logging) would be throwaway scripts with no tooling or tests |
| Skeleton with real tables and Bedrock | Would build on unchecked assumptions (A3, A4, Q5, Q6) and risk spend before the budget alert exists |

## Consequences
About 4 hours are spent before the riskiest unknown is answered. If the spike fails (no license-clean source, missing member table), the skeleton's table loader and stub are small and cheap to rework. The skeleton's fake data is labeled as fake in the CSV, its note and every CLI output so it cannot be mistaken for framing data.
