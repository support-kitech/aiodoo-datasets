# Contract Adoption (Phase 2)

Scope: how `aiodoo-datasets` consumes `aiodoo_contract` (the canonical
Capability Contract package — see `ecosystem-v2-certification/
ARCHITECTURE_FREEZE_REPORT.md` and the ADRs in `aiodoo-contract/docs/adr/`).

This document records **what was adopted, how, and why**, and — per the
ADR-0005/ADR-0007 ownership rules ("everything shared lives in exactly one
place") — every case where this repository still defines something of its
own, with the reason it is not a duplicate contract.

## 1. What "adoption" means here

`aiodoo-datasets` generators do not produce `CapabilityRequest`/
`CapabilityResponse` pairs directly. Each generator's JSONL record is a rich,
training-pedagogy-oriented structure (e.g. Planner emits `goal`/`tasks` with
priorities and rationale; Repair emits `problem`/`root_cause`/
`expected_outcome`) that predates `aiodoo_contract` and is deliberately more
detailed than the lean request/response the contract defines for runtime
inference. Rewriting eight generators' domain models to *be* the contract
schema would have discarded that training richness and was explicitly not
requested ("dataset generators remain responsible for producing data, NOT
defining contracts").

Instead, `aiodoo-datasets` adopts the contract through an **adapter
(projection) layer**: `generators/common/contract/adapters.py`. For every
supported capability, `project_<capability>(record) -> ContractProjection`
maps this repository's own record shape onto the exact
`aiodoo_contract.schemas.<capability>.<Capability>Request`/`Response` Pydantic
models — the same models `aiodoo-training`, `aiodoo-validation`, and
`aiodoo-core` import. Malformed input raises `ContractAdapterError` (never a
bare `KeyError`/`TypeError`), so callers can distinguish "this record isn't
representable in the contract" from a real bug in the adapter.

This projection is then used for two purposes, both of which run the
*canonical* validator (`aiodoo_contract.validators.ContractValidator`) — never
a hand-rolled equivalent:

1. **Validation framework integration** — `validation/rules/generators/
   contract_compliance.py`'s `ContractComplianceRule` (one instance per
   capability, registered in `validation/builders/rule_builder.py`) projects
   every record and validates the projection during `python3
   build_dataset.py`'s existing validation pass.
2. **Evaluation corpus generation** — `generators/common/contract/
   eval_corpus.py`'s `build_eval_corpus`/`write_eval_corpus` (Section 3).

## 2. Evaluation corpora (ACT-007 / architecture audit gap)

The architecture freeze report and `MASTER_ACTION_LIST.md` identified that
**no repository produced a contract-conformant evaluation corpus** — a
certification/validation blocker (tracked as the eval-corpus gap, `B1`/`C1`/
`DEF-05` in `ecosystem-v2-certification/ARCHITECTURE_FREEZE_REPORT.md`).

`generators/common/contract/eval_corpus.py` closes this gap. For each
capability in `generators.common.contract.adapters.SUPPORTED_CAPABILITIES`
(`planner`, `coding`, `repair`, `execution`, `conversation`, `approval`):

1. Deterministically samples up to `DEFAULT_SAMPLE_SIZE` records from that
   capability's already-generated training dataset (stable ordering by
   content hash — no randomness, so `--resume`/re-runs are reproducible).
2. Projects each sampled record via `project_record` and validates it with
   `ContractValidator`. Records that fail projection or validation are
   skipped and counted, never silently included.
3. Writes `<capability>_eval_corpus.jsonl` (each line: `capability`,
   `request`, `expected_response`, `source_protocol_hash`), plus a manifest
   and statistics file, via the same `DatasetWriter` every other generator
   uses.

This is wired into `build_dataset.py` as step "8b", after the existing
per-capability generators and the (separate, richer) `evaluation` generator's
own dataset (`generators/evaluation/`, which evaluates cross-capability
benchmarks — see Section 5). `build_dataset.py` raises if any capability
produces zero contract-valid cases, so a regression in the adapter layer
fails the build instead of silently shipping an empty/broken eval corpus.

## 3. Reliability fixes (dataset-specific items from the audit)

| ID | Finding | Fix | Test |
| :--- | :--- | :--- | :--- |
| ACT-005 | `generators/execution/integration/pipeline.py` caught exceptions in the Planning/Export phases and reported `success=True` with an empty result — a silent success. | Exceptions now propagate as `PipelineResult(success=False, diagnostics=(...),...)` with the original exception repr, plus `logger.exception(...)`. | `generators/execution/tests/test_integration_pipeline_reliability.py` |
| ACT-102 | `generators/common/pipeline/orchestrator.py`'s `"module"` checkpoint strategy called `checkpoint.save(...)` unconditionally, so a module that produced zero *new* records in a run was marked "processed" — a future `--resume` would never retry it. | `checkpoint.save(...)` is now only called if `writer.written_count` increased during that module's processing; otherwise a warning is logged and the module is left un-checkpointed so `--resume` retries it. | `generators/common/pipeline/tests/test_orchestrator.py` |
| ACT-103 | `generators/evaluation/api.py`'s `validate()` was a no-op stub that always returned `True` regardless of input (comment: "Protocol validation removed"). | Delegates to the real domain validators (`EvaluationValidator`, `DatasetValidator`); fails closed (`False`) on an empty dataset, a non-`Evaluation` element, or any validation/unexpected exception. | `generators/evaluation/tests/unit/test_api_validate.py` |
| (found while fixing ACT-103) | `generators/evaluation/validation/protocol_validator.py` imported `generators.evaluation.protocol.domain.benchmark_protocol`, a module that does not exist anywhere in this repository (orphaned from an earlier "protocol layer removed" refactor — see the `# Protocol ... removed` comments throughout `generators/evaluation/`). This was previously unreachable dead code — `generators/evaluation/validation/__init__.py` imported it unconditionally, but nothing imported `dataset_validator`/`evaluation_validator` through the package `__init__` until ACT-103's fix did, which would have made `evaluation.api.validate()` crash at import time. | Deleted `protocol_validator.py` and removed its import/`__all__` entry from `validation/__init__.py`. Nothing else referenced `ProtocolValidator` (searched the whole repo — see `git log`/grep in the implementation PR). | Covered indirectly by every test in `generators/evaluation/tests/` and `generators/common/contract/tests/` (all of which import through `generators.evaluation.api` or `generators.evaluation.validation`). |

## 4. Duplication that was **not** removed, and why

Per the primary goal ("if duplication cannot be removed, document the
reason"), the following were audited against `aiodoo_contract` and
deliberately **not** replaced with imports:

- **`generators/approval/enums.py:DecisionEnum`** vs.
  `aiodoo_contract.schemas.enums.ApprovalStatus` — `DecisionEnum` has a
  `CHANGES_REQUESTED` member with no equivalent contract state (the contract
  only models `pending`/`approved`/`rejected` — a genuinely leaner runtime
  state machine than this repository's training-time review taxonomy). The
  adapter (`project_approval`) maps `CHANGES_REQUESTED` → `ApprovalStatus.
  PENDING` as a documented, lossy-but-closest mapping (see the comment above
  `_DECISION_STATUS_MAP` in `adapters.py`) — it is not claimed to be
  equivalent. The dataset-side enum is retained because collapsing it to the
  contract's three states would lose real training signal (the model should
  learn to distinguish "needs changes" from "rejected").
- **Per-generator `Severity`-shaped enums** (e.g. repair's
  `problem.severity` string field) vs. `aiodoo_contract.schemas.enums.
  Severity` — several generators use different granularity/casing for
  severity than the contract's canonical enum. Where a generator's severity
  feeds a contract projection (repair's confidence heuristic in
  `adapters.py`), the adapter normalizes the raw string itself rather than
  importing the generator's own enum; the contract's `Severity` enum is not
  otherwise threaded through generator-internal domain models, because those
  models predate and are more detailed than the contract's needs.
- **`generators/evaluation/domain/*`** (`BenchmarkCatalog`, `BenchmarkSuite`,
  `EvaluationCase`, `GroundTruth`, ...) — this is a *different, larger*
  domain than `aiodoo_contract.schemas.evaluation.EvaluationRequest/
  Response`. The evaluation generator produces multi-suite, multi-case
  *benchmark catalogs* for cross-capability regression testing; the contract's
  `EvaluationRequest`/`Response` model a single capability-evaluation
  request/response pair. These are complementary, not duplicate, concerns —
  there is nothing in `aiodoo_contract` to import here. (The `eval_corpus.py`
  producer added in Section 2 is the piece that *does* use the contract's
  evaluation-relevant request/response shapes, per-capability.)
- **`generators/*/validation/core_validator.py:CoreProtocolValidator`** — these
  wrap the *separate*, pre-existing `aiodoo.validator.ProtocolValidator`
  (an external/optional dependency, imported defensively with a
  `try`/`except ImportError` fallback) used for semantic domain-object
  validation during generation (e.g. planner task graphs). This is unrelated
  to `aiodoo_contract` — it is not a competing contract, and nothing in
  `aiodoo_contract` replaces it.
- **`validation/schemas/*` (`DatasetSchema`, `FieldDefinition`)** — these
  describe this repository's own JSONL row envelope
  (`instruction`/`context`/`output`/`metadata`), which is a
  dataset-file-format concern specific to `aiodoo-datasets`, not a capability
  request/response contract. `aiodoo_contract` has no equivalent, and the
  Architecture Freeze Report does not assign row-envelope ownership to it.

## 5. What `aiodoo_contract.validators` now covers vs. what stays local

- **New**: `ContractComplianceRule` (`validation/rules/generators/
  contract_compliance.py`) runs `aiodoo_contract.validators.
  ContractValidator` against every record's projection, for every supported
  capability, as part of the existing validation pipeline
  (`ValidationCategory.CONTRACT`, `WARNING` severity — see the module
  docstring for why this is a warning, not a hard failure, today).
- **Unchanged (intentionally)**: `RequiredFieldsRule`, `FieldTypeRule`,
  `RecordStructureRule`, and the generator-specific rules in `validation/
  rules/generators/*.py` (e.g. `RepairTaskStructureRule`) continue to check
  this repository's own row envelope and generator-internal invariants
  (e.g. "task IDs must be non-empty", "no circular artifact dependencies").
  These are not contract concerns — `aiodoo_contract` does not define a JSONL
  row format or generator-internal task-graph rules — so there is no
  overlapping/competing validator to remove.

## 6. Backward compatibility

- Every existing generator's produced dataset format, field names, and CLI
  behavior are unchanged. The adapter layer is additive (new module,
  new validation rule at `WARNING` severity, new `8b` eval-corpus step); no
  existing generator output changed shape.
- The two exceptions are the reliability fixes in Section 3: a pipeline run
  that previously **silently reported success** on an unhandled exception
  (ACT-005) or **silently marked an empty module as done** (ACT-102) will now
  surface as an explicit failure / retry-on-resume. This is an intentional,
  audit-mandated behavior change — the old behavior was a correctness bug,
  not a feature.
- `generators/evaluation/api.validate()` (ACT-103) previously always returned
  `True`; a caller that depended on that stub behavior for a malformed
  dataset will now correctly receive `False`. No caller was found that relied
  on this in this repository (`git grep` for `evaluation.api.validate` inside
  `aiodoo-datasets`), but any downstream consumer relying on the old always-
  `True` behavior should adjust.

## 7. Deferred / out of scope for this phase

- Broadening the `WARNING`-severity `ContractComplianceRule` to a hard
  failure once every generator's data-richness gaps (see the adapter
  docstrings, e.g. coding artifacts with empty `content`/`diff`) are closed.
  Tracked, not implemented here, to avoid breaking existing `build_dataset.py`
  runs on today's data.
- Full closure of the "Approval / conversation / evaluation richness" gap
  documented in `docs/FUTURE_INTEGRATION_IMPROVEMENTS.md` — unrelated to
  contract adoption and explicitly out of scope for Phase 2.
- Any change to `aiodoo-training`, `aiodoo-validation`, `aiodoo-model`,
  `aiodoo-core`, `aiodoo-vscode`, `aiodoo-colab`, or `aiodoo-contract` itself
  — out of scope per Phase 2's instructions.
