# FP2 generators (TR-3)

FP2-native generators are owned by:

`aiodoo-training` → `aiodoo_training.system_training_contract.generators`

This datasets repository holds the separated fixture output at `datasets/fp2/`.

Legacy generators under `generators/{planner,coding,...}/` remain **historical /
provider-plane** and must not silently overwrite FP2 corpora.

```bash
cd ../aiodoo-training
PYTHONPATH=. python3 -m aiodoo_training.system_training_contract.generators.cli \
  --output-dir ../aiodoo-datasets/datasets/fp2
```
