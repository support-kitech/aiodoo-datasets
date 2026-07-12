"""CLI configuration for Conversation Generator."""

import argparse
from generators.conversation.pipeline_context import PipelineContext
from generators.conversation.builders.metadata_builder import MetadataBuilder
from generators.conversation.enums import ConversationType


def build_pipeline_context(args: argparse.Namespace) -> PipelineContext:
    """Build the pipeline context from CLI arguments."""

    artifact_records = getattr(args, "artifact_records", {})
    input_protocols = {
        "planner_protocol": tuple(artifact_records.get("planner", ())),
        "coding_protocol": tuple(artifact_records.get("coding", ())),
        "repair_protocol": tuple(artifact_records.get("repair", ())),
        "context_protocol": tuple(artifact_records.get("context", ())),
        "execution_protocol": tuple(artifact_records.get("execution", ())),
        "approval_protocol": tuple(artifact_records.get("approval", ())),
    }

    metadata = MetadataBuilder.build(
        conversation_type=ConversationType.PLANNING, source_module=str(args.source_dir.name)
    )

    return PipelineContext(
        input_protocols=input_protocols,
        metadata=metadata,
        output_dir=str(args.output_dir),
        source_identifier=str(args.source_dir.name),
        strict_mode=args.fail_fast,
        protocol_context=getattr(args, "protocol_context", None),
    )
