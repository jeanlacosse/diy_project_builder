# 001. Python, Pydantic contract, uv toolchain

_Status: accepted_ · _Date: 2026-11-05_

## Context
IDEA.md constrains the project to Python with a Pydantic schema as the contract between the LLM and deterministic code. Time is 2-4 hrs/week, so tooling must be quick and boring.

## Decision
Python 3.12, `uv` for environments and dependencies, `pytest` for tests, `ruff` for lint and format, `mypy` for type checks. The Pydantic `ShedSpec` model is the only way data crosses from LLM output into deterministic code.

## Alternatives considered
| Option | Why not |
|---|---|
| pip/venv + pyright | Slower setup, pyright needs node; no benefit here |
| poetry | Heavier than uv for a single-package project |

## Consequences
One-command setup and checks. Everything the LLM produces is validated before use. Ties us to Python for the whole project (fine, per IDEA.md).
