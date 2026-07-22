# AIODOO Datasets

Deterministic pipelines that scan Odoo sources and emit protocol JSONL datasets
for `aiodoo-training`.

This repository is an **internal engineering tree**. It is **not** an installable
Python package and is **not** published to PyPI.

## Requirements

- Python 3.12+
- Dependencies: `pydantic`, `PyYAML`, `aiodoo_contract` (runtime); `pytest`,
  `coverage`, `ruff` (CI/dev)

```bash
git clone <repository_url>
cd aiodoo-datasets
python3 -m pip install pydantic PyYAML pytest coverage ruff
python3 -m pip install -e ../aiodoo-contract  # canonical Capability Contract
```

`aiodoo_contract` is the ecosystem's canonical Capability Contract package
(schemas, validators, prompt builder, chat templates — see
`ecosystem-v2-certification/ARCHITECTURE_FREEZE_REPORT.md`). This repository
consumes it via a projection/adapter layer rather than redefining schemas;
see `CONTRACT_ADOPTION.md` for what was adopted, what stayed local, and why.

Run all commands from the **repository root** so imports resolve (`sources`,
`generators`, `protocol`, …).

## Full dataset build

Primary production entrypoint:

```bash
python3 build_dataset.py
```

This orchestrates Sources → Preprocessing → Protocol → all eight capability
generators → Validation → per-capability `aiodoo_contract` evaluation
corpora. Configure local Odoo paths in `config/sources.yaml`. Build output is
written under `datasets/` (gitignored artifacts; see `datasets/README.md` for
the release inventory description).

## Capability generators

Each capability lives under `generators/<name>/`. Orchestration is only via
`build_dataset.py`. Individual generator modules may expose helpers for
development; there is **no** console script entry point and **no**
`aiodoo_datasets` package namespace.

Example (execution API, importable from repo root):

```python
from generators.execution.api import generate
```

## Testing and lint (matches CI)

```bash
ruff check .
ruff format --check .
coverage run -m pytest
coverage report -m --fail-under=60
```

Coverage intentionally measures framework code plus generators that have
substantial tests (context, approval, and the `aiodoo_contract` adapter /
eval-corpus / orchestrator code under `generators/common/contract` and
`generators/common/pipeline`). Sparse/stub generators are omitted from the
coverage gate — see `AUDIT_RESOLUTION.md` and
`docs/FUTURE_INTEGRATION_IMPROVEMENTS.md`.

## Documentation

- Architecture / ADRs: `docs/`
- Contract adoption (`aiodoo_contract` integration, what stayed local, why): `CONTRACT_ADOPTION.md`
- Honest freeze status: `docs/production_freeze_report.md`
- Deferred richness (approval / conversation / evaluation): `docs/FUTURE_INTEGRATION_IMPROVEMENTS.md`
- Sources public API: `docs/public_api.md`
