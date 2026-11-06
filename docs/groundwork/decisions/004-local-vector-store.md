# 004. Local file-based vector store (Chroma)

_Status: accepted_ · _Date: 2026-11-05_

## Context
Slice 2 runs RAG over a small prose corpus (fasteners, anchoring, sheathing, rule text) for citations and guide guidance, with recall@k measured. The corpus is tiny and re-chunking must be cheap for the before/after experiment.

## Decision
Use Chroma with a persistent local directory. Embeddings come from a Bedrock embedding model (decided with the slice 2 spec). Retrieval sits behind a small `retrieve(query, k)` interface so the store can change.

## Alternatives considered
| Option | Why not |
|---|---|
| LanceDB | Equally valid; Chroma has the simpler API for a first RAG build |
| Postgres + pgvector | Needs a running database for a tiny corpus; revisit in months 10-12 |

## Consequences
No server to run. The index is rebuildable from the corpus, so it is not committed. Not suitable for multi-user production, which is out of scope.
