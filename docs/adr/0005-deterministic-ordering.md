# ADR-0005: Deterministic Ordering

## Decision
All lists, tuples, and internal mappings across the Sources Framework (including inside `RepositoryContext` and Cache Serialization) must be strictly and deterministically ordered (e.g., sorted alphabetically by name or path) before being frozen. 

## Rationale
Machine Learning and AI dataset generation require strict determinism. If the same source code is scanned twice, the resulting JSONL datasets must be byte-for-byte identical. OS-level filesystem traversal (`os.walk` or `Path.iterdir()`) yields files in arbitrary orders depending on disk allocation. If this arbitrary order is passed into the cache and subsequently to generators, the final dataset sequences will shuffle between runs, ruining evaluation metrics and causing massive diffs in version control.

## Alternatives Considered
- **Sorting in Generators:** Forcing every generator to sort the data it receives. Rejected because it duplicates sorting logic and is prone to human error (developers forgetting to sort a new list).
- **No Ordering:** Accepting non-deterministic datasets. Rejected because strict reproducibility is a core engineering principle for AIODOO.

## Consequences
- **Positive:** Guaranteed 100% deterministic output. Two researchers running the pipeline on different operating systems will produce identical datasets.
- **Negative:** Sorting operations introduce a minimal performance overhead during the `RepositoryScanner` and `ModuleFactory` phases, but this is entirely mitigated by the SQLite Cache (which caches the pre-sorted collections).
