# aiodoo-datasets — Audit Resolution

Scope: production-readiness audit findings for this repository only.  
Rule: implement only BLOCKER / HIGH / MEDIUM with **Implementation Required = YES**.  
Do not implement FUTURE WORK, INTENTIONAL, or OUT OF SCOPE.

| Audit Finding | Category | Decision | Action | Reason | Implementation Required? |
| :--- | :--- | :--- | :--- | :--- | :---: |
| Declared as installable Python package (`[build-system]` / `[project]`); `pip install -e .` fails (multiple top-level packages); README claims `pip install -e .[dev]` | **BLOCKER** | Fix | Remove packaging metadata; treat repo as clone-and-run; document `python3 build_dataset.py` + dependency install only | User requirement: not a Python package; editable install is broken and blocks documented setup | **YES** |
| README documents console script `generate-execution` and `from aiodoo_datasets.generators...` (package does not exist; no `[project.scripts]`) | **HIGH** | Fix docs | Rewrite README for real entrypoints (`build_dataset.py`, module paths under repo root) | Incorrect documentation vs actual behavior | **YES** |
| CI coverage config conflict: `pyproject.toml` measures all of `generators` + `fail_under=65`; `.coveragerc` measures framework+context only. Without `.coveragerc`, coverage ≈54% and CI `--fail-under=60` fails | **BLOCKER** | Fix | Single coverage config: honest measured surface (framework + context + approval tests already present); `fail_under=60` aligned with CI; omit untested stub/sparse generators explicitly | Broken / fragile CI | **YES** |
| CI workflow vs local gates inconsistent / packaging not needed for CI | **HIGH** | Fix | Keep dependency-only install (no editable); align fail-under with tooling config; ensure workflow matches documented gates | Broken CI / honesty | **YES** |
| `.gitignore` ignores entire `datasets/` including `datasets/README.md` (release inventory docs) | **HIGH** | Fix | Ignore build artifacts under `datasets/` but track `datasets/README.md` | Necessary documentation must not be skipped | **YES** |
| `docs/production_freeze_report.md` claims Production Ready / 10/10 while approval/conversation/evaluation are sparse stubs and coverage omit list exists | **HIGH** | Fix docs | Rewrite freeze report to honest status for repo tooling freeze `v2.0.0`; do not claim train-all-8 readiness | Incorrect documentation | **YES** |
| Approval / conversation / evaluation 1-record corpora; approval ~258MB line | **FUTURE WORK** | Leave | Already documented in `docs/FUTURE_INTEGRATION_IMPROVEMENTS.md` | Intentional deferred richness | **NO** |
| Approval rules with `IMPLEMENTED = False` | **INTENTIONAL** / **FUTURE WORK** | Leave | Marked placeholders; registered stubs documented | Not a production bug relative to documented future work | **NO** |
| Missing tests for planner/coding/repair/execution/conversation/evaluation | **FUTURE WORK** / **MEDIUM** | Defer bulk suites | Do not invent large generator test suites; keep coverage omit honest | Expanding coverage via new suites is roadmap, not required to fix CI once config is honest | **NO** |
| Execution strategy / factory `NotImplementedError` placeholders | **INTENTIONAL** | Leave | Existing stubs in deferred paths | Not required for current DAG freeze path | **NO** |
| Artifacts not versioned in git (`datasets/*.jsonl`) | **INTENTIONAL** | Leave | Build output stays gitignored; release lives outside repo (`AIODOO/datasets/...`) | Architectural boundary | **NO** |
| No automated freeze/publish job in CI | **OUT OF SCOPE** / **FUTURE WORK** | Leave | Manual freeze remains | Not required for this remediation | **NO** |
| Mixed `*_v1_0` vs `*_dataset` naming; context `manifest.json` | **FUTURE WORK** | Leave | Documented in FUTURE_INTEGRATION_IMPROVEMENTS | Naming debt deferred | **NO** |
| Manifest `generator_version` `0.1.0` vs release `v1.0.0` | **LOW** / **INTENTIONAL** | Leave | Historical artifact metadata; regenerating all corpora is out of scope | Not a CI/docs blocker for tooling freeze | **NO** |
| Hardcoded absolute paths in `config/sources.yaml` | **INTENTIONAL** | Leave | Local machine config for generation; not consumed by CI unit tests | Environment-specific | **NO** |
| Sibling repos (training/validation/model) integration gaps | **OUT OF SCOPE** | Leave | Other repositories | Boundary rule | **NO** |
| Training cannot consume huge approval blob | **OUT OF SCOPE** | Leave | Consumer-side / future dataset richness | Owned by training usage + future datasets work | **NO** |

## Implementation batch (YES only)

1. Strip packaging from `pyproject.toml` (tooling-only, match aiodoo-training posture).
2. Unify coverage config; align CI `fail-under=60`.
3. Correct README (no package / no false CLI).
4. Correct production freeze report honesty; record tooling release `v2.0.0`.
5. Adjust `.gitignore` + track `datasets/README.md`.
6. Emit `IMPLEMENTATION_REPORT.md`; run ruff / pytest / coverage; commit; annotated tag `v2.0.0`.
