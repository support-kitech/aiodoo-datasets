# AIODOO Execution Generator

The AIODOO Execution Generator is a deterministic pipeline designed to statically analyze Odoo modules and convert them into AI-ready execution graphs. It forms the foundational data preparation layer for training Large Language Models to write Odoo implementations.

## Installation

You can install the package directly via pip. Since the project uses modern standards, it is recommended to install in a virtual environment.

```bash
# Clone the repository
git clone <repository_url>
cd aiodoo-datasets

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package and its development dependencies
pip install -e .[dev]
```

## Quick Start

You can generate an execution dataset by passing a target Odoo module directory and an output directory.

```bash
generate-execution --source-dir /path/to/odoo/module --output-dir /path/to/output/
```

This will automatically:
1. Parse the Python source structure.
2. Build the dependency graph.
3. Plan the execution sequences.
4. Export the resulting protocol JSONL and manifest files to your output directory.

## Architecture Overview

The generator enforces a strictly immutable, phase-based architecture:
1. **Analysis:** AST parsing and component extraction.
2. **Builders:** Knowledge translation from raw AST into domain rules.
3. **Graph:** Construction of the topological DAG ensuring valid execution sequence.
4. **Planning:** Orchestration of stages, phases, and schedules.
5. **Protocol:** Mapping to a strictly typed, versioned JSON schema.
6. **Export:** Atomic I/O streaming to disk without partial-write corruption.

For an in-depth breakdown, please read the [Architecture Documentation](generators/execution/docs/architecture.md).

## CLI Usage

The package provides the `generate-execution` CLI tool.

```bash
# Basic usage
generate-execution --source-dir ./custom_addons/my_module --output-dir ./generated_datasets

# Fail-fast and debug mode
generate-execution --source-dir ./custom_addons/my_module --output-dir ./generated_datasets --debug --fail-fast
```

## Python API Examples

If you wish to integrate the pipeline programmatically rather than via CLI, the package exposes a stable Python API.

```python
from pathlib import Path
from aiodoo_datasets.generators.execution.api import generate
from aiodoo_datasets.generators.execution.integration.pipeline_context import PipelineContext
from aiodoo_datasets.generators.execution.config.generator_config import GeneratorConfig
from aiodoo_datasets.generators.execution.config.export_config import ExportConfig
from aiodoo_datasets.generators.execution.config.runtime_config import RuntimeConfig
from aiodoo_datasets.generators.execution.integration.pipeline_statistics import PipelineStatistics
from types import MappingProxyType

# 1. Build immutable configurations
gen_config = GeneratorConfig(custom_settings=MappingProxyType({"source_dir": Path("./source")}))
export_config = ExportConfig(output_directory=Path("./output"))
rt_config = RuntimeConfig(debug_mode=True)

# 2. Assemble context
context = PipelineContext(
    generator_config=gen_config,
    export_config=export_config,
    runtime_config=rt_config,
    discovery_result={"source_dir": Path("./source")},
    pipeline_statistics=PipelineStatistics()
)

# 3. Generate dataset
result = generate(context)

if result.success:
    print(f"Dataset exported to {export_config.output_directory}")
else:
    print(f"Generation failed: {result.diagnostics}")
```

## Extension Guide

If you need to define custom node types or adjust protocol serialization formatting without forking the entire architecture, please review the [Extension Guide](generators/execution/docs/extension_guide.md).

## Developer Guide

For information on contributing, testing, and adhering to the immutability requirements, see the [Developer Guide](generators/execution/docs/developer_guide.md).

## Testing

The project uses `pytest` for all unit and integration testing.

```bash
# Run all tests
pytest

# Run only integration tests
pytest tests/integration

# Run tests marked as integration across the suite
pytest -m integration
```
