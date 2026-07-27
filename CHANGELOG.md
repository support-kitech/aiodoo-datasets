# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Conversation generator v2 (Step 4):** episode reconstruction + dialogue slicing —
  one JSONL record per assistant reply with bounded history, stable
  `record_id` (`conversation_id` + `turn_index` + `id_scheme_version`),
  deterministic ordering, and production-scale validation (CNV-002..004).
  Approval is a soft upstream dependency. Schema `conversation-v2`.
  See `generators/conversation/README.md`.
- **Approval generator v2 (Step 3):** subject-partitioned training grain — one JSONL
  record per planner/coding/repair/execution subject with bounded evidence,
  stable `record_id` (`capability` + `subject_id` + `source_object_id` +
  `id_scheme_version`), deterministic ordering, and production-scale validation
  (APR-002..004). Schema `approval-v2`. See `generators/approval/README.md`.

### Added

- `aiodoo_contract` adopted as the canonical Capability Contract dependency
  (see `CONTRACT_ADOPTION.md`).
- `generators/common/contract/adapters.py`: projects each capability's own
  record shape onto `aiodoo_contract`'s `CapabilityRequest`/
  `CapabilityResponse` schemas (`project_planner`, `project_coding`,
  `project_repair`, `project_execution`, `project_conversation`,
  `project_approval`, `project_record`).
- `generators/common/contract/eval_corpus.py`: per-capability, contract-
  conformant evaluation corpus generation (`<capability>_eval_corpus.jsonl`),
  wired into `build_dataset.py` (step 8b). Closes the "no eval-corpus
  producer" architecture-audit gap (ACT-007 / DEF-05).
- `validation/rules/generators/contract_compliance.py`: `ContractComplianceRule`
  runs `aiodoo_contract.validators.ContractValidator` against every record's
  projection, one rule instance per supported capability
  (`ValidationCategory.CONTRACT`, `WARNING` severity).
- Tests: `generators/common/contract/tests/`,
  `generators/common/pipeline/tests/test_orchestrator.py`,
  `generators/execution/tests/test_integration_pipeline_reliability.py`,
  `generators/evaluation/tests/unit/test_api_validate.py`,
  `validation/tests/unit/test_contract_compliance.py`.
- `CONTRACT_ADOPTION.md`.

### Fixed

- **ACT-005**: `execution/integration/pipeline.py` no longer reports a
  forced `success=True` when the Planning or Export phase raises; it now
  returns `PipelineResult(success=False, diagnostics=(...))` and logs the
  exception.
- **ACT-102**: `common/pipeline/orchestrator.py`'s `"module"` checkpoint
  strategy no longer marks a module "processed" if it contributed zero new
  written records, so `--resume` correctly retries it.
- **ACT-103**: `generators/evaluation/api.validate()` no longer always
  returns `True`; it delegates to `EvaluationValidator`/`DatasetValidator`
  and fails closed on empty/malformed/invalid input.
- Removed `generators/evaluation/validation/protocol_validator.py`, which
  imported a nonexistent `generators.evaluation.protocol` module (orphaned
  dead code from an earlier "protocol layer removed" refactor, made newly
  reachable — and therefore import-fatal — by the ACT-103 fix).

### Changed

- `pyproject.toml` coverage `source` now includes `generators/common/contract`
  and `generators/common/pipeline` (both now have substantial tests).

## [2.0.0] - 2026-07-19

### Changed

- Repository is **not** an installable Python package (tooling-only `pyproject.toml`)
- README documents clone-and-run via `python3 build_dataset.py` (no false console scripts)
- Coverage gate unified in `pyproject.toml` (`fail_under=60`; honest measured surface)
- Production freeze report and dataset inventory README made honest (train-all-8 = NO)
- `.gitignore` tracks `datasets/README.md` while ignoring build artifacts

### Added

- `AUDIT_RESOLUTION.md`, `IMPLEMENTATION_REPORT.md`, `RELEASE_REPORT.md`

### Not in this release

- Approval / conversation / evaluation corpus richness
- Repo-wide mypy gate (intentionally out of CI)
- Automated freeze/publish workflow

## [1.0.0] - 2026-07-10

### Added (historical)

- Execution generator and shared export/validation infrastructure
- Full eight-capability DAG via `build_dataset.py` (later commits)
- Sources / preprocessing / protocol / validation frameworks
- CI: Ruff + pytest + coverage on Python 3.12 (source checkout; no editable install)

### Notes

Historical packaging / MyPy / console-script claims in early docs were incorrect
and are superseded by the **v2.0.0** tooling freeze. Prefer the v2.0.0 tag for
current release identity.
