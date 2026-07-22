"""Adoption layer for the shared `aiodoo_contract` Capability Contract.

Per the AIODOO v2.0.0-fixes Phase 0 Architecture Freeze (D1-D12) and Phase 2
("aiodoo-datasets Contract Adoption"), `aiodoo-contract` owns the canonical
shape of every capability's request/response schema, enums, validators, and
version policy. This package does **not** redefine any of that. It exists
solely to *project* this repository's existing, richer generator output
records (`instruction`/`context`/`output`/`metadata` JSONL rows, tuned for
training-time pedagogy) onto the canonical `aiodoo_contract` request/response
schema for a capability, so that:

- the projection can be validated against the contract
  (:mod:`generators.common.contract.adapters`), and
- an evaluation corpus for `aiodoo-validation` can be produced using the same
  contract schemas as every other consumer
  (:mod:`generators.common.contract.eval_corpus`).

See `CONTRACT_ADOPTION.md` at the repository root for the full rationale,
including which generator-internal enums/metadata models were deliberately
*not* collapsed into `aiodoo_contract` imports, and why.
"""
