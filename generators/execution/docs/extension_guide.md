# Extension Guide

The Execution Generator is built around static registries to allow extensions without modifying core code.

## 1. Custom Builders
To add a new builder for a specific Odoo node type:
1. Implement `BaseBuilder`.
2. Register it in `BuilderRegistry`.

## 2. Custom Protocol Mappers
To adjust the JSON schema output:
1. Implement `ProtocolMapper`.
2. Register it in `ProtocolRegistry`.

## 3. Custom Output Writers
To support formats other than JSONL (e.g., SQLite, Parquet):
1. Implement `BaseWriter` in the `export` package.
2. Ensure atomic write constraints via temporary files.
3. Register it in `ExportRegistry`.

> [!WARNING]
> Do NOT use reflection or runtime discovery for extensions. All extensions must be explicitly statically registered in the pipeline bootstrap.
