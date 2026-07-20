"""Tests for generators.common.contract.adapters.

Every ``project_*`` function is checked against (a) a minimal record shaped
like this repository's real generator output, and (b) records missing the
structure it needs, to prove `ContractAdapterError` is raised (never a bare
`KeyError`/`TypeError`) instead of crashing or silently succeeding.
"""

from __future__ import annotations

import pytest
from aiodoo_contract.schemas.coding import CodingRequest, CodingResponse
from aiodoo_contract.schemas.enums import ApprovalStatus, ConversationRole, ExecutionStatus
from aiodoo_contract.schemas.planner import PlannerRequest, PlannerResponse
from aiodoo_contract.schemas.repair import RepairRequest, RepairResponse
from aiodoo_contract.validators import ContractValidator

from generators.common.contract.adapters import (
    ContractAdapterError,
    SUPPORTED_CAPABILITIES,
    project_approval,
    project_coding,
    project_conversation,
    project_execution,
    project_planner,
    project_record,
    project_repair,
)

_validator = ContractValidator()


def _assert_valid(projection) -> None:  # type: ignore[no-untyped-def]
    request_result = _validator.validate_request(projection.request)
    response_result = _validator.validate_response(projection.response)
    assert request_result.valid, request_result.issues
    assert response_result.valid, response_result.issues


class TestSupportedCapabilities:
    def test_matches_expected_set(self) -> None:
        assert set(SUPPORTED_CAPABILITIES) == {
            "planner",
            "coding",
            "repair",
            "execution",
            "conversation",
            "approval",
        }

    def test_project_record_unknown_capability_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_record("not-a-capability", {})

    def test_project_record_dispatches(self) -> None:
        record = {
            "instruction": "Do a thing.",
            "input": "ctx",
            "output": {"goal": "Do a thing.", "tasks": [{"id": "t1", "title": "Step one"}]},
        }
        projection = project_record("planner", record)
        assert projection.capability == "planner"
        assert isinstance(projection.request, PlannerRequest)
        assert isinstance(projection.response, PlannerResponse)


class TestProjectPlanner:
    def test_valid_record_projects_and_validates(self) -> None:
        record = {
            "instruction": "Build feature X",
            "input": "Target Odoo Version: 17.0",
            "output": {
                "goal": "Build feature X",
                "tasks": [
                    {"id": "t1", "title": "Create model", "priority": "medium"},
                    {"id": "t2", "title": "Add view", "priority": "low"},
                ],
            },
        }
        projection = project_planner(record)
        assert projection.capability == "planner"
        assert len(projection.response.steps) == 2
        _assert_valid(projection)

    def test_missing_output_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_planner({"instruction": "x"})

    def test_missing_tasks_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_planner({"instruction": "x", "output": {"goal": "g"}})

    def test_no_usable_goal_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_planner({"output": {"tasks": [{"id": "t1", "title": "Step"}]}})


class TestProjectCoding:
    def test_valid_record_projects_and_validates(self) -> None:
        record = {
            "instruction": "Implement the feature.",
            "output": {
                "goal": "Implement the feature",
                "artifacts": [
                    {"path": "models/foo.py", "diff": "", "reason": "add model"},
                    {"path": "views/foo_views.xml", "content": "<xml/>"},
                ],
            },
        }
        projection = project_coding(record)
        assert isinstance(projection.request, CodingRequest)
        assert isinstance(projection.response, CodingResponse)
        assert len(projection.response.edits) == 2
        assert projection.response.edits[1].content == "<xml/>"
        _assert_valid(projection)

    def test_missing_instruction_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_coding({"output": {"artifacts": [{"path": "a.py"}]}})

    def test_no_artifacts_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_coding({"instruction": "x", "output": {"artifacts": []}})

    def test_artifacts_without_path_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_coding({"instruction": "x", "output": {"artifacts": [{"type": "file"}]}})


class TestProjectRepair:
    def test_valid_record_applies_search_replace_and_validates(self) -> None:
        record = {
            "instruction": "Fix the bug.",
            "output": {
                "tasks": [
                    {
                        "problem": {
                            "description": "Direct SQL bypasses ORM rules.",
                            "severity": "high",
                        },
                        "root_cause": {"analysis": "cr.execute used directly."},
                        "artifacts": [
                            {"path": "models/foo.py", "content": "self.env.cr.execute(x)"}
                        ],
                        "expected_outcome": {
                            "operations": [
                                {
                                    "operation": "replace",
                                    "search": "self.env.cr.execute",
                                    "replace": "self.env.sudo().cr.execute",
                                }
                            ]
                        },
                    }
                ]
            },
        }
        projection = project_repair(record)
        assert isinstance(projection.request, RepairRequest)
        assert isinstance(projection.response, RepairResponse)
        assert projection.response.fix.edits[0].content == "self.env.sudo().cr.execute(x)"
        assert projection.response.fix.confidence == pytest.approx(0.65)
        _assert_valid(projection)

    def test_missing_output_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_repair({"instruction": "x"})

    def test_no_tasks_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_repair({"output": {"tasks": []}})

    def test_tasks_without_artifacts_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_repair({"output": {"tasks": [{"problem": {"description": "x"}}]}})


class TestProjectExecution:
    def test_valid_record_with_steps_is_succeeded(self) -> None:
        record = {
            "instruction": "Execute the plan.",
            "output": {
                "module": "my_module",
                "steps": [{"id": "s1"}],
                "summary": "Executed 1 step.",
            },
        }
        projection = project_execution(record)
        assert projection.response.status == ExecutionStatus.SUCCEEDED
        assert projection.request.working_directory == "my_module"
        _assert_valid(projection)

    def test_no_steps_is_pending(self) -> None:
        record = {"instruction": "Execute.", "output": {"module": "m", "steps": []}}
        projection = project_execution(record)
        assert projection.response.status == ExecutionStatus.PENDING
        _assert_valid(projection)

    def test_missing_instruction_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_execution({"output": {"module": "m"}})


class TestProjectConversation:
    def test_valid_record_projects_and_validates(self) -> None:
        record = {
            "output": {
                "turns": [
                    {
                        "messages": [
                            {"role": "user", "content": "Please do X."},
                            {"role": "assistant", "content": "Done."},
                        ]
                    }
                ]
            }
        }
        projection = project_conversation(record)
        assert projection.request.turns[0].role == ConversationRole.USER
        assert projection.response.reply.role == ConversationRole.ASSISTANT
        assert projection.response.reply.content == "Done."
        _assert_valid(projection)

    def test_reviewer_role_maps_to_assistant(self) -> None:
        record = {
            "output": {
                "turns": [
                    {
                        "messages": [
                            {"role": "user", "content": "Review this."},
                            {"role": "reviewer", "content": "Looks good."},
                        ]
                    }
                ]
            }
        }
        projection = project_conversation(record)
        assert projection.response.reply.role == ConversationRole.ASSISTANT
        _assert_valid(projection)

    def test_too_few_messages_raises(self) -> None:
        record = {"output": {"turns": [{"messages": [{"role": "user", "content": "Only one."}]}]}}
        with pytest.raises(ContractAdapterError):
            project_conversation(record)

    def test_no_turns_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_conversation({"output": {"turns": []}})


class TestProjectApproval:
    def test_approved_decision_projects_and_validates(self) -> None:
        record = {
            "review_id": "REV-1",
            "metadata": {"source_module": "my_module"},
            "decision": {"status": "APPROVED", "reasoning": "Meets standards."},
            "evidence": [{"evidence_id": "E1"}],
        }
        projection = project_approval(record)
        assert projection.response.status == ApprovalStatus.APPROVED
        assert projection.request.payload["evidence_count"] == 1
        _assert_valid(projection)

    def test_changes_requested_maps_to_pending(self) -> None:
        record = {
            "metadata": {"module": "my_module"},
            "decision": {"status": "CHANGES_REQUESTED"},
        }
        projection = project_approval(record)
        assert projection.response.status == ApprovalStatus.PENDING
        _assert_valid(projection)

    def test_missing_decision_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_approval({"metadata": {}})

    def test_unmappable_status_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            project_approval({"decision": {"status": "ON_HOLD"}})
