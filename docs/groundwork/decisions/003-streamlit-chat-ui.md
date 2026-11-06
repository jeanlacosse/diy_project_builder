# 003. Streamlit web chat

_Status: accepted; deferred by [008](008-defer-ui-cli-first.md) (timing only: Streamlit is still the chosen UI, but it is built later)_ · _Date: 2026-11-05_

## Context
Friends should use the app without a terminal (A5). No hosting or support burden is acceptable, and frontend work is not a trained skill.

## Decision
A Streamlit chat app is the interface. It is a thin layer over a plain Python pipeline (`chat -> ShedSpec -> parts list`), so the pipeline and evals run without the UI. The owner runs it locally and shares it with friends by tunnel or screen share. There is no public hosting in Artifact #1, so AWS credentials and Bedrock spend stay on the owner's machine. Friends can use it only when the owner has it running.

## Alternatives considered
| Option | Why not |
|---|---|
| CLI chat | Friends need a terminal; risks A5 |
| FastAPI + JS frontend | Frontend work eats the time budget |

## Consequences
Fast UI in pure Python. Limited layout control. No accounts, which matches the non-goals. UI code holds no business logic, so it needs little testing.
