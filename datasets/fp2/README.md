# FP2-native datasets (TR-3 / TR-4 / TR-5)

**Classification:** FP2 System Training Contract v1.0.0  
**Not** Production Certified V1 / provider Protocol corpora.

## Location

`datasets/fp2/` — intentionally separated from legacy production JSONL.

## Contents (fixture root)

| File | Record type |
|------|-------------|
| `capability_intent.jsonl` | Engineering capability intents |
| `execution_work_unit.jsonl` | ExecutionWorkUnit WHAT |
| `planning_decision.jsonl` | Planning / COMPLETE / ESCALATE |
| `observation.jsonl` | Observation envelopes |
| `engineering_feedback.jsonl` | EngineeringFeedback |
| `engineering_state.jsonl` | Current-cycle EngineeringState |
| `decision_context.jsonl` | EngineeringDecisionContext |
| `loop_decision.jsonl` | Intelligence Loop decisions |
| `projection_fixtures.jsonl` | Selective historical projection cases |
| `quality_negatives.jsonl` | Adversarial quality-only (NOT training) |
| `quality_report_tr4.json` | TR-4 scorecard |
| `manifest.json` | Fixture generation metadata |
| `controlled_batch_1/` | **TR-5 controlled batch (PASS, immutable evidence)** |
| `controlled_batch_2/` | **TR-7 derivative — READY_FOR_TRAINING** |

## Controlled batch 1 (TR-5)

See `controlled_batch_1/README.md` and `aiodoo-training/docs/FP2_CONTROLLED_BATCH.md`.

- 1200 native records, 23/23 preferred Engineering coverage  
- train/val/test splits + Development/Reasoning packs  
- Decision: **PASS**

## Controlled batch 2 (TR-7)

See `controlled_batch_2/README.md`.

- 1386 native records (TR-5 + continuity expansion + domain corrections)  
- Continuity: state/DC/loop = 77 each; ambiguous domain labels = 0  
- Decision: **READY_FOR_TRAINING** (no training started)
## Quality

```bash
cd ../aiodoo-training
PYTHONPATH=. python3 -m aiodoo_training.system_training_contract.quality.cli \
  --corpus ../aiodoo-datasets/datasets/fp2
```

## Regeneration

```bash
cd ../aiodoo-training
PYTHONPATH=. python3 -m aiodoo_training.system_training_contract.generators.cli \
  --output-dir ../aiodoo-datasets/datasets/fp2

PYTHONPATH=. python3 -m aiodoo_training.system_training_contract.generators.controlled_batch_cli \
  --target 1200 \
  --output-dir ../aiodoo-datasets/datasets/fp2/controlled_batch_1
```

Do **not** run `build_dataset.py` to overwrite these.  
Do **not** train on `quality_negatives.jsonl`.  
Do **not** modify legacy production datasets.

## Contract

See `aiodoo-training/docs/TRAINING_SYSTEM_CONTRACT.md`, `FP2_NATIVE_CORPORA.md`,
`FP2_CORPUS_QUALITY.md`, `FP2_CONTROLLED_BATCH.md`.
