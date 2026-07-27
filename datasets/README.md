# AIODOO Dataset Release Inventory (artifact release v1.0.0)

> Describes the frozen JSONL corpora produced by this repository.  
> Artifact files themselves are **gitignored**; the canonical copy may also live under
> `AIODOO/datasets/v1.0.0/`. This README is tracked for inventory honesty.

Generator tooling freeze for this repository: **v2.0.0** (see
`docs/production_freeze_report.md`). Dataset **artifact** version remains **v1.0.0**
until a new data release is published.

---

## Overview

Local builds write into `datasets/` via `python3 build_dataset.py`. Validation
“pass” means schema/integrity rules succeeded — it does **not** mean every
capability is training-scale or high-signal.

---

## Release information

| Property | Value |
| --- | --- |
| Dataset artifact version | v1.0.0 |
| Generator repository | aiodoo-datasets (tooling tag v2.0.0) |
| Total records | 67,258 |
| Supported Odoo versions (sources) | 17.0, 18.0, 19.0 |
| Train-all-8 ready? | **No** — see sparse rows below |

---

## Dataset contents (measured)

| File | Records | Training-scale? |
| --- | ---: | --- |
| planner_v1_0.jsonl | 5,695 | Yes |
| coding_v1_0.jsonl | 5,459 | Yes (duplicates present in stats) |
| repair_v1_0.jsonl | 481 | Yes (smaller) |
| context_v1_0.jsonl | 50,161 | Yes |
| execution_dataset.jsonl | 5,459 | Yes |
| approval_dataset.jsonl | many (1/subject after regen) | **Yes (v2 grain)** — regenerate; old 1-row file obsolete |
| conversation_dataset.jsonl | many (1/reply after regen) | **Yes (v2 grain)** — regenerate; old 1-row file obsolete |
| evaluation_dataset.jsonl | many (1/judgment after regen) | **Yes (v2 grain)** — regenerate; old catalog-as-SFT obsolete |
| evaluation_benchmark_catalog.jsonl | 1 catalog | **Not SFT** — certification/benchmark side channel |
| **Total** | **67,258** (pre A/C/E v2 regen) | |

Approval / Conversation / Evaluation generator v2 docs under `generators/*/README.md`.

---

## Directory layout (build / external release)

```text
datasets/   # or AIODOO/datasets/v1.0.0/
├── *_v1_0.jsonl / *_dataset.jsonl
├── *_manifest.json (context may use manifest.json)
├── *_statistics.json
└── (checkpoints / sqlite caches may appear in local builds — not part of release)
```

External release may use `manifests/` and `statistics/` subdirectories.

---

## Intended usage

- Prefer planner / coding / repair / context / execution / approval /
  conversation / **evaluation** (after v2 regen) for training.
- Do **not** train on `evaluation_benchmark_catalog.jsonl`.
- Consumer: `aiodoo-training` (configs under `configs/training/`).

---

## License

Distributed under the licensing terms of the AIODOO project.
