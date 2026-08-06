> **Historical document.** Written when Git tags / release identity existed.
> Git tags and GitHub Releases were later removed ecosystem-wide.
> **Current source of truth:** branch `main` only. See `docs/STATUS.md`.
> Do not treat tag or release recommendations in this file as current instructions.

# AIODOO Dataset Repository: Production Freeze Report

## 1. Repository Overview

This document is the production freeze report for the **AIODOO Dataset Repository**
(generators + orchestration). It records what is frozen for tooling release
**v2.0.0**, and what remains intentionally deferred.

**Repository tooling version:** `v2.0.0`  
**Repository status:** `Tooling freeze — generation DAG complete; three corpora sparse`  
**Freeze recommendation:** `Approved for annotated tag v2.0.0 (tooling); not train-all-8 ready`

This repository is **not** an installable Python package. Run from source via
`python3 build_dataset.py`.

---

## 2. Completed Generators (orchestration)

All eight generators are implemented as code and registered in `build_dataset.py`:

| # | Capability | Training-scale corpus? | Notes |
| --- | --- | --- | --- |
| 1 | Planner | Yes (thousands of records) | Usable at scale |
| 2 | Coding | Yes | Usable at scale; some duplicates in stats |
| 3 | Repair | Yes (hundreds) | Smaller but non-stub |
| 4 | Context | Yes (tens of thousands) | Best-tested generator |
| 5 | Execution | Yes | Consumes upstream artifacts |
| 6 | Approval | **No** — 1 record | Rules partially stubbed; see FUTURE doc |
| 7 | Conversation | **No** — 1 record | Richness deferred |
| 8 | Evaluation | **No** — 1 record | Placeholder prompts; deferred |

Frozen release inventory (external `AIODOO/datasets/…` and local `datasets/` build):
**67,258** total records. Sparse counts are intentional and documented in
`docs/FUTURE_INTEGRATION_IMPROVEMENTS.md`.

---

## 3. Engineering Principles (unchanged)

- **Deterministic:** Sorted keys; shared export writer.
- **Immutable domain:** Frozen models where established.
- **Layered pipelines:** Domain → builders → protocol → export → validation.
- **Shared infrastructure:** DatasetWriter, validation framework, checkpoints.

---

## 4. Repository Checklist

- [x] No UUID / no random in generator ID paths (factory hashing).
- [x] Shared DatasetWriter / manifests / statistics paths.
- [x] Validation framework runs at end of `build_dataset.py`.
- [x] CI: ruff + pytest + coverage (honest measured surface).
- [x] Not packaged; README matches clone-and-run workflow.
- [ ] Approval / conversation / evaluation training-scale richness (future).
- [ ] Automated freeze/publish job (out of scope for this freeze).

---

## 5. Testing Summary

- Strong coverage on **sources / protocol / preprocessing / validation / context**.
- Unit coverage on **approval** rule wiring (not E2E richness).
- **No** dedicated `test_*.py` suites for planner, coding, repair, execution,
  conversation, or evaluation — coverage gate **omits** those trees intentionally.
- Determinism infrastructure exists; byte-identical multi-run claims are **not**
  proven by CI for every generator.

---

## 6. Repository Metrics (honest)

| Metric | Score | Assessment |
| :--- | :---: | :--- |
| Architecture / layering | **7/10** | Real layered stack; stubs remain in sparse paths |
| Generator completeness | **4/10** | Five scalable corpora; three documented stubs |
| Schema / validation | **6/10** | Framework works; quality ≠ pass |
| Determinism | **5/10** | Infrastructure present; not CI-proven for all 8 |
| Packaging / CLI honesty | **8/10** | Clone-and-run; no false package claims (v2.0.0) |
| Tests / coverage honesty | **5/10** | Gate measures tested surface only |
| Training usability (all 8) | **2/10** | Skip approval / conversation / evaluation at scale |
| Docs honesty | **7/10** | This report + FUTURE doc aligned with artifacts |
| **Overall production readiness** | **3/10** | Demoable DAG; **not** train-all-8 ready |

---

## 7. Final Recommendation

**Approve tooling tag `v2.0.0`** for: clone-and-run layout, honest docs, green CI,
and frozen architecture of the generation DAG.

**Do not** treat this freeze as approval to train all eight capabilities tomorrow.
Block or skip **approval**, **conversation**, and **evaluation** until richness is
rebuilt (future work — not part of this freeze).
