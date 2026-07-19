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
