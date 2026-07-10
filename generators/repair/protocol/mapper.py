"""Maps repair scenarios to the Repair Protocol V1 JSON Schema."""

from pathlib import Path
from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from aiodoo_datasets.generators.repair.validation.schema import (
    RepairTask, Problem, RootCause, Artifact, ExpectedOutcome, RepairPayload
)
from aiodoo_datasets.generators.repair.analysis.rules.base import RepairOpportunity

def build_repair_task(opp: RepairOpportunity, base_path: Path) -> RepairTask:
    start_line = None
    end_line = None
    try:
        full_path = base_path / opp.artifact_path
        lines = full_path.read_text(encoding="utf-8").splitlines()
        start = max(0, opp.line_num - 11)
        end = opp.line_num + 10
        content = "\n".join(lines[start:end])
        start_line = start + 1
        end_line = min(len(lines), end)
    except Exception:
        content = opp.code_snippet
        
    artifact = Artifact(
        id=opp.artifact_path.replace("/", "_").replace(".", "_"),
        path=opp.artifact_path,
        type=opp.artifact_type,
        start_line=start_line,
        end_line=end_line,
        content=content
    )
    
    return RepairTask(
        id=opp.id,
        problem=Problem(
            description=opp.problem_description,
            severity=opp.severity,
            location=opp.location
        ),
        root_cause=RootCause(
            analysis=opp.root_cause
        ),
        context=[artifact],
        artifacts=[artifact],
        expected_outcome=ExpectedOutcome(
            operations=opp.operations,
            explanation=opp.explanation
        ),
        constraints=[],
        metadata={
            "rule_id": opp.rule_id,
            "rule_name": opp.rule_title,
            "category": opp.category,
            "severity": opp.severity.value if hasattr(opp.severity, "value") else opp.severity,
            "detector": opp.detector_name,
            "supported_versions": opp.supported_versions,
            "confidence": 1.0
        }
    )

def build_repair_payload(module: OdooModule, opportunities: list[RepairOpportunity]) -> RepairPayload:
    tasks = [build_repair_task(opp, module.path) for opp in opportunities]
    return RepairPayload(
        goal=f"Repair {len(tasks)} issues in {module.name}",
        workspace=f"src/{module.name}",
        tasks=tasks,
        summary=f"Found {len(tasks)} deterministic repair opportunities."
    )
