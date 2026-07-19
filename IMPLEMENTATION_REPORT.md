# aiodoo-datasets — Implementation Report (v2.0.0 tooling freeze)

## 1. Modified files

| File | Why |
| --- | --- |
| `pyproject.toml` | Removed installable `[build-system]` / `[project]`; tooling-only coverage/ruff/pytest aligned with CI (`fail_under=60`, honest omit list) |
| `.github/workflows/ci.yml` | Documented no editable install; coverage gate comment |
| `.gitignore` | Track `datasets/README.md` while ignoring build artifacts |
| `README.md` | Removed false `pip install -e`, `generate-execution`, and `aiodoo_datasets.*` claims |
| `docs/production_freeze_report.md` | Replaced overclaim 10/10 with honest scores and train-all-8 = NO |

## 2. New files

| File | Why |
| --- | --- |
| `AUDIT_RESOLUTION.md` | Mandatory finding classification before code changes |
| `IMPLEMENTATION_REPORT.md` | This report |
| `datasets/README.md` (now tracked) | Release inventory was gitignored; honest record counts |

## 3. Deleted files

| File | Why |
| --- | --- |
| `.coveragerc` | Consolidated into `pyproject.toml` so CI cannot silently diverge |

## 4. Before → After

| Topic | Before | After |
| --- | --- | --- |
| Packaging | Declared package; `pip install -e .` fails (multiple top-level packages) | Not a package; deps-only install |
| README | Console script + fake package imports | `python3 build_dataset.py` + real module paths |
| Coverage | `.coveragerc` vs `pyproject` conflict; bare `generators` → ~54% if coveragerc missing | Single config; measured surface ~81%; fail_under 60 |
| Freeze report | Production Ready 10/10 | Honest metrics; tooling v2.0.0; sparse corpora called out |
| `datasets/README.md` | Ignored by `datasets/` | Tracked; artifacts still ignored |

## 5. Architecture impact

None. No generators moved, no DAG changes, no new abstractions.

## 6. Test impact

No new product tests. Existing suite: **264 passed**. Coverage gate still 60% on the honest measured surface.

## 7. Backward compatibility

- Callers already using repo-root imports (`from sources…`, `from generators…`) unchanged.
- Anyone relying on `pip install -e .` or `aiodoo_datasets` namespace was already broken; docs now match reality.
- Dataset **artifact** version remains **v1.0.0**; repository **tooling** tag is **v2.0.0**.

## 8. Breaking changes

Documentation / packaging posture only. No protocol or generator API redesign.

## 9. Future work left intentionally untouched

- Approval / conversation / evaluation corpus expansion
- Completing stub approval rules
- Generator test suites for planner/coding/repair/execution/conversation/evaluation
- Automated freeze/publish CI job
- Naming unification (`*_v1_0` vs `*_dataset`, context `manifest.json`)
- Regenerating manifests to bump `generator_version`
- Hardcoded `config/sources.yaml` paths
- Sibling-repo training/validation/model integration

## 10. Quality gate results (local)

```
ruff check .          → passed
ruff format --check . → passed
coverage run -m pytest → 264 passed
coverage report --fail-under=60 → ~81%
```

`mypy` is not part of this repository’s GitHub workflow (unlike `aiodoo-training`); not added here to avoid inventing a new gate across hundreds of untyped modules.
