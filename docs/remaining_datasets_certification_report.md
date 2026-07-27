# Remaining Capability Datasets — Production Certification

**Date:** 2026-07-27  
**Scope:** Certification only (no regeneration, no generator/schema/contract/architecture changes)  
**Datasets:** planner, coding, repair, execution, context  
**Machine report:** `~/workspace/aidevelopment/step7b_remaining_certification_report.json`  
**Prior:** A/C/E certified in `docs/step7_certification_report.md`

## 1. Certification summary

| Dataset | Records | ValidationManager | Manifest/checksum | Unique IDs | Content unique | Contract projection | Decision |
|---------|--------:|:-----------------:|:-----------------:|:----------:|:--------------:|--------------------:|----------|
| planner_v1_0.jsonl | 5,695 | Pass (0) | Pass | ✓ | ✓ | 5,695/5,695 | **Production Certified** |
| coding_v1_0.jsonl | 5,459 | Pass (0) | Pass | ✓ | ✓ | 5,459/5,459 | **Production Certified** |
| repair_v1_0.jsonl | 481 | Pass (0) | Pass | ✓ | ✓ | 481/481 | **Production Certified** |
| execution_dataset.jsonl | 5,459 | Pass (0) | Pass | ✓ | ✓ | 5,459/5,459 | **Production Certified** |
| context_v1_0.jsonl | 50,161 | Pass (0) | Pass | ✓ | ✓ | N/A (supporting) | **Production Certified** |

Quality gates: Ruff **pass**, targeted unit tests **pass**. Blocking failures: **0**.

**Overall decision: Production Certified**

## 2. Dataset integrity

### Identity keys (stable, unique)

| Dataset | Identity field | Format |
|---------|----------------|--------|
| Planner | `metadata.protocol_hash` | 64-hex |
| Coding | `metadata.protocol_hash` | 64-hex |
| Repair | `metadata.protocol_hash` | 64-hex |
| Execution | `output.execution_id` | 16-hex |
| Context | `id` | 64-hex |

Full-file scans: **0** duplicate identifiers, **0** duplicate record bodies.

### Required fields / invariants

- Planner: `instruction`, `input`, `output`, `metadata`; non-empty `output.tasks`
- Coding: `instruction`, `context`, `output`, `metadata`; non-empty `output.artifacts`
- Repair: `instruction`, `context`, `output`, `metadata`; non-empty `output.tasks`
- Execution: `instruction`, `output`, `metadata`; non-empty `output.steps`
- Context: `id`, `query`, `artifacts`, `graph`, `metadata`

Generation-time `duplicate_count` in statistics (skipped during build) is **not** residual file duplication:

| Dataset | stats.duplicate_count (skipped) | duplicates in final JSONL |
|---------|--------------------------------:|:-------------------------:|
| Planner | 762 | 0 |
| Coding | 998 | 0 |
| Repair | 59 | 0 |
| Execution | 0 | 0 |
| Context | 51,443 | 0 |

## 3. Validation results

| Gate | Result |
|------|--------|
| ValidationManager (all 5 files) | passed, 0 issues |
| Ruff (generators + contract + validation) | exit 0 |
| Pytest (contract, schemas, manager, context, execution) | exit 0 |
| ContractValidator on projections | 0 malformed request/response |

## 4. Manifest verification

| Dataset | Manifest file | row_count | checksum matches JSONL |
|---------|---------------|----------:|:----------------------:|
| Planner | planner_manifest.json | 5,695 | ✓ |
| Coding | coding_manifest.json | 5,459 | ✓ |
| Repair | repair_manifest.json | 481 | ✓ |
| Execution | execution_manifest.json | 5,459 | ✓ |
| Context | manifest.json | 50,161 | ✓ |

Generator version in manifests: **0.1.0**. Schema IDs: **planner-v1 / coding-v1 / repair-v1 / execution-v1 / context-v1** (schema version **1.0.0**).

## 5. Statistics verification

| Stats file | total_samples matches JSONL |
|------------|:---------------------------:|
| planner_statistics.json | ✓ 5,695 |
| coding_statistics.json | ✓ 5,459 |
| repair_statistics.json | ✓ 481 |
| execution_statistics.json | ✓ 5,459 |
| statistics.json (context) | ✓ 50,161 |

Context query types (live = stats): `find_field` 34,295 · `find_model` 15,866.

Planner/coding scenario labels in statistics use the **primary** scenario string; live `metadata.scenario` is a tag list — counts align at the primary-label level used by the exporter (not a row-count drift).

## 6. Contract verification

| Projector | Valid pairs |
|-----------|------------:|
| `project_planner` | 5,695 |
| `project_coding` | 5,459 |
| `project_repair` | 481 |
| `project_execution` | 5,459 |

**Context:** not a contract `CapabilityName` (`CONTRACT_ADOPTION.md` / `SUPPORTED_CAPABILITIES`). Certified on schema + integrity only; no `project_context`.

## 7. Reproducibility verification

| Check | Result |
|-------|--------|
| Manifest SHA-256 ↔ file | Pass (all 5) |
| Unique stable IDs | Pass |
| Unique content hashes | Pass |
| Lexicographic ID sort | Not required for v1 (deterministic generation/export order; checksum is source of truth) |

## 8. Known follow-ups

### Blocking

None.

### Non-blocking

1. **v1 ID order:** exports are not lexicographically sorted by protocol_hash / execution_id / id (unlike A/C/E v2). Reproducibility is via checksum + deterministic pipelines.
2. **Context sidecar naming:** writes `manifest.json` / `statistics.json` instead of `context_manifest.json` / `context_statistics.json` — easy to overwrite if another generator uses the same names.
3. **`datetime.utcnow()` deprecation** in checkpoint/manifest helpers (pytest warnings only).
4. **Scenario stats shape:** planner/coding statistics store primary scenario string; records store tag lists — cosmetic reporting difference only.

## 9. Certification decision

### Production Certified

All five remaining production datasets pass schema validation, manifest/checksum/statistics alignment, identifier and content uniqueness, production scale, and (where applicable) 100% contract projection.

**Approved for downstream LoRA training** (planner, coding, repair, execution; context as supporting corpus).
