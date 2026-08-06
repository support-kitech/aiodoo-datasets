> **Historical document.** Written when Git tags / release identity existed.
> Git tags and GitHub Releases were later removed ecosystem-wide.
> **Current source of truth:** branch `main` only. See `docs/STATUS.md`.
> Do not treat tag or release recommendations in this file as current instructions.

# Evaluation Generator Migration Notes (v1 → v2)

## What changed

| Aspect | v1 (placeholder) | v2 (production grain) |
|--------|------------------|------------------------|
| `evaluation_dataset.jsonl` | 1 BenchmarkCatalog aggregate | N judgment R/R records |
| Training unit | Catalog authoring | Candidate → verdict |
| BenchmarkCatalog | Same file as SFT | Separate `evaluation_benchmark_catalog.jsonl` |
| Contract projection | None | `project_evaluation` |
| Schema | `evaluation-v1` | `evaluation-v2` (+ `benchmark-catalog-v1`) |

## Consumer impact

- `api.generate` / `export` signatures unchanged.
- `PipelineResult.dataset` is now a tuple of judgment **dicts**.
- `PipelineResult.catalog` holds the BenchmarkCatalog side artifact.
- `api.validate` accepts judgment dicts **or** legacy `Evaluation` aggregates.
- **Never train** on `evaluation_benchmark_catalog.jsonl`.
- `aiodoo-training` `EvaluationFormatter` still formats catalog-shaped rows — sync it to the contract path after regenerating SFT data (known follow-up).

## Regeneration

```bash
python3 build_dataset.py
```

Full corpus regeneration remains **Step 6**.

## Non-goals (unchanged)

- `aiodoo-contract` EvaluationRequest/Response schemas
- Approval / Conversation redesign
- Planner / Coding / Repair / Execution / Context generators
