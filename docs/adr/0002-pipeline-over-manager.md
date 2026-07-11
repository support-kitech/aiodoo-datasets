# ADR-0002: Pipeline Over Manager

## Decision
The `RepositoryManager` remains a thin façade that exposes high-level intent (e.g., `load`, `scan`). All actual business logic and execution flow resides within the strictly ordered `SourcesPipeline`.

## Rationale
Separating the public API (`RepositoryManager`) from the orchestration logic (`SourcesPipeline`) adheres to the Single Responsibility Principle. If the public manager contained pipeline logic, it would easily become bloated as features (like caching, loading, scanning, building) expanded. 

## Alternatives Considered
- **Fat Manager:** Putting all logic into `RepositoryManager`. This was rejected because it violates SRP, merges API concerns with internal execution concerns, and makes unit testing difficult.
- **Direct Pipeline Exposure:** Allowing downstream code to instantiate `SourcesPipeline` directly. This was rejected because the pipeline requires complex constructor injections (Cache, Loader, Scanner) which the consumer shouldn't need to know about.

## Consequences
- **Positive:** `RepositoryManager` stays stable, lightweight, and cleanly defines the boundary of the AIODOO ecosystem. `SourcesPipeline` remains independently testable and modular.
- **Negative:** A slight indirection is introduced where `manager.load()` immediately delegates to `pipeline.execute()`.
