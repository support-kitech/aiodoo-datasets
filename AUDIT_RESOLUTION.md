# aiodoo-datasets — Audit Resolution

Scope: production-readiness audit findings for this repository only.  
Rule: implement only Production Blocker / Bug / Documentation / Missing production implementation.  
Do not implement FUTURE WORK, INTENTIONAL, or OUT OF SCOPE.

## Batch A — tooling freeze (completed in prior commit `6656670`)

| Audit Finding | Category | Decision | Status |
| :--- | :--- | :--- | :--- |
| Installable package / broken `pip install -e .` / false README install | **BLOCKER** | Strip packaging; clone-and-run | **DONE** |
| False `generate-execution` / `aiodoo_datasets.*` API | **Documentation** | Honest README | **DONE** |
| Coverage config conflict (~54% without `.coveragerc`) | **BLOCKER** | Single pyproject coverage; fail_under 60 | **DONE** |
| CI packaging / fail-under mismatch | **Bug** | Deps-only CI; aligned fail_under | **DONE** |
| `datasets/README.md` ignored | **Documentation** | Track README; ignore artifacts | **DONE** |
| Freeze report 10/10 overclaim | **Documentation** | Honest freeze report | **DONE** |

## Batch B — v2.0.0 completion residuals (this pass)

| Audit Finding | Category | Decision | Action | Implementation Required? |
| :--- | :--- | :--- | :--- | :---: |
| `CHANGELOG.md` claims packaging, MyPy CI, execution-only API | **Documentation** | Fix | Add `[2.0.0]`; correct historical claims | **YES** |
| Missing `RELEASE_REPORT.md` | **Missing Implementation** | Fix | Write release report with gates + verdict | **YES** |
| `docs/release_checklist.md` still Pyright / >95% / sources-only | **Documentation** | Fix | Align with real ruff/pytest/coverage gates | **YES** |
| FUTURE summary “Infrastructure: Production Ready” without train-all-8 caveat | **Documentation** | Fix | Soften summary; call out sparse three | **YES** |
| No mypy in CI | **Intentional** | Leave | Do not invent repo-wide mypy gate | **NO** |
| Full regenerate all corpora for this pass | **Out Of Scope** | Leave | Validate existing `datasets/` (67,258) | **NO** |
| Approval / conversation / evaluation richness | **Future Work** | Leave | Documented deferred | **NO** |
| Approval rules `IMPLEMENTED = False` | **Intentional** | Leave | Marked stubs | **NO** |
| Missing tests for most generators | **Future Work** | Leave | Coverage omit honest | **NO** |
| Naming debt (`*_v1_0` vs `*_dataset`) | **Future Work** | Leave | FUTURE doc | **NO** |
| Automated freeze publish CI | **Out Of Scope** | Leave | Manual freeze | **NO** |
| Sibling-repo training/validation ownership | **Out Of Scope** | Leave | Boundary | **NO** |

## Implementation batch B (YES only)

1. Update this file (residual classification).
2. Fix CHANGELOG, release checklist, FUTURE summary.
3. Re-run quality gates; fix only if failing.
4. Validate existing artifact counts + training `REQUIRED_FIELDS` spot-check.
5. Write `RELEASE_REPORT.md`; refresh `IMPLEMENTATION_REPORT.md`.
6. Logical commits; recreate local annotated tag `v2.0.0`.

## Batch C — `aiodoo-contract` adoption (Phase 2, `ecosystem-v2-certification/MASTER_ACTION_LIST.md`)

Scope: adopt the canonical Capability Contract package (`aiodoo_contract`,
implemented in Phase 1B) as the single source of truth for
schemas/parsers/validators this repository previously owned independently,
and resolve the dataset-specific reliability findings assigned to this
repository. See `CONTRACT_ADOPTION.md` for the full design rationale,
including every case where duplication was deliberately **not** removed.

| Audit Finding (`MASTER_ACTION_LIST.md`) | Category | Decision | Action | Implementation Required? |
| :--- | :--- | :--- | :--- | :---: |
| ACT-005 — silent `success=True` after an exception in `execution/integration/pipeline.py` | **BLOCKER / Bug** | Fix | Exceptions in the Planning/Export phases now return `PipelineResult(success=False, diagnostics=(...))` instead of a forced-success result | **YES** |
| ACT-102 — `--resume` checkpoint semantics: a module producing zero new records was still marked "processed" | **BLOCKER / Bug** | Fix | `SharedPipelineOrchestrator`'s `"module"` strategy only checkpoints a module if `writer.written_count` actually increased | **YES** |
| ACT-103 — `generators/evaluation/api.validate()` was a no-op stub that always returned `True` | **BLOCKER / Bug** | Fix | Delegates to `EvaluationValidator`/`DatasetValidator`; fails closed on empty/malformed input or a validation exception | **YES** |
| ACT-007 / eval-corpus gap (`ARCHITECTURE_FREEZE_REPORT.md` B1/C1/DEF-05) — no repository produced a contract-conformant evaluation corpus | **Missing Implementation** | Fix | New `generators/common/contract/eval_corpus.py`, wired into `build_dataset.py` step 8b, one `<capability>_eval_corpus.jsonl` per supported capability | **YES** |
| No shared adapter from this repository's own record shapes to `aiodoo_contract`'s request/response schemas | **Missing Implementation** | Fix | New `generators/common/contract/adapters.py` (`project_<capability>`, `ContractAdapterError`) | **YES** |
| `aiodoo_contract.validators` not integrated into the validation framework | **Missing Implementation** | Fix | New `ContractComplianceRule` (`validation/rules/generators/contract_compliance.py`), registered in `RuleBuilder.build_default()`, `ValidationCategory.CONTRACT` at `WARNING` severity | **YES** |
| Orphaned `generators/evaluation/validation/protocol_validator.py` importing a nonexistent `generators.evaluation.protocol` module (found while fixing ACT-103) | **Bug (latent, newly reachable)** | Fix | Deleted the module and its `__init__.py` import/export; nothing else referenced it | **YES** |
| `DecisionEnum.CHANGES_REQUESTED` has no equivalent in `aiodoo_contract.schemas.enums.ApprovalStatus` | **Intentional divergence** | Leave, document | Adapter maps it to `PENDING` (documented lossy mapping); dataset enum retained for training signal | **NO** |
| `generators/evaluation/domain/*` (`BenchmarkCatalog`/`BenchmarkSuite`/...) vs. `aiodoo_contract.schemas.evaluation` | **Not a duplicate** | Leave, document | Different domains (multi-suite benchmark catalog vs. single capability-evaluation request/response) — nothing to import | **NO** |
| `validation/schemas/*` (`DatasetSchema`/`FieldDefinition`), generator-specific row-structure rules | **Not a duplicate** | Leave, document | Describe this repository's own JSONL row envelope; `aiodoo_contract` has no equivalent (out of its ownership per the ADRs) | **NO** |
| Raising `ContractComplianceRule` from `WARNING` to a hard failure | **Future Work** | Leave | Requires closing generator data-richness gaps first (e.g. coding artifacts with empty `content`/`diff`); tracked in `CONTRACT_ADOPTION.md` §7 | **NO** |
| Rewriting generators to natively emit `aiodoo_contract` shapes instead of projecting | **Out Of Scope** | Leave | Explicitly excluded — "dataset generators remain responsible for producing data, NOT defining contracts"; would discard training-pedagogy richness | **NO** |

### Implementation batch C

1. Add `generators/common/contract/` (adapters + eval corpus) and
   `validation/rules/generators/contract_compliance.py`; register the new
   rule in `RuleBuilder.build_default()`.
2. Fix ACT-005 (`execution/integration/pipeline.py`), ACT-102
   (`common/pipeline/orchestrator.py`), ACT-103
   (`evaluation/api.py`) and the orphaned `protocol_validator.py` import it
   exposed.
3. Wire eval-corpus generation into `build_dataset.py` (step 8b).
4. Add `generators/common/contract` and `generators/common/pipeline` to the
   `coverage` `source` allowlist in `pyproject.toml` (now meaningfully
   tested).
5. Add tests: `generators/common/contract/tests/`,
   `generators/common/pipeline/tests/test_orchestrator.py`,
   `generators/execution/tests/test_integration_pipeline_reliability.py`,
   `generators/evaluation/tests/unit/test_api_validate.py`,
   `validation/tests/unit/test_contract_compliance.py`.
6. Write `CONTRACT_ADOPTION.md`; update this file, `README.md`,
   `CHANGELOG.md`.
7. Re-run `ruff check`, `ruff format --check`, `pytest`, `coverage report
   --fail-under=60`; confirm zero net-new `mypy` errors against the
   pre-Phase-2 baseline (mypy remains intentionally out of the CI gate — see
   Batch B).
