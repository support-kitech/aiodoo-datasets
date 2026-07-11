"""Assembles the full Planning Protocol V1 payload."""

from typing import Sequence
from preprocessing.domain.repository import PreprocessedModule
from generators.common.discovery.ast_parser import PythonKnowledge
from generators.common.discovery.xml_parser import XMLKnowledge
from generators.common.discovery.classifier import Scenario
from generators.planner.validation.schema import PlanPayload, Analysis
from generators.planner.protocol.task_builder import build_tasks
from generators.planner.protocol.action_builder import build_actions


def build_plan_payload(
    module: PreprocessedModule,
    scenario: Scenario,
    python_data: Sequence[PythonKnowledge],
    xml_data: Sequence[XMLKnowledge],
) -> PlanPayload:
    """Constructs the deterministic PlanPayload."""

    tasks = build_tasks(python_data, xml_data)
    actions = build_actions(tasks)

    analysis = Analysis(
        summary=f"Implementing {scenario.name} architecture for {module.name}.",
        risks=["Dependency conflicts", "Backward compatibility"],
    )

    return PlanPayload(
        goal=f"Build {module.metadata.get('name', module.name)} features matching {scenario.name}.",
        workspace=f"src/{module.name}",
        analysis=analysis,
        tasks=tasks,
        execution=actions,
        summary="Plan compiled successfully based on structural analysis.",
    )
