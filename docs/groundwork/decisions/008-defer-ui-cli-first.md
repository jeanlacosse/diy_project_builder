# 008. Defer the UI; slice 1 runs from a CLI or notebook

_Status: accepted_ · _Date: 2026-11-05_

## Context
The second critic pass found the scope heavy for 25-50 hours, and that the UI is not needed for any Artifact #1 success criterion. Sharing a UI through a tunnel would also expose the owner's Bedrock spend, and the live app has no cost cap. [003](003-streamlit-chat-ui.md) put Streamlit in the first slice.

## Decision
Slice 1 is the pipeline plus the eval harness, driven from a CLI or notebook. Streamlit is still the chosen UI (the rest of 003 stands), but it is built only after the criteria 1-5 numbers exist. No public or tunnel sharing until then. Friends run the CLI on their own machines with their own model credentials. Before any shared live use of the owner's account, add a shared password, a per-day call cap in the app, and an AWS Budgets alert (Budgets only alerts; the in-app cap is the real limit).

## Alternatives considered
| Option | Why not |
|---|---|
| Keep Streamlit in slice 1 | Costs hours that the 50-case eval set needs; makes the spend-exposure controls urgent |

## Consequences
More time for the eval set and the measured results. Friends need a working Python setup and their own Bedrock (or other model) credentials to use the CLI, which is real setup work for a non-developer. Slice 1 ends with one friend trying it to test A5; if setup is too hard, that is the signal to build the UI sooner. The pipeline is already UI-free, so adding the UI later is a thin layer.
