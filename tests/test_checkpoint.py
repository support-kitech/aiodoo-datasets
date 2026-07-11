"""Tests for Dataset Checkpoint Manager."""

from generators.planner.state.checkpoint import CheckpointManager

def test_checkpoint_lifecycle(tmp_path):
    output_dir = tmp_path / "output"
    checkpoint = CheckpointManager(output_dir)
    
    # Initially empty
    state = checkpoint.load()
    assert len(state["processed_modules"]) == 0
    
    # Save a module
    checkpoint.save("account_accountant", written_rows=15)
    
    # Re-instantiate to test persistent loading
    checkpoint2 = CheckpointManager(output_dir)
    state2 = checkpoint2.load()
    
    assert "account_accountant" in state2["processed_modules"]
    assert state2["processed_count"] == 1
    assert state2["written_dataset_rows"] == 15
    assert checkpoint2.is_processed("account_accountant") is True
    assert checkpoint2.is_processed("sale_management") is False
    
    # Clear checkpoint
    checkpoint2.clear()
    state3 = checkpoint2.load()
    assert len(state3["processed_modules"]) == 0
    assert not (output_dir / "checkpoint.json").exists()
