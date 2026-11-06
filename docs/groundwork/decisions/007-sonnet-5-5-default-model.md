# 007. Start with Claude Sonnet 5.5 on Bedrock

_Status: proposed (becomes accepted when the spike confirms the model ID and access)_ · _Date: 2026-11-05_

## Context
[002](002-bedrock-llm-access.md) chose Bedrock but not a model. Extraction needs reliable tool use and schema-valid output, and the work runs on a $10 budget. The baseline and final eval numbers must come from one fixed, recorded model.

## Decision
Use Claude Sonnet 5.5 on Bedrock for extraction and, later, the guide. The model ID lives in `config.py` and every eval results file records it. The exact Bedrock model ID, model access and region are confirmed in the first spike. If Sonnet 5.5 is unavailable in the owner's account or region, the fallback is Claude Sonnet 5 (exact ID confirmed in the spike), and the baseline is run on whichever model is used.

## Alternatives considered
| Option | Why not |
|---|---|
| Haiku 5.5 as default | Cheaper, but riskier for messy and ambiguous inputs. May still be tried on the dev split; Sonnet stays the reported model unless Haiku scores about the same |
| Opus 5.5 | Costs more than a $10 budget comfortably allows, with no sign extraction needs it |

## Consequences
Quality is unlikely to limit extraction accuracy, and the cost of 50 cases is small. Changing the model later is a config change, but it invalidates earlier baselines, so a change means re-running the baseline. The embedding model (slice 2) is still undecided.
