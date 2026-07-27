# AIODOO Datasets
# Future Integration Improvements

This document contains improvements intentionally postponed after the
Execution / Approval / Conversation / Evaluation integration.

These are NOT blockers for v1.0.

Current build status:

- ✅ Deterministic
- ✅ Reproducible
- ✅ Dependency-aware orchestration
- ✅ Validation passing
- ✅ Dataset generation working
- ✅ Downstream generators consume upstream datasets

The following items should be revisited in future iterations.

---

# 1. Context Export Naming

Current:

datasets/
    manifest.json
    statistics.json

Desired:

datasets/
    context_manifest.json
    context_statistics.json

Reason:

Every other generator now exports generator-specific files.

Benefits:

- avoids filename ambiguity
- easier debugging
- cleaner validation
- consistent export convention

Priority:
Low

---

# 2. Dataset Naming Convention

Current:

planner_v1_0.jsonl
coding_v1_0.jsonl
repair_v1_0.jsonl
context_v1_0.jsonl

execution_dataset.jsonl
approval_dataset.jsonl
conversation_dataset.jsonl
evaluation_dataset.jsonl

Future decision:

Either

planner_v1_0.jsonl
coding_v1_0.jsonl
...
execution_v1_0.jsonl

or

planner_dataset.jsonl
coding_dataset.jsonl
...

Choose one convention and use it consistently.

Priority:
Low

---

# 3. Approval Dataset Richness

**Status (Step 3):** Implemented — subject-decision grain (generator v2).

Approval now emits **one JSONL record per upstream subject** (planner / coding /
repair / execution) with bounded evidence and stable `record_id`s. See
`generators/approval/README.md`.

Remaining optional richness (rules signal quality, more negative cases) can
still improve diversity but is no longer a grain/architecture blocker.

---

# 4. Conversation Dataset Richness

**Status (Step 4):** Implemented — next-reply grain (generator v2).

Conversation now reconstructs development episodes and emits **one JSONL record
per assistant reply** with bounded history and stable identities. See
`generators/conversation/README.md` and `docs/conversation_migration_v2.md`.

Remaining optional richness (more natural dialogue phrasing, tool turns) can
still improve diversity but is no longer a grain/architecture blocker.

---

# 5. Evaluation Dataset Richness

Current:

Single evaluation record.

Future improvements:

Generate benchmark suites for:

- correctness
- reasoning
- planning
- code generation
- repair
- execution
- approval
- retrieval
- multi-turn conversation

Goal:

Large evaluation benchmark.

Priority:
High

---

# 6. Execution Dataset Improvements

Current:

Execution builds execution plans from upstream datasets.

Future improvements:

Generate:

- execution failures
- rollback plans
- retry plans
- dependency failures
- environment failures
- migration execution
- upgrade execution
- deployment execution

Goal:

Increase execution diversity.

Priority:
Medium

---

# 7. Stronger Cross-Dataset Validation

Future improvements:

Validate:

Planner task
↓

Coding artifact
↓

Execution step
↓

Approval evidence
↓

Conversation references
↓

Evaluation benchmark

Everything should be traceable by protocol hash.

Priority:
Medium

---

# 8. Dataset Quality Audit

Infrastructure is now stable.

Future work should focus on dataset quality.

Audit:

- prompt quality
- response quality
- reasoning quality
- grounding
- diversity
- hallucinations
- duplication
- instruction quality
- metadata quality

Priority:
High

---

# 9. AIODOO Core Protocol Validator

Current:

Could not import AIODOO Core Protocol Validator.

Not blocking.

Future:

Integrate once AIODOO Core package is available.

Priority:
Low

---

# Summary

Current Status:

- **Orchestration / DAG:** ready (all 8 generators wired in `build_dataset.py`)
- **Framework CI:** ready (ruff + pytest + coverage fail-under 60)
- **Training-scale corpora:** planner, coding, repair, context, execution
- **Sparse (not train-all-8):** approval, conversation, evaluation — deferred richness
- **Overall train-all-8 readiness:** **NO**

Next Phase:

Improve dataset quality (sparse corpora) rather than orchestration.
