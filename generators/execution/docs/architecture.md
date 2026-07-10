# Execution Generator Architecture

The Execution Generator is a deterministic, immutable pipeline designed to convert parsed Odoo module structures into strict, AI-ready JSONL datasets representing execution graphs.

## Core Principles

1. **Immutability:** All domain models and execution contexts are strictly immutable (using frozen dataclasses).
2. **Stateless Operations:** Pipeline stages never modify global state or input contexts. They always return a new `Result` object.
3. **Pure Orchestration:** The Integration layer contains no business logic. It simply wires together isolated packages.
4. **Deterministic Generation:** Identical AST inputs guarantee byte-for-byte identical dataset outputs, including checksums and JSON serialization.

## Packages

- **Discovery & Analysis:** Extracts structure from Python AST.
- **Builders:** Translates raw AST objects into structured knowledge representations.
- **Graph:** Constructs the Directed Acyclic Graph (DAG) and ensures execution topology.
- **Planning:** Generates execution schedules, batches, phases, and stages.
- **Protocol:** Serializes the plan into a strict versioned dataset schema.
- **Export:** Writes the final dataset and metadata to disk atomically.
- **Integration:** Wires everything together via CLI.
