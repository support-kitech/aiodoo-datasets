"""CLI configuration builder."""

import argparse
from aiodoo_datasets.generators.approval.pipeline_context import PipelineContext
from aiodoo_datasets.generators.approval.config.approval_config import ApprovalConfig
from aiodoo_datasets.generators.approval.domain.metadata import ReviewMetadata
from aiodoo_datasets.generators.approval.rules.registry import RuleRegistry


def build_pipeline_context(args: argparse.Namespace) -> PipelineContext:
    """Build the pipeline context from CLI arguments."""

    config = ApprovalConfig(
        output_dir=str(args.output_dir),
        manifest_path=str(args.output_dir / "dataset_manifest.json"),
        fail_on_validation=args.fail_fast,
        strict_mode=args.fail_fast,
    )

    # In a real scenario, this would dynamically parse the protocols from input paths
    # For now, we initialize an empty context to satisfy the pipeline
    input_protocols = {}

    metadata = ReviewMetadata(
        generator_version="1.0.0",
        protocol_version="1.0",
        schema_version="1.0",
        source_module=str(args.source_dir.name),
        odoo_version="18.0",
        odoo_edition="enterprise",
        complexity_score=10,
    )

    rule_set = RuleRegistry.compile()

    return PipelineContext(
        config=config, input_protocols=input_protocols, metadata=metadata, rule_set=rule_set
    )
