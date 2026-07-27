"""CLI configuration builder."""

import argparse
from generators.approval.pipeline_context import PipelineContext
from generators.approval.config.approval_config import ApprovalConfig
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.rules.registry import RuleRegistry
from generators.approval.version import SCHEMA_VERSION, __version__


def build_pipeline_context(args: argparse.Namespace) -> PipelineContext:
    """Build the pipeline context from CLI arguments."""

    config = ApprovalConfig(
        output_dir=str(args.output_dir),
        manifest_path=str(args.output_dir / "dataset_manifest.json"),
        fail_on_validation=args.fail_fast,
        strict_mode=args.fail_fast,
    )

    artifact_records = getattr(args, "artifact_records", {})
    input_protocols = {
        "planner_data": tuple(artifact_records.get("planner", ())),
        "coding_data": tuple(artifact_records.get("coding", ())),
        "repair_data": tuple(artifact_records.get("repair", ())),
        "execution_data": tuple(artifact_records.get("execution", ())),
    }

    metadata = ReviewMetadata(
        generator_version=__version__,
        protocol_version="1.0",
        schema_version=SCHEMA_VERSION,
        source_module=str(args.source_dir.name),
        odoo_version="18.0",
        odoo_edition="enterprise",
        complexity_score=10,
    )

    rule_set = RuleRegistry.compile()

    return PipelineContext(
        config=config,
        input_protocols=input_protocols,
        metadata=metadata,
        rule_set=rule_set,
        protocol_context=getattr(args, "protocol_context", None),
    )
