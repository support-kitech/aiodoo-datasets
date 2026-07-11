# Release Checklist

This checklist must be rigorously followed before tagging any official release (e.g., v1.0.0, v1.1.0) of the AIODOO Sources Framework. Due to its foundational role across all AI training datasets, instability here causes systemic failures downstream.

### 1. Static Analysis & Typing
- [ ] **Ruff**: `ruff check sources/ generators/` passes with 0 errors.
- [ ] **Pyright**: `pyright sources/ generators/` passes with 0 errors.
- [ ] **MyPy**: (Future consideration, ensure structural compatibility).

### 2. Automated Testing
- [ ] **Unit Tests**: `pytest sources/tests/unit/` passes.
- [ ] **Integration Tests**: `pytest sources/tests/integration/` (if any) passes.
- [ ] **CLI Tests**: `test_cli.py` executes successfully.
- [ ] **End-to-End Tests**: All `generators/*/tests/` pass, proving the Framework adapter (`ContextModuleScanner`) is functionally identical to the legacy filesystem scanner.
- [ ] **Test Coverage**: Ensure `pytest --cov=sources` remains >95%.

### 3. Pipeline Validation
- [ ] **build_dataset.py**: Run `python3 build_dataset.py`. Verify that the orchestrator correctly identifies repositories and triggers standard dataset pipelines without throwing `SourcesError`.
- [ ] **Cache Validation**: 
  - Ensure modifying `sources.yaml` instantly triggers cache invalidation.
  - Ensure `aiodoo-sources cache-info` outputs correct HIT/MISS metadata.
  - Verify SQLite file sizes remain predictable.

### 4. Code & Architecture Review
- [ ] **Public API Review**: Ensure `sources/__init__.py` has not accidentally exported internal modules.
- [ ] **Dependency Review**: Verify `generators` **do not** directly import `sources.core`, `sources.cache`, or `sources.pipeline`.
- [ ] **Circular Import Check**: Validate that `sources.domain` never imports `sources.core`.
- [ ] **Documentation Review**: Read `docs/public_api.md` and `docs/architecture.md` to ensure they accurately reflect code state.

### 5. Final Versioning
- [ ] Update `SOURCES_FRAMEWORK_VERSION` in `sources/constants/framework.py`.
- [ ] Update any references in `docs/` or `README.md`.
