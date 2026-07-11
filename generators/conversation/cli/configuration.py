"""CLI configuration for Conversation Generator."""

import argparse
from aiodoo_datasets.generators.conversation.pipeline_context import PipelineContext
from aiodoo_datasets.generators.conversation.builders.metadata_builder import MetadataBuilder
from aiodoo_datasets.generators.conversation.enums import ConversationType


def build_pipeline_context(args: argparse.Namespace) -> PipelineContext:
    """Build the pipeline context from CLI arguments."""

    # In a real environment, this would read actual protocols from args.source_dir
    input_protocols = {}

    metadata = MetadataBuilder.build(
        conversation_type=ConversationType.PLANNING, source_module=str(args.source_dir.name)
    )

    return PipelineContext(
        input_protocols=input_protocols,
        metadata=metadata,
        output_dir=str(args.output_dir),
        source_identifier=str(args.source_dir.name),
        strict_mode=args.fail_fast,
    )
