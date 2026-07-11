# Preprocessing Architecture v1.0.0

## High-Level Architecture
The AIODOO Preprocessing Framework acts as the canonical normalization layer between the raw Odoo Source repositories and the AIODOO Dataset Generators.

```mermaid
graph TD
    A[Sources Framework] -->|RepositoryContext| B[PreprocessingManager]
    B -->|PipelineOptions| C[PreprocessingPipeline]
    
    C -->|Stage 1 Validation| D{Cache Valid?}
    D -- Hit --> E[Deserializer]
    E --> F[PreprocessedRepositoryContext]
    
    D -- Miss --> G[ProcessorRegistry]
    G --> H[ProcessorPipeline]
    H -->|Builders| I[Stage 2 Validation]
    I --> J[Serializer]
    J --> K[SQLite Store]
    I --> F
    
    F --> L[All Generators]
```

## Core Principles
1. **Total Immutability**: `ProcessorContext` instances are cloned using `with_update`, completely destroying mutability bugs.
2. **Determinism**: A `RepositoryContext` hash will ALWAYS produce the exact same `PreprocessedRepositoryContext` hash, thanks to explicit Priority sorting in the `ProcessorRegistry`.
3. **Stateless Processing**: Processors (`WhitespaceProcessor`, `PythonProcessor`, etc.) maintain no internal state between pipeline executions.
