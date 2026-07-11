# Public API Specification

The AIODOO Sources Framework v1.0.0 exposes a strictly minimized public API to ensure extreme stability for generators while allowing internal logic (caching, parsing, validation) to evolve transparently.

## Stable Public API

The official interface is exported in `sources/__init__.py`. External generators must **only** import from `sources`.

```python
from sources import (
    RepositoryManager,
    PipelineOptions,
    PipelineResult,
    RepositoryContext,
    Repository,
    OdooModule,
    SourcesError,
    __version__,
    SOURCES_FRAMEWORK_VERSION,
)
```

### `RepositoryManager`
The primary facade of the framework. It encapsulates all state and internal lifecycle management.
- **`__init__(cache_db_path: Path)`**: Initializes the manager with a transparent SQLite cache.
- **`load(config_path: Path, options: PipelineOptions = None) -> PipelineResult`**: Safely loads, parses, caches, and returns a contextual model of the source environment. This is the only method generators should invoke.
- **`refresh_cache(config_path: Path) -> PipelineResult`**: Clears and aggressively rebuilds the cache.
- **`clear_cache() -> None`**: Wipes the active SQLite cache.

### `PipelineOptions`
A strictly typed, immutable dataclass controlling pipeline execution.
- `force_rescan` (bool): Bypass caching, force I/O scanning.
- `skip_cache` (bool): Do not use caching.
- `validate_only` (bool): Parse configurations and halt.
- `scan_only` (bool): Discover files, bypass interpretation.

### `PipelineResult`
A deterministic output payload.
- `success` (bool)
- `context` (Optional[RepositoryContext]): The resulting immutable context on success.
- `errors` (tuple[str, ...])
- `warnings` (tuple[str, ...])
- `statistics` (PipelineStatistics): Runtime execution metrics.

### Domain Models
Domain models are immutable, frozen dataclasses. Generators safely consume them without side effects.
- **`RepositoryContext`**: A unified wrapper containing a collection of `Repository` instances.
- **`Repository`**: Represents an isolated git/local repository mapped to an Odoo version. Contains `modules`.
- **`OdooModule`**: A fully interpreted, deterministic representation of a discovered Odoo module (name, path, edition, dependencies, hashes).

### `SourcesError`
The base exception class for fatal errors emitted by the framework, cleanly handled by the internal CLI.

---

## Internal / Private API (Forbidden)

The following components are strictly **internal implementation details**. They must **never** be imported by external tools or dataset generators. Modifying or importing these components will break pipeline stability.

### Discovery & Loader Layer
- `RepositoryLoader`
- `RepositoryScanner`
- `RepositoryInterpreter`

### Instantiation Layer
- `ModuleFactory`
- `RepositoryBuilder`
- `ManifestBuilder`

### State Management
- `CacheStore`
- `CacheInvalidator`
- `RepositorySerializer`
- `RepositoryDeserializer`

### Pipeline Internals
- `SourcesPipeline`
- `RepositoryIndex`
- `ConfigValidator`
