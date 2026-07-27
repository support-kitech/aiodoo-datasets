# Approval Generator — subject-decision training grain (v2)

## Training unit

One JSONL record = one Approval capability interaction:

```text
ApprovalRequest (subject + bounded payload)
        ↓
ApprovalResponse (status + reason)
```

Never a corpus-wide Review. Never unbounded evidence pools in the dataset.

## Generator flow

```text
Upstream JSONL (planner, coding, repair, execution)
        ↓
SubjectPartitioner  (one subject per upstream row)
        ↓
Per subject:
  parse subject-scoped evidence (full pool may exist in memory)
  DecisionEngine
  bound evidence / findings / recommendations
  emit Review with stable record_id
        ↓
Sort by record_id → DatasetWriter (N records)
        ↓
manifest + statistics
```

## Identity (Step 2.1)

```text
record_id = H(capability + subject_id + source_object_id + id_scheme_version)
```

- `review_id` equals `record_id`
- No timestamps / UUIDs / randomness in the ID preimage
- Emit order: ascending `record_id`

## Bounds

| Field | Cap |
|-------|-----|
| evidence items | 32 |
| findings | 32 |
| recommendations | 16 |

Configured in `generators/approval/policy.py`.

## Versions

- Generator: `2.0.0` (major: grain change from 1-record placeholder)
- Schema: `approval-v2` / `schema_version` `2.0`
- `id_scheme_version`: `1`

## Migration

| Before | After |
|--------|-------|
| 1 Review, ~701k evidence | N subject decisions, ≤32 evidence each |
| `approval-v1` fields only | + `record_id`, `capability`, `subject_id`, `source_object_id`, `subject`, `payload` |
| Unusable for SFT | Production SFT grain |

Regenerate `approval_dataset.jsonl` after upgrading. Old single-record files fail APR-004 (production scale) and APR-002/003.

Conversation / Evaluation consumers that iterate approval rows continue to work; they now see many bounded decisions instead of one mega-row.

## Public API

`generators.approval.api.generate|validate|export` and `ApprovalPipeline.generate` signatures are unchanged. `PipelineResult.approval_protocol` is now a **tuple of Reviews** (was a single Review).
