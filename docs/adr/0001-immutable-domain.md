# ADR-0001: Immutable Domain

## Decision
All domain entities (`RepositoryContext`, `Repository`, `OdooModule`, `InterpretedModule`) are implemented as strictly immutable, frozen Python dataclasses (`@dataclass(frozen=True)`). Once instantiated, their state cannot be modified.

## Rationale
The Sources Framework serves as the foundational data layer for multiple downstream AI dataset generators. If downstream generators were allowed to mutate the context (e.g., modifying module paths, stripping dependencies), it would introduce non-deterministic bugs, race conditions in concurrent processing workloads, and pollute the cache.

## Alternatives Considered
- **Mutable Dictionaries:** Too error-prone, lacks typing, and causes silent key errors downstream.
- **Standard Classes with Getters/Setters:** Requires extensive boilerplate to prevent modification and is less memory-efficient than `slots=True` dataclasses.

## Consequences
- **Positive:** Guaranteed determinism. Downstream consumers can share the same memory references safely.
- **Negative:** Any structural change to a domain object requires instantiating an entirely new object (e.g., using `dataclasses.replace()`), which can carry a marginal CPU/Memory cost during the initial pipeline building phase.
