"""Tests for Planner Dataset Deduplication."""

from pathlib import Path
from generators.planner.validation.deduplicator import Deduplicator
from generators.planner.export.metadata import compute_protocol_hash
from generators.planner.discovery.scanner import OdooModule, ManifestInfo
from generators.planner.discovery.classifier import Scenario
from generators.planner.validation.schema import PlanPayload, Analysis, TaskSpec, PlanAction

def test_protocol_hash_determinism():
    mod = OdooModule(
        name="test_mod",
        path=Path("/tmp"),
        version="17.0",
        edition="community",
        manifest=ManifestInfo(name="Test Mod"),
        module_hash="mod_hash_1",
        manifest_hash="man_hash_1"
    )
    scenario = Scenario(name="Portal Interface")
    
    payload = PlanPayload(
        goal="Test Goal",
        workspace="src/test_mod",
        analysis=Analysis(summary="sum", risks=[]),
        tasks=[TaskSpec(id="t1", title="T1", description="D1", complexity=1, estimated_files=1, estimated_time=1)],
        execution=[PlanAction(id="a1", action="create_file", args={}, reason="r", expected_result="e")],
        summary="sum"
    )
    
    hash1 = compute_protocol_hash(mod, scenario, payload)
    hash2 = compute_protocol_hash(mod, scenario, payload)
    
    # Hash should be perfectly deterministic
    assert hash1 == hash2
    
    # Modify something critical
    mod.module_hash = "mod_hash_2"
    hash3 = compute_protocol_hash(mod, scenario, payload)
    assert hash1 != hash3

def test_deduplicator_blocks_identical_protocol_hashes():
    deduplicator = Deduplicator()
    
    hash_a = "abc123hash"
    hash_b = "def456hash"
    
    assert deduplicator.is_unique(hash_a) is True
    assert deduplicator.is_unique(hash_a) is False  # Duplicate!
    assert deduplicator.is_unique(hash_b) is True
