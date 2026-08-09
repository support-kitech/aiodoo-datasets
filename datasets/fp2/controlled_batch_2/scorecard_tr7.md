TR-6 Training-Pack Readiness — datasets/fp2/controlled_batch_2
Native records: 1386
Dev pack: 1004  Reasoning pack: 1078
Checksum OK: True
Readiness: READY_FOR_TRAINING

Hard gates:
  [PASS] checksum
  [PASS] continuity
  [PASS] decision_context_integrity
  [PASS] forbidden_how
  [PASS] inventory_1200
  [PASS] negative_contamination
  [PASS] objective_completion_semantics
  [PASS] pack_validity
  [PASS] provider_separation
  [PASS] schema
  [PASS] split_integrity
  [PASS] taxonomy

Soft metrics:
  [PASS] capability_balance
  [PASS] continuity_volume
  [PASS] domain_balance
  [PASS] edge_case_coverage
  [PASS] pack_balance
  [PASS] repetition
  [PASS] scenario_diversity
  [WARN] split_capability_balance

Diversity: unique_families=211 concentration=2.53% largest=nav_tests
Odoo/generic: 226/1160 (16.31%) ambiguous=0

Rationale:
  - hard_gates_pass_and_soft_metrics_acceptable

