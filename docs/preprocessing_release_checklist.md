# Release Checklist v1.0.0

- [x] Architecture matches the approved specification
- [x] CLI exposes `normalize`, `validate`, `summary`, `cache-info`, `cache-clear`, `refresh-cache`, `benchmark`
- [x] Cache is fully deterministic and strictly separates JSON mapping from SQLite storage
- [x] All processors execute under a strict immutable context
- [x] Processor priority uses constants, no magic numbers
- [x] All tests pass
- [x] `ruff check --fix` is completely clean
- [x] `pyright` is completely clean
- [x] `build_dataset.py` explicitly injects `PreprocessingManager`
- [x] `__version__` exported accurately
