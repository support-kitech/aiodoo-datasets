# Evaluation Generator — capability SFT + separate BenchmarkCatalog (v2)

## Training unit

One JSONL record = one Evaluation capability interaction:

```text
EvaluationRequest { candidate, expectation?, rubric? }
        ↓
EvaluationResponse { verdict, score?, explanation? }
```

Never a single BenchmarkCatalog as the training dataset.

## Artifacts

| File | Role |
|------|------|
| `evaluation_dataset.jsonl` | SFT judgments (many records) |
| `evaluation_benchmark_catalog.jsonl` | Certification / benchmark / regression (**not** SFT) |

## Generator flow

```text
Upstream JSONL (planner/coding/repair/execution required;
               context/approval/conversation soft)
        ↓
JudgmentBuilder  (pass + fail + inconclusive per candidate)
        ↓
Sort by record_id → evaluation_dataset.jsonl
        ↓
CatalogExport → evaluation_benchmark_catalog.jsonl (side channel)
```

## Identity (Step 2.1)

```text
candidate_id = H(capability + source_object_id)
record_id    = H(candidate_id + evaluation_case_key + id_scheme_version)
```

## Versions

- Generator: `2.0.0`
- Schema: `evaluation-v2`
- Catalog schema: `benchmark-catalog-v1`

## Migration

See `docs/evaluation_migration_v2.md`.
