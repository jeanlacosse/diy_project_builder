# 002. Bedrock for LLM access

_Status: accepted_ · _Date: 2026-11-05_

## Context
IDEA.md leaves "Bedrock vs. direct Anthropic API" to design. The project doubles as practice for the owner's day-job stack (Textract and Bedrock), so skill transfer matters. Only public, non-confidential data is used.

## Decision
Call Claude models through Amazon Bedrock with `boto3` (Converse API, tool use for structured spec extraction). All LLM calls go through one thin `llm` module so the provider is swappable and tests can fake it.

## Alternatives considered
| Option | Why not |
|---|---|
| Anthropic API direct | Simpler start, but doesn't build the Bedrock skills the plan targets |
| Both behind a wrapper | Doubles the test surface in a 3-month budget |

## Consequences
Needs an AWS account with Bedrock model access and a personal (not work) AWS profile, because no work resources may be used. First-run setup is slower. Model IDs and region live in config. Unit tests never call Bedrock; evals do, and cost is logged per run.
