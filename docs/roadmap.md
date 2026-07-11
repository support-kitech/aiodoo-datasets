# Sources Framework Roadmap

The following concepts represent potential future architectural expansions for the AIODOO Sources Framework. They are documented here for long-term tracking but **are not** implemented in v1.0.0.

### 1. Remote Repositories & Git Loaders
Support for dynamically fetching and isolating repositories directly from remote Git origins or GitHub API configurations, removing the requirement for developers to manually clone entire ecosystems before running dataset generation.

### 2. Parallel & Concurrent Scanning
Implement multi-processed workers inside `RepositoryScanner`. For enterprise-scale environments containing tens of thousands of Odoo modules, disk I/O traversing could become a bottleneck. Offloading I/O to threaded/process pools would drastically decrease Cold Load times.

### 3. Distributed Caching (Redis/Postgres)
Replace or extend the local SQLite `CacheStore` with a distributed persistence layer. This would allow CI/CD pipelines and multiple developer workstations to instantly share the massive `RepositoryContext` graphs without each node building the cache locally.

### 4. Incremental Scanning
Instead of invalidating the entire Repository or Framework cache on a single file modification, implement granular hashing strategies at the `OdooModule` level to only rescan and re-interpret the exact modules that were changed, leaving 99% of the cache intact.

### 5. Live Repository Watching
Implement an active filesystem watcher (e.g., `watchdog`) embedded in a daemon service, allowing generators to hook into continuous streams of source updates rather than statically invoking `build_dataset.py` as a batch process.

### 6. Deep AST Caching Optimization
Currently, AST parsing happens downstream in the Generators. The Sources Framework could theoretically pre-parse `.py` and `.xml` files into generic Abstract Syntax Trees directly during the `RepositoryInterpreter` phase, embedding the fully parsed trees directly into the SQLite Cache.
