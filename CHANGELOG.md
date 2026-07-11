# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-10

### Added
- **Core Generator:** Fully functional, immutable execution generator converting Python ASTs to dataset schema.
- **Integration Layer:** CLI orchestration pipeline bridging discovery to export.
- **Export Engine:** Atomic JSONL writer that securely streams datasets without data corruption.
- **Protocol Mapper:** Strict execution protocol mapper compliant with version 1.0.0 specs.
- **Validation Engine:** End-to-end integration and graph validators preventing structural anomalies.
- **Public API:** `execution.generate`, `execution.validate`, and `execution.export` entry points exposed.
- **Packaging:** Full `pyproject.toml` support for dependency and CLI entry point management.
- **Documentation:** Architecture, Pipeline, Developer, and Extension guides provided in the `docs/` folder.
- **CI/CD:** Testing pipeline for Python 3.12 with Ruff, MyPy, and Coverage gates.
