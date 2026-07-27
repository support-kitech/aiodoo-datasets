# Approval Generator Migration Notes (v1 → v2)

## What changed

| Aspect | v1 (placeholder) | v2 (production grain) |
|--------|------------------|------------------------|
| Records | 1 corpus-wide Review | N subject decisions |
| Evidence | Entire upstream pool (~701k) | ≤32 items per record |
| Identity | Weak `REV-*` from module/version | `APR-*` from capability+subject+source+scheme |
| Contract | Thin subject/payload | Explicit `subject` + bounded `payload` |
| Schema | `approval-v1` | `approval-v2` |

## Consumer impact

- `PipelineResult.approval_protocol` is now `tuple[Review, ...]` (was a single `Review`).
- Conversation / Evaluation approval parsers already iterate lists — no API break.
- Training: regenerate before training the Approval LoRA; do not use the old 1-row file.
- Validation: old 1-row files fail APR-004 (and likely APR-002/003 / schema).

## Regeneration

```bash
# After upstream planner/coding/repair/execution JSONL exist:
python3 build_dataset.py
# Or invoke Approval stage only via the existing CLI / pipeline entrypoints.
```

Full corpus regeneration remains **Step 6** of the platform roadmap; Step 3 only
ships the generator + validation + tests.

## Non-goals (unchanged)

- `aiodoo-contract` ApprovalRequest/Response schemas
- Development / Reasoning adapter assignment
- Planner / Coding / Repair / Execution / Context generators
