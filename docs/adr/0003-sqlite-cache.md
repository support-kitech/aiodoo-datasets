# ADR-0003: SQLite Cache

## Decision
The Sources Framework utilizes a local SQLite database (`sources.sqlite`) to serialize and persist the complete, immutable `RepositoryContext` graph, fully bypassing file I/O and parsing during subsequent executions (Warm Loads).

## Rationale
Parsing thousands of Odoo modules (Python AST, XML views, YAML manifests) takes significant CPU time and disk I/O. For dataset generators that run repeatedly across the same source code, this cold-start time is heavily penalizing. A binary caching format (like Pickle) is fragile across Python versions. A pure JSON file lacks structured queries and efficient metadata retrieval. SQLite provides an ACID-compliant, universally supported, single-file storage engine that seamlessly stores JSON blobs and indexing metadata.

## Alternatives Considered
- **Pickle / Joblib:** Dropped because Pickle files break frequently when underlying domain classes change or Python versions upgrade.
- **Pure JSON Files:** Dropped because reading a 50MB JSON file into memory purely to check a metadata timestamp is inefficient. SQLite allows reading a single `metadata` row instantly to validate the cache.
- **Redis / Memcached:** Dropped because it requires developers to install external infrastructure. The cache must work universally out-of-the-box.

## Consequences
- **Positive:** Massive execution speedups (e.g., 18x improvement from 1.4s to 0.07s). Completely transparent to developers.
- **Negative:** Introduces an explicit caching step during pipeline orchestrations. Requires robust invalidation logic to ensure the cache never goes stale when source code changes.
