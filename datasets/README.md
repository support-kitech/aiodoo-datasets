# AIODOO Dataset Release Inventory (Production Certified)

> Describes the JSONL corpora under `datasets/`.  
> Artifact files themselves are **gitignored**.

Generator tooling: **v2.0.0** (Approval / Conversation / Evaluation generators).  
Step 6 regeneration date: **2026-07-27**.  
Step 7 (A/C/E) certification: **Production Certified** — `docs/step7_certification_report.md`.  
Remaining (P/C/R/E/Context) certification: **Production Certified** — `docs/remaining_datasets_certification_report.md`.

---

## Overview

Local builds write into `datasets/` via `python3 build_dataset.py` (full) or
`python3 regenerate_v2_datasets.py` (Approval / Conversation / Evaluation only,
from existing upstream JSONL).

---

## Release information

| Property | Value |
| --- | --- |
| Dataset artifact status | **Production Certified** (all train JSONL) |
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
