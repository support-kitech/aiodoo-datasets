"""Pipeline orchestrator for Conversation Generator."""

import dataclasses
import hashlib
import json
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
            required_inputs = (
                "planner_protocol",
                "coding_protocol",
                "repair_protocol",
                "context_protocol",
                "execution_protocol",
                "approval_protocol",
            )
            missing_inputs = tuple(
                name for name in required_inputs if not context.input_protocols.get(name)
            )
            if missing_inputs:
                return PipelineResult(
                    success=False,
                    diagnostics=[
                        f"Missing required upstream artifact: {name}" for name in missing_inputs
                    ],
                )

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

            output = dataclasses.asdict(conversation)
            protocol_hash = hashlib.sha256(
                json.dumps(output, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
            ).hexdigest()
            record = {
                "instruction": (
                    "Create an integrated conversation over the generated AIODOO datasets."
                ),
                "context": {
                    "source_identifier": context.source_identifier,
                    "upstream_generators": sorted(context.input_protocols.keys()),
                    "evidence_count": len(analysis_result.evidence_pool),
                },
                "output": output,
                "metadata": {
                    "module": context.metadata.source_module,
                    "protocol_hash": protocol_hash,
                    "generator_version": context.metadata.generator_version,
                    "protocol_version": context.metadata.protocol_version,
                    "schema_version": context.metadata.schema_version,
                    "conversation_type": context.metadata.conversation_type.value,
                },
            }

            writer.write_record(record)
            writer.export_manifest("conversation_manifest.json")
            writer.export_statistics("conversation_statistics.json")

            return PipelineResult(success=True, statistics=stats)

        except ConversationValidationError as e:
            return PipelineResult(success=False, diagnostics=[f"Validation failed: {str(e)}"])
        except Exception as e:
            return PipelineResult(success=False, diagnostics=[f"Pipeline failed: {str(e)}"])
