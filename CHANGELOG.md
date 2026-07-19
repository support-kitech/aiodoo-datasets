# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
