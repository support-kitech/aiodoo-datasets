# Preprocessing Public API v1.0.0

## `PreprocessingManager`
The thin, stateless facade exposed to all consumers.

### Methods
- `normalize(source_context: RepositoryContext, options: PipelineOptions = None) -> PipelineResult`: Primary entry point. Converts Raw to Normalized contexts safely, prioritizing Cache hits.
- `validate(source_context: RepositoryContext) -> PipelineResult`: Dry run that asserts all stage validations pass. Does not populate cache.
- `refresh_cache(source_context: RepositoryContext) -> PipelineResult`: Overrides `PipelineOptions` to forcibly recalculate normalization and override SQLite values.
- `clear_cache() -> None`: Drops all cached payloads.

## Domain Models
- `PreprocessedRepositoryContext`: Root domain object. Deeply nested tuple wrapper.
- `NormalizedFile`: Immutable representation containing `normalized_content`, `statistics`, and `metadata`.
- `PipelineResult`: Wraps a success boolean, the context, and execution statistics.
- `PipelineStatistics`: Granular floats describing serialization speeds, processing delays, and lookup bottlenecks.
