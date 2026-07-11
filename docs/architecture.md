# Architecture Overview

The AIODOO Sources Framework is designed around three fundamental principles:
1. **Immutability:** Once source code is discovered and interpreted, it is locked into frozen deterministic Data Transfer Objects (DTOs) preventing side-effects.
2. **Transparency:** Dataset generators consume standard Python objects and remain completely oblivious to filesystem I/O, YAML parsing, caching engines, or module validation logic.
3. **Pipeline Pattern:** Execution follows a strict, one-way pipeline where data enters as raw file structures and emerges as fully assembled and validated domain graphs.

## Dependency Graph

```text
       Generators / CLI
              │
              ▼
      RepositoryManager
     (Thin Public Facade)
              │
              ▼
       SourcesPipeline
    (Central Orchestrator)
              │
     ┌────────┴────────┐
     ▼                 ▼
Cache Layer      Filesystem Layer
 (SQLite)        (YAML, os.walk)
     │                 │
     │                 ▼
     │            Loader (YAML)
     │                 │
     │                 ▼
     │         Validation Layer
     │                 │
     │                 ▼
     │              Scanner
     │                 │
     │                 ▼
     │            Interpreter
     │                 │
     │                 ▼
     └──────► ModuleFactory
                       │
                       ▼
               RepositoryBuilder
                       │
                       ▼
                RepositoryIndex
                       │
                       ▼
               RepositoryContext
              (Immutable Output)
```

## Layer Responsibilities

1. **RepositoryManager**: A highly constrained public facade. Exposes high-level intent (`load`, `refresh_cache`, `scan`) and hides pipeline orchestration internals.
2. **SourcesPipeline**: Encapsulates the sequential, deterministic order of execution. No business logic leaks out of the pipeline.
3. **Loader & Validation**: Reads `sources.yaml` and executes structural schema validation to ensure the dataset config adheres to strict typing before I/O.
4. **Cache Layer**: Intercepts `SourcesPipeline` flows. Transparently skips filesystems and interpreters by serializing/deserializing graph nodes using a SQLite persistence engine.
5. **Scanner & Interpreter**: Interrogates the underlying file system, extracts `__manifest__.py`, evaluates static AST, and bridges Odoo's internal definitions into generic `InterpretedModule` representations.
6. **Factory & Builder**: Assembles `InterpretedModule` instances into `OdooModule`s, and `OdooModule`s into `Repository` objects. It is the sole owner of object creation.
7. **RepositoryIndex**: A deduplication registry mapping repositories to unique memory hashes, preventing duplicate paths or version conflicts.
8. **RepositoryContext**: The terminal node of the pipeline. A completely frozen snapshot of the current local environment.

## Design Philosophies

### 1. Thin Manager
The `RepositoryManager` contains zero business rules. It acts as an adapter, delegating to the `SourcesPipeline` and emitting standard `PipelineResult` payloads.

### 2. Cache Transparency
No internal class natively references the cache (except `SourcesPipeline`). Caching is an orchestration feature. The `Scanner` and `Interpreter` have no knowledge of whether they are bypassing execution.

### 3. Immutable Domain
All outputs (`OdooModule`, `Repository`, `RepositoryContext`) inherit from frozen dataclasses (`frozen=True`). The output of the Sources Framework is guaranteed stable across multi-processed and multithreaded AI training generator workloads.
