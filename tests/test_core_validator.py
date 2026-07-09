"""Tests for the pluggable CoreProtocolValidator."""

import pytest
from typing import Any
from aiodoo_datasets.generators.planner.validation.core_validator import CoreProtocolValidator


def test_core_protocol_validator_initialization():
    validator = CoreProtocolValidator()
    # It should initialize without crashing, even if core is not found (is_available=False)
    assert hasattr(validator, "is_available")


def test_core_protocol_validator_valid_payload():
    validator = CoreProtocolValidator()
    if not validator.is_available:
        pytest.skip("AIODOO Core not found, skipping deep validation test.")

    valid_payload = {
        "goal": "Build a module",
        "workspace": "src/module",
        "analysis": {"summary": "Valid summary", "risks": []},
        "tasks": [
            {
                "id": "t1",
                "title": "Valid Task",
                "description": "Desc",
                "complexity": 1,
                "dependencies": [],
                "estimated_files": 1,
                "estimated_time": 10
            }
        ],
        "execution": [
            {
                "id": "act_t1",
                "action": "create_file",
                "args": {"path": "test.py"},
                "reason": "Test",
                "expected_result": "Success",
                "depends_on": [],
                "continue_on_error": False
            }
        ],
        "summary": "Overall summary"
    }
    
    # Should not raise
    validator.validate_plan(valid_payload)


def test_core_protocol_validator_invalid_payload():
    validator = CoreProtocolValidator()
    if not validator.is_available:
        pytest.skip("AIODOO Core not found, skipping deep validation test.")

    invalid_payload = {
        "goal": "Build a module",
        "workspace": "src/module",
        "analysis": {"summary": "Valid summary", "risks": []},
        "tasks": [
            {
                "id": "t1",
                "title": "Valid Task",
                "description": "Desc",
                "complexity": -1,  # INVALID: Complexity cannot be negative
                "dependencies": [],
                "estimated_files": 1,
                "estimated_time": 10
            }
        ],
        "execution": [],
        "summary": "Overall summary"
    }
    
    with pytest.raises(ValueError, match="Core Protocol Validation Failed"):
        validator.validate_plan(invalid_payload)
