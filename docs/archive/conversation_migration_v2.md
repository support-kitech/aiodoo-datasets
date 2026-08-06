> **Historical document.** Written when Git tags / release identity existed.
> Git tags and GitHub Releases were later removed ecosystem-wide.
> **Current source of truth:** branch `main` only. See `docs/STATUS.md`.
> Do not treat tag or release recommendations in this file as current instructions.

# Conversation Generator Migration Notes (v1 → v2)

## What changed

| Aspect | v1 (placeholder) | v2 (production grain) |
|--------|------------------|------------------------|
| Records | 1 integrated conversation | N next-reply slices |
| Training unit | Whole dialogue | Prefix → one assistant reply |
| Approval | Hard required input | Soft / optional dialogue material |
| Identity | Weak corpus hash | `CNV-*` from conversation_id + turn_index |
| Schema | `conversation-v1` | `conversation-v2` |

## Consumer impact

- Public `ConversationPipeline.generate` / `api.generate|export` signatures unchanged.
- `PipelineResult` adds `record_count` / `episode_count`.
- Training: regenerate before training the Conversation LoRA; do not use the old 1-row file.
- Validation: old 1-row files fail CNV-004 (and likely CNV-002/003 / schema).

## Regeneration

```bash
python3 build_dataset.py
```

Full corpus regeneration remains **Step 6**. Step 4 ships generator + validation + tests.

## Non-goals (unchanged)

- `aiodoo-contract` ConversationRequest/Response schemas
- Approval / Evaluation redesign
- Planner / Coding / Repair / Execution / Context generators
