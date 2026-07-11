"""Pipeline orchestrator for Conversation Generator."""

from types import MappingProxyType
from generators.conversation.pipeline_context import PipelineContext
from generators.conversation.pipeline_result import PipelineResult
from generators.conversation.exceptions import ConversationValidationError
from generators.conversation.analysis.context import AnalysisContext
from generators.conversation.analysis.evidence_extractor import EvidenceExtractor
from generators.conversation.builders.conversation_builder import (
    ConversationBuilder,
)
from generators.conversation.validation.conversation_validator import (
    ConversationValidator,
)
from generators.conversation.statistics.conversation_statistics import (
    ConversationStatistics,
)


class ConversationPipeline:
    """Orchestrates the conversation generation process."""

    @staticmethod
    def generate(context: PipelineContext) -> PipelineResult:
        """Execute the full pipeline."""
        stats = ConversationStatistics()

        try:
            # 1. Analysis Layer
            analysis_ctx = AnalysisContext(
                input_protocols=MappingProxyType(context.input_protocols)
            )
            analysis_result = EvidenceExtractor.extract(analysis_ctx)

            # 2. Builder Layer
            conversation = ConversationBuilder.build(
                analysis_result=analysis_result,
                metadata=context.metadata,
                source_identifier=context.source_identifier,
            )

            # 3. Validation Layer (Domain)
            if context.strict_mode:
                ConversationValidator.validate(conversation)

            # 4. Protocol Mapping Layer (Removed)
            # 5. Validation Layer (Protocol) (Removed)

            # 6. Statistics (handled by DatasetWriter below)

            # 7. Export Layer
            from pathlib import Path
            from generators.common.export.writer import DatasetWriter

            writer = DatasetWriter(
                output_dir=Path(context.output_dir),
                stats=stats,
                filename="conversation_dataset.jsonl",
                dataset_name="conversation",
            )
            # Add protocol hash to the domain object's metadata before export
            if hasattr(context, "protocol_context") and context.protocol_context:
                protocol_hash = context.protocol_context.dataset.identifier.hash_value
                if hasattr(conversation, "metadata"):
                    conversation.metadata.protocol_hash = protocol_hash
            
            # Write the domain object directly
            writer.write_record(conversation)
            writer.export_manifest()
            writer.export_statistics()

            return PipelineResult(success=True, statistics=stats)

        except ConversationValidationError as e:
            return PipelineResult(success=False, diagnostics=[f"Validation failed: {str(e)}"])
        except Exception as e:
            return PipelineResult(success=False, diagnostics=[f"Pipeline failed: {str(e)}"])
