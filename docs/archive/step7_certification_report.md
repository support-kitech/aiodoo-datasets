> **Historical document.** Written when Git tags / release identity existed.
> Git tags and GitHub Releases were later removed ecosystem-wide.
> **Current source of truth:** branch `main` only. See `docs/STATUS.md`.
> Do not treat tag or release recommendations in this file as current instructions.

# Step 7 — Production Dataset Validation & Certification

**Date:** 2026-07-27  
**Scope:** Certification only (no regeneration, no generator/architecture changes)  
**Machine report:** `~/workspace/aidevelopment/step7_certification_report.json`  
**Baseline:** Step 6 regen (`docs/step6_regeneration_report.md`, `datasets/step6_regeneration_summary.json`)

## 1. Certification summary

| Check | Result |
|-------|--------|
| Schema (ValidationManager) | Pass — 0 issues on all 4 files |
| Manifests ↔ file checksums / row counts | Pass |
| Statistics presence & totals | Pass |
| Deterministic IDs + sorted export order | Pass (full scans) |
| Duplicate detection | Pass (0 duplicate IDs) |
| Production scale (N ≫ 1 for SFT) | Pass |
| Contract projection (full record set) | Pass — 0 failures |
| Generator / schema versions | 2.0.0 / 2.0 |
| Ruff | Pass |
| Unit tests (A/C/E + contract + validation rules) | Pass |
| BenchmarkCatalog `training_forbidden` | Pass (`true`) |

**Decision: Production Certified**

## 2. Dataset integrity

| Dataset | Records | IDs unique | IDs sorted | Projection OK |
|---------|--------:|:----------:|:----------:|-------------:|
| approval_dataset.jsonl | 17,094 | ✓ | ✓ | 17,094 / 17,094 |
| conversation_dataset.jsonl | 29,016 | ✓ | ✓ | 29,016 / 29,016 |
| evaluation_dataset.jsonl | 189,615 | ✓ | ✓ | 189,615 / 189,615 |
| evaluation_benchmark_catalog.jsonl | 1 | n/a | n/a | catalog rules ✓ |

Checksums match Step 6 summary and per-file manifests (no drift).

### Approval

- Subject partitioning across planner / coding / execution / repair: **5,695 / 5,459 / 5,459 / 481**
- Stable `APR-…` IDs; `review_id == record_id`
- Evidence bounded: max **32** / bound **32**
- Decision status: all **APPROVED** (17,094) — consistent with v2 policy
- No integrity defects on full scan

### Conversation

- Episodes: **5,459**; slices: **29,016**
- Stable `CNV-…` / `CONV-…` IDs; valid `turn_index`
- History prefix max **11** (bound **16**)
- Assistant-reply grain: last message assistant on **29,016 / 29,016**
- No integrity defects on full scan

### Evaluation SFT

- Judgment records: **189,615**
- Verdicts balanced: pass / fail / inconclusive = **63,205** each
- Candidate IDs `CAND-…`; case keys ∈ {pass, fail, inconclusive}
- No catalog leakage into SFT rows
- By capability_under_test: conversation 87,048 · approval 51,282 · planner 17,085 · coding 16,377 · execution 16,377 · repair 1,443 · context 3

### Benchmark catalog

- **1** record; `metadata.training_forbidden = true`
- **7** suites; **189,615** unique case refs
- Sample case refs resolve into evaluation SFT ID set
- Schema / catalog integrity: ValidationManager passed

## 3. Validation results

### ValidationManager

| File | Status | Records | Issues |
|------|--------|--------:|-------:|
| approval_dataset.jsonl | passed | 17,094 | 0 |
| conversation_dataset.jsonl | passed | 29,016 | 0 |
| evaluation_dataset.jsonl | passed | 189,615 | 0 |
| evaluation_benchmark_catalog.jsonl | passed | 1 | 0 |

### Quality gates

| Gate | Result |
|------|--------|
| Ruff (A/C/E generators, contract, validation, regen script) | exit 0 |
| Pytest (targeted unit suite) | exit 0 |
| Contract projection (project_approval / project_conversation / project_evaluation + ContractValidator) | 0 failures |

## 4. Manifest verification

| Artifact | row_count | checksum matches file + Step 6 |
|----------|----------:|:------------------------------:|
| approval_manifest.json | 17,094 | ✓ |
| conversation_manifest.json | 29,016 | ✓ |
| evaluation_manifest.json | 189,615 | ✓ |
| evaluation_benchmark_catalog_manifest.json | 1 | ✓ |

SHA-256 values identical to `datasets/step6_regeneration_summary.json`.

## 5. Statistics verification

| Stats file | total aligns with JSONL |
|------------|:-----------------------:|
| approval_statistics.json | ✓ 17,094 |
| conversation_statistics.json | ✓ 29,016 |
| evaluation_statistics.json | ✓ 189,615 |
| evaluation_benchmark_catalog_statistics.json | ✓ 1 |

Capability / verdict distributions above match deep-scan counters.

## 6. Contract verification

Full-set projection + `ContractValidator` on request/response:

| Projector | Valid pairs |
|-----------|------------:|
| `project_approval` | 17,094 |
| `project_conversation` | 29,016 |
| `project_evaluation` | 189,615 |

Benchmark catalog is excluded from SFT projection (non-training artifact).

## 7. Known follow-ups

These do **not** block dataset certification:

1. **Training adapter sync:** `aiodoo-training` `EvaluationFormatter` is still catalog-shaped — sync to contract / judgment SFT before Evaluation LoRA training.
2. **Deprecation warning:** `datetime.utcnow()` in `generators/common/export/manifest.py` (pytest noise only).
3. **JSONL not in git:** production artifacts remain gitignored; reproduce via `regenerate_v2_datasets.py` + verify against Step 6 checksums.
4. **Product merge / LoRA training:** later phases; train per-capability adapters first.

## 8. Certification decision

### Production Certified

**Justification:** All four regenerated production artifacts pass schema validation, manifest/checksum/statistics alignment with Step 6, full-scan ID uniqueness and deterministic ordering, production scale, evidence/history/verdict invariants, BenchmarkCatalog `training_forbidden` + case-ref integrity, and 100% contract projection success. Quality gates (ruff, unit tests, ValidationManager) are green. Zero certification failures; zero warnings.

Datasets certified for downstream training use (SFT files only; catalog excluded from training).
