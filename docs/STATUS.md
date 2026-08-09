# Status — aiodoo-datasets

**Living document.** `main` is the only source of truth.  
**Permanent branch:** `main`  
**Git tags / GitHub Releases:** none (metadata reset)  
**Historical evidence:** `docs/archive/`

## Purpose

Dataset generation plane for capability corpora.

## Current implementation (on main)

| Item | Status |
|------|--------|
| Generators / DAG tooling | Shipped on `main` |
| Contract adoption | `docs/CONTRACT_ADOPTION.md` |
| Product composition | Out of scope |
| ECO-1 / Odoo specialization | **Legitimate Training domain** — Odoo sources drive generators; must not define generic Running System identity |
| Alignment to FP2 System contracts | **TR-6 pack evaluation** — `READY_WITH_REQUIRED_DATA_FIXES` (`controlled_batch_1/quality_report_tr6.json`). Legacy production JSONL **untouched**. |

## Living docs

- `docs/architecture.md`, `docs/public_api.md`, `docs/CONTRACT_ADOPTION.md`, `docs/adr/`
- `docs/roadmap.md`, `README.md`, `CHANGELOG.md`
- `datasets/fp2/README.md` — FP2 namespace inventory
- `datasets/fp2/controlled_batch_1/README.md` — TR-5/TR-6 batch artifacts
- Training SoT: `aiodoo-training/docs/FP2_PACK_EVALUATION.md`, `FP2_CONTROLLED_BATCH.md`, `FP2_CORPUS_QUALITY.md`

## Historical

Completed migration/freeze/certification reports live under `docs/archive/`.
