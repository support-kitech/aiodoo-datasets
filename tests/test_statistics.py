"""Tests for Planner Statistics aggregation."""

import json
from pathlib import Path
from aiodoo_datasets.generators.planner.statistics.planner_statistics import PlannerStatistics
from aiodoo_datasets.generators.planner.validation.schema import PlannerDatasetRecord, PlanPayload, Analysis, TaskSpec, PlanAction

def test_planner_statistics_aggregation(tmp_path):
    stats = PlannerStatistics()
    
    # Simulate a validation failure
    stats.record_validation_failure()
    
    # Simulate a duplicate
    stats.record_duplicate()
    stats.record_duplicate()
    
    # Simulate a valid record
    payload = PlanPayload(
        goal="Test",
        workspace="src/test",
        analysis=Analysis(summary="sum", risks=[]),
        tasks=[
            TaskSpec(id="t1", title="T1", description="D1", complexity=1, estimated_files=1, estimated_time=1, dependencies=[]),
            TaskSpec(id="t2", title="T2", description="D2", complexity=2, estimated_files=1, estimated_time=1, dependencies=["t1"])
        ],
        execution=[],
        summary="sum"
    )
    
    metadata = {
        "module": "test_module",
        "odoo_version": "17.0",
        "edition": "enterprise",
        "scenario": ["Portal Interface", "UI"],
        "difficulty": 4
    }
    
    record = PlannerDatasetRecord(
        instruction="Do it",
        input="context",
        output=payload,
        metadata=metadata
    )
    
    json_str = json.dumps(record.model_dump())
    
    stats.add_sample(record, json_str)
    
    assert stats.total_samples == 1
    assert stats.total_modules == 1
    assert stats.validation_failures == 1
    assert stats.duplicate_count == 2
    
    assert stats.total_tasks == 2
    assert stats.total_dependencies == 1
    
    assert stats.version_distribution["17.0"] == 1
    assert stats.edition_distribution["enterprise"] == 1
    assert stats.scenario_distribution["Portal Interface"] == 1
    assert stats.difficulty_distribution[4] == 1
    
    # Export and verify JSON structure
    out_file = tmp_path / "stats.json"
    stats.export(out_file)
    
    with open(out_file, "r") as f:
        data = json.load(f)
        
    assert data["total_samples"] == 1
    assert data["total_modules"] == 1
    assert data["duplicate_count"] == 2
    assert data["validation_failures"] == 1
    assert data["average_tasks_per_sample"] == 2.0
    assert data["average_dependencies_per_task"] == 0.5
