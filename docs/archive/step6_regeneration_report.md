> **Historical document.** Written when Git tags / release identity existed.
> Git tags and GitHub Releases were later removed ecosystem-wide.
> **Current source of truth:** branch `main` only. See `docs/STATUS.md`.
> Do not treat tag or release recommendations in this file as current instructions.

# Step 6 — Production Dataset Regeneration Report

**Date:** 2026-07-27  
**Method:** `python3 regenerate_v2_datasets.py` (upstream JSONL reused; no architecture changes)  
**Log:** `~/workspace/aidevelopment/step6_regen.log`  
**Validation:** `~/workspace/aidevelopment/step6_validation_report.json`

## 1. Dataset counts

| Dataset | Records | Size |
|---------|--------:|-----:|
| approval_dataset.jsonl | 17,094 | 211 MB |
| conversation_dataset.jsonl | 29,016 | 47 MB |
| evaluation_dataset.jsonl | 189,615 | 408 MB |
| evaluation_benchmark_catalog.jsonl | 1 | 41 MB |

## 2. Statistics (highlights)

**Approval:** 17,094 samples; by_capability planner 5,695 / coding 5,459 / execution 5,459 / repair 481; max_evidence_items 32; duplicates 0.

**Conversation:** 29,016 training examples; 5,459 episodes; avg ~6.37 messages/turn; duplicates 0.

**Evaluation SFT:** 189,615 judgments; verdict mix pass/fail/inconclusive = 63,205 each; duplicates 0.

**BenchmarkCatalog:** 1 record; `training_forbidden=true`; 7 suites.

## 3. Validation summary

All four files: **PASSED**, 0 issues (schema, identity, scale, catalog rules, contract projection rules as applicable).

## 4. Manifest summary

| Manifest | row_count | checksum (sha256 prefix) |
|----------|----------:|--------------------------|
| approval_manifest.json | 17,094 | a4979342d1215136… |
| conversation_manifest.json | 29,016 | d295d7678cdc99a5… |
| evaluation_manifest.json | 189,615 | 8a25166d6d0a3804… |
| evaluation_benchmark_catalog_manifest.json | 1 | 7560b11c16d334c5… |

Full checksums: `datasets/step6_regeneration_summary.json`.

## 5. Generator versions

| Generator | Version |
|-----------|---------|
| Approval | 2.0.0 |
| Conversation | 2.0.0 |
| Evaluation | 2.0.0 |

## 6. Schema versions

| Schema | ID / version |
|--------|----------------|
| Approval | approval-v2 / 2.0 |
| Conversation | conversation-v2 / 2.0 |
| Evaluation SFT | evaluation-v2 / 2.0 |
| BenchmarkCatalog | benchmark-catalog-v1 / 1.0 |

## 7. Migration confirmation

| Placeholder | Replaced |
|-------------|----------|
| 1-row Approval (~247 MB mega-evidence) | 17,094 subject decisions |
| 1-row Conversation | 29,016 next-reply slices |
| 1-row Evaluation catalog-as-SFT | 189,615 judgments + separate catalog |

## 8. Final verification

| Check | Result |
|-------|--------|
| Production-scale (N≫1) | Pass |
| Deterministic ID sort (prefix 5k) | Pass |
| Unique IDs (prefix 5k) | Pass |
| Contract projection samples | Pass |
| Catalog not SFT | Pass (`training_forbidden`) |
| Ruff on regen script | Pass |
| Architecture / contracts unchanged | Confirmed |
