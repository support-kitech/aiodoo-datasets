# ADR-0004: No Generator YAML Parsing

## Decision
Dataset generators (`PlannerPipeline`, `CodingPipeline`, etc.) are explicitly forbidden from directly reading, parsing, or interacting with `sources.yaml` or any filesystem representations of repository state. They must exclusively consume the `RepositoryContext` domain object.

## Rationale
Historically, generators duplicated the logic to read `sources.yaml`, traverse the OS filesystem, check for missing manifests, and load static files. This caused code bloat, fragile paths, and prevented centralized performance improvements. By forcing all generators to consume `RepositoryContext`, we guarantee that if the underlying infrastructure changes (e.g., pulling repositories from a remote database instead of disk), the generators require absolutely zero code changes.

## Alternatives Considered
- **Shared Utils Module:** Providing a `parse_yaml()` utility to all generators. Rejected because the generators still own the orchestration of traversing paths, keeping them deeply coupled to the filesystem.
- **Dependency Injection of Paths:** Passing lists of resolved paths to generators. Rejected because generators would still need to parse `__manifest__.py` files individually, causing redundant I/O operations.

## Consequences
- **Positive:** Generators are entirely decoupled from configuration and filesystem complexities. They become pure functions mapping source code to AI datasets.
- **Negative:** Generators require the Sources Framework to act as an intermediary adapter (`ContextModuleScanner`), meaning they can no longer be run independently of the `RepositoryManager`.
