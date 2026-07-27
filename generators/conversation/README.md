# Conversation Generator — next-reply training grain (v2)

## Training unit

One JSONL record = one Conversation capability interaction:

```text
ConversationRequest { turns: prefix… }
        ↓
ConversationResponse { reply: next assistant turn }
```

Never a single integrated corpus-wide conversation.

## Generator flow

```text
Upstream JSONL (planner, coding, execution required;
               repair / context / approval soft)
        ↓
EpisodeReconstructor  (one dialogue per coding anchor / module)
        ↓
DialogueSlicer        (one TrainingSlice per assistant reply)
        ↓
History truncation    (max messages + char budget; no future leakage)
        ↓
Sort by record_id → DatasetWriter (N records)
        ↓
manifest + statistics
```

## Identity (Step 2.1)

```text
conversation_id = H(module + anchor_id + id_scheme_version)
record_id       = H(conversation_id + turn_index + id_scheme_version)
```

- No timestamps / UUIDs / randomness in the ID preimage
- Emit order: ascending `record_id`

## History bounds

| Bound | Value |
|-------|-------|
| Max prefix messages | 16 |
| Max prefix chars | 12_000 |
| Max message chars | 1_500 |

Configured in `generators/conversation/policy.py`.

## Versions

- Generator: `2.0.0`
- Schema: `conversation-v2` / `schema_version` `2.0`
- `id_scheme_version`: `1`

## Migration

| Before | After |
|--------|-------|
| 1 integrated conversation | N next-reply slices |
| Approval hard dependency | Approval soft / optional |
| `conversation-v1` | `conversation-v2` (+ record_id, conversation_id, turn_index) |

See `docs/conversation_migration_v2.md`.
