> **Historical document.** Written when Git tags / release identity existed.
> Git tags and GitHub Releases were later removed ecosystem-wide.
> **Current source of truth:** branch `main` only. See `docs/STATUS.md`.
> Do not treat tag or release recommendations in this file as current instructions.

# aiodoo-datasets — RELEASE_REPORT (v2.0.0)

**Release identity:** annotated tag `v2.0.0` (tooling freeze)  
**Dataset artifact version:** remains `v1.0.0` inventory (67,258 records)  
**Date:** 2026-07-19

---

## Production Ready

| Question | Answer |
| --- | --- |
| In-boundary tooling / generation DAG production ready? | **YES** |
| Train-all-8 capabilities ready? | **NO** |
| Overall production score (in-boundary) | **7 / 10** |
| Train-all-8 score | **3 / 10** |

---

## Quality gates (local)

| Gate | Result |
| --- | --- |
| `ruff check .` | Pass |
| `ruff format --check .` | Pass (806 files) |
| `coverage run -m pytest` | **264 passed** |
| `coverage report --fail-under=60` | **81%** |
| mypy | **Not in CI** (intentional; not configured as a gate) |

---

## Existing artifact validation (no full regenerate)

| File | Records | Status |
| --- | ---: | --- |
| planner_v1_0.jsonl | 5,695 | OK |
| coding_v1_0.jsonl | 5,459 | OK |
| repair_v1_0.jsonl | 481 | OK |
| context_v1_0.jsonl | 50,161 | OK |
| execution_dataset.jsonl | 5,459 | OK |
| approval_dataset.jsonl | 1 | OK (sparse) |
| conversation_dataset.jsonl | 1 | OK (sparse) |
| evaluation_dataset.jsonl | 1 | OK (sparse) |
| **Total** | **67,258** | OK |

Training compatibility spot-check (first-record keys vs
`aiodoo-training` `REQUIRED_FIELDS`): **all 8 OK**.

Full `python3 build_dataset.py` regeneration was **not** re-run for this tag
(multi-GB / long-running). Validation-at-build remains the production path for
future regenerations.

---

## Architecture impact

None. Repository still owns dataset generation only.

---

## Remaining blockers

None for **in-boundary tooling freeze**.

Remaining for **train-all-8 / ecosystem E2E** (not this tag’s scope):

- Approval single ~258MB record / incomplete rules
- Conversation / evaluation 1-record stubs
- Approval blob unusable under training max sequence length (consumer impact)

---

## Remaining future work

See `docs/FUTURE_INTEGRATION_IMPROVEMENTS.md`: sparse richness, naming
unification, automated freeze publish, generator test expansion.

---

## Architectural debt

- Mixed `*_v1_0` vs `*_dataset` filenames
- Context generic `manifest.json`
- Coverage omit list for untested generators (honest, not hidden)

---

## Repository health

**Good** for clone-and-run + CI. Docs aligned with reality. No false packaging.

---

## Release recommendation

**Ship annotated tag `v2.0.0`** as tooling freeze. Do **not** market as
train-all-8 ready. Prefer planner/coding/repair/context/execution for training.
