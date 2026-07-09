"""Tests for dataset manifest generation."""

import json
from pathlib import Path
from aiodoo_datasets.generators.planner.export.manifest import generate_manifest
from aiodoo_datasets.generators.planner.statistics.planner_statistics import PlannerStatistics

def test_manifest_generation(tmp_path):
    stats = PlannerStatistics()
    stats.total_samples = 100
    stats.total_modules = 50
    stats.version_distribution["17.0"] = 50
    stats.version_distribution["18.0"] = 50
    stats.scenario_distribution["portal"] = 100
    stats.difficulty_distribution[3] = 100
    stats.total_tasks = 200
    stats.total_dependencies = 50
    
    manifest_path = tmp_path / "planner_manifest.json"
    
    generate_manifest(
        output_path=manifest_path,
        dataset_name="Test Planner",
        jsonl_filename="test.jsonl",
        checksum="fake_sha256",
        stats=stats
    )
    
    assert manifest_path.exists()
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["dataset_name"] == "Test Planner"
    assert data["jsonl_filename"] == "test.jsonl"
    assert data["checksum_sha256"] == "fake_sha256"
    assert data["row_count"] == 100
    assert data["repository_counts"] == 50
    assert data["average_task_count"] == 2.0
    assert data["average_dependency_count"] == 0.25
    assert data["version_counts"]["17.0"] == 50
    assert "generation_date" in data
