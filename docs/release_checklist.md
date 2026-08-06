# Release Checklist (aiodoo-datasets v2.0.x)

Use this checklist before tagging a tooling release. This repository is
**clone-and-run** (not PyPI). Dataset JSONL artifacts are gitignored; release
inventory is described in `datasets/README.md`.

### 1. Static analysis

- [ ] **Ruff**: `ruff check .` passes
- [ ] **Ruff format**: `ruff format --check .` passes
- [ ] **MyPy**: not required for this repository (intentionally out of CI)

### 2. Automated testing

- [ ] **Pytest**: `coverage run -m pytest` passes
- [ ] **Coverage**: `coverage report -m --fail-under=60` passes
- [ ] Coverage measures framework + context + approval only (see `pyproject.toml` omit list)

### 3. Pipeline / artifacts

- [ ] Local `datasets/*.jsonl` line counts match freeze inventory (or regenerate via `python3 build_dataset.py` when Odoo sources are configured)
- [ ] First-record field contracts compatible with `aiodoo-training` `REQUIRED_FIELDS`
- [ ] Sparse approval / conversation / evaluation still documented as non-training-scale

### 4. Documentation

- [ ] `README.md` matches clone-and-run reality (no `pip install -e .`, no false console scripts)
- [ ] `docs/production_freeze_report.md` does not overclaim train-all-8 readiness
- [ ] `CHANGELOG.md` has a section for the release version
- [ ] `archive/RELEASE_REPORT.md` written for the release on main

### 5. Versioning

- [ ] Annotated tag `vX.Y.Z` created on the commit that contains the above
- [ ] Do not move historical tags once published to remote
