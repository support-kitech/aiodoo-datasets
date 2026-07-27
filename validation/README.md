# AIODOO Validation Framework

Production-grade, generator-aware validation for all AIODOO dataset generators.

## Overview

The Validation Framework is the 4th shared framework in the AIODOO ecosystem. It runs as a post-generation gate, validating every dataset before statistics and export.

**Version:** 1.0.0  
**Rules:** 23  
**Schemas:** 8  
**Test Coverage:** 81/81 passing

## Architecture

```
validation/
├── __init__.py                         Public API (20 exports)
├── exceptions.py                       Exception hierarchy
├── constants/framework.py              Version + priority constants
├── domain/                             Frozen domain models
│   ├── enums.py                        5 enums (all str,Enum)
│   ├── models.py                       ValidationIssue, ValidationContext
│   ├── results.py                      ValidationResult, Summary, Report
│   └── metrics.py                      ValidationMetrics
├── schemas/                            Schema Framework
│   ├── base.py                         DatasetSchema, FieldDefinition
│   ├── registry.py                     SchemaRegistry (freezable)
│   ├── planner.py                      Planner schema
│   ├── coding.py                       Coding schema
│   ├── repair.py                       Repair schema
│   ├── context.py                      Context schema
│   ├── execution.py                    Execution schema
│   ├── approval.py                     Approval schema
│   ├── conversation.py                 Conversation schema
│   └── evaluation.py                   Evaluation schema
├── rules/                              Rule engine
│   ├── base.py                         BaseRule ABC
│   ├── registry.py                     RuleRegistry (freezable)
│   ├── schema/                         3 schema rules (SCH-001..003)
│   ├── metadata/                       3 metadata rules (META-001..003)
│   ├── integrity/                      4 integrity rules (INT-001..004)
│   ├── references/                     3 reference rules (REF-001..003)
│   ├── serialization/                  2 serialization rules (SER-001..002)
│   └── generators/                     8 generator rule files (11 rules)
├── validators/                         3-tier validation
├── pipeline/                           Pipeline orchestration
├── builders/                           Object construction (4 builders)
├── core/manager.py                     ValidationManager facade
├── reports/                            4 output formats
├── cli/                                CLI commands
└── tests/unit/                         81 unit tests
```

## Quick Start

```python
from pathlib import Path
from validation import ValidationManager, ValidationOptions

manager = ValidationManager()

# Validate all datasets
result = manager.validate(Path("datasets"))
print(f"Passed: {result.success}")

# Validate a single file
result = manager.validate_file(Path("datasets/planner_v1_0.jsonl"))

# Validate a single record with schema awareness
record = {"instruction": "...", "input": "...", "output": {...}, "metadata": {...}}
result = manager.validate_record(record, "planner_v1_0.jsonl")

# Validate generator output before export
records = [...]
result = manager.validate_generator_output(records, "planner")
```

## Schema Framework

Each generator has a dedicated schema describing its record structure:

| Generator | Schema ID | Top-Level Fields |
|-----------|-----------|-----------------|
| Planner | planner-v1 | instruction, input, output, metadata |
| Coding | coding-v1 | instruction, context, output, metadata |
| Repair | repair-v1 | instruction, context, output, metadata |
| Context | context-v1 | id, query, artifacts, graph, metadata |
| Execution | execution-v1 | instruction, output, metadata, context? |
| Approval | approval-v2 | review_id, decision, findings, evidence, recommendations, metadata, record_id, capability, subject_id, source_object_id, subject, payload |
| Conversation | conversation-v2 | instruction, output, metadata, context?, record_id, conversation_id, turn_index |
| Evaluation | evaluation-v2 | record_id, candidate_id, evaluation_case_key, capability_under_test, candidate, verdict, metadata, … |
| BenchmarkCatalog | benchmark-catalog-v1 | evaluation_id, catalog, metadata (non-SFT) |

### Schema Authoring

To add a new generator schema:

```python
from validation.schemas.base import DatasetSchema, FieldDefinition

MY_SCHEMA = DatasetSchema(
    schema_id="mygen-v1",
    generator_name="mygen",
    version="1.0.0",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
```

Then register it in `validation/builders/schema_builder.py`.

### Schema Resolution

Schemas are resolved automatically from dataset filenames:
- `planner_v1_0.jsonl` → `planner` schema
- `approval_dataset.jsonl` → `approval` schema
- Unknown filenames → fallback to generic validation

## Rule Engine

### Categories & Priorities

| Priority | Category | Rule IDs | Description |
|----------|----------|----------|-------------|
| 10–12 | Schema | SCH-001..003 | Required fields, types, structure |
| 20–22 | Metadata | META-001..003 | Protocol hash, versions, timestamps |
| 30–33 | Integrity | INT-001..004 | Hash format, duplicates, IDs, checksums |
| 40–42 | References | REF-001..003 | Orphans, cycles, cross-record |
| 51 | Serialization | SER-002 | Null byte detection |
| 60–61 | Generator | 11 rules | Per-generator validations |

### Rule Authoring

```python
from validation.rules.base import BaseRule
from validation.domain.enums import ValidationSeverity, ValidationCategory

class MyRule(BaseRule):
    @property
    def rule_id(self) -> str:
        return "MYR-001"

    @property
    def description(self) -> str:
        return "Check something specific."

    @property
    def severity(self) -> ValidationSeverity:
        return ValidationSeverity.ERROR

    @property
    def category(self) -> ValidationCategory:
        return ValidationCategory.GENERATOR

    def validate(self, record, context):
        schema = context.metadata.get("resolved_schema")
        # Schema-aware validation logic
        return ()
```

## CLI

```bash
# Validate all datasets
python -m validation.cli.commands validate-all --dir datasets --format console

# Validate single dataset
python -m validation.cli.commands validate-dataset datasets/planner_v1_0.jsonl

# Validate single record
python -m validation.cli.commands validate-record datasets/planner_v1_0.jsonl 0
```

## Report Formats

- **Console** — Human-readable terminal output with severity icons
- **JSON** — Machine-readable `validation_report.json`
- **Markdown** — `VALIDATION_REPORT.md` for documentation
- **CI** — GitHub Actions annotations

## Integration

The framework is wired into `build_dataset.py` as Step 9:

```
Sources → Preprocessing → Protocol → Generators → Validation → Statistics
```

Exit codes:
- `0` — All generators and validation passed
- `1` — Generator failure
- `2` — Validation failure (datasets generated but invalid)

## Version Support

Adding support for new Odoo versions requires only schema registration:

```python
PLANNER_ODOO18_SCHEMA = DatasetSchema(
    schema_id="planner-v2",
    generator_name="planner_odoo18",
    version="2.0.0",
    ...
)
```

No framework internals need modification.

## Tests

```bash
pytest validation/tests/ -v
# 81 passed in 0.18s
```
