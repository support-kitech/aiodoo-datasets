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
from generators.conversation.protocol.mapper import ProtocolMapper
from generators.conversation.validation.conversation_validator import (
    ConversationValidator,
)
from generators.conversation.validation.protocol_validator import ProtocolValidator
from generators.conversation.validation.dataset_validator import DatasetValidator
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

            # 4. Protocol Mapping Layer
            protocol = ProtocolMapper.map_conversation(conversation)

            # 5. Validation Layer (Protocol)
            if context.strict_mode:
                ProtocolValidator.validate(protocol)
                # Dataset validation is a single item here, but could be extended to validate against history if needed.
                DatasetValidator.validate_all([protocol])

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
            writer.write_record(protocol)
            writer.export_manifest()
            writer.export_statistics()

            return PipelineResult(success=True, statistics=stats)

        except ConversationValidationError as e:
            return PipelineResult(success=False, diagnostics=[f"Validation failed: {str(e)}"])
        except Exception as e:
            return PipelineResult(success=False, diagnostics=[f"Pipeline failed: {str(e)}"])
