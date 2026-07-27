# AIODOO Dataset Release Inventory (post Step 6 regen)

> Describes the JSONL corpora under `datasets/`.  
> Artifact files themselves are **gitignored**.

Generator tooling: **v2.0.0** (Approval / Conversation / Evaluation generators).  
Step 6 regeneration date: **2026-07-27**.

---

## Overview

Local builds write into `datasets/` via `python3 build_dataset.py` (full) or
`python3 regenerate_v2_datasets.py` (Approval / Conversation / Evaluation only,
from existing upstream JSONL).

---

## Release information

| Property | Value |
| --- | --- |
| Dataset artifact status | Step 6 regen complete (A/C/E v2) |
| Generator repository | aiodoo-datasets |
| Supported Odoo versions (sources) | 17.0, 18.0, 19.0 |
| Train-all-8 ready? | **Yes** for grain (see note on EvaluationFormatter) |

---

## Dataset contents (measured 2026-07-27)

| File | Records | Training-scale? |
| --- | ---: | --- |
| planner_v1_0.jsonl | 5,695 | Yes |
| coding_v1_0.jsonl | 5,459 | Yes |
| repair_v1_0.jsonl | 481 | Yes (smaller) |
| context_v1_0.jsonl | 50,161 | Yes |
| execution_dataset.jsonl | 5,459 | Yes |
| approval_dataset.jsonl | **17,094** | **Yes (v2)** |
| conversation_dataset.jsonl | **29,016** | **Yes (v2)** |
| evaluation_dataset.jsonl | **189,615** | **Yes (v2)** |
| evaluation_benchmark_catalog.jsonl | **1** | **Not SFT** |
| **Train JSONL total (excl. catalog)** | **303,380** | |

Checksums: `datasets/step6_regeneration_summary.json`.

---

## Intended usage

- Train Development: Coding, Repair, Execution (+ supporting Context).
- Train Reasoning: Planner, Conversation, Approval, Evaluation (SFT file only).
- Do **not** train on `evaluation_benchmark_catalog.jsonl`.
- Sync `aiodoo-training` EvaluationFormatter to contract projection before
  Evaluation LoRA training (known follow-up).

---

## License

Distributed under the licensing terms of the AIODOO project.
