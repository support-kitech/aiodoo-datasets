"""Pipeline orchestrator for Conversation Generator (next-reply training grain)."""

from __future__ import annotations

from pathlib import Path

from generators.conversation.analysis.episode import EpisodeReconstructor
from generators.conversation.analysis.slicer import DialogueSlicer
from generators.conversation.builders.slice_record_builder import SliceRecordBuilder
from generators.conversation.pipeline_context import PipelineContext
from generators.conversation.pipeline_result import PipelineResult
from generators.conversation.policy import MIN_PRODUCTION_RECORDS, REQUIRED_PROTOCOL_KEYS
from generators.conversation.statistics.conversation_statistics import ConversationStatistics
from generators.common.export.writer import DatasetWriter


class ConversationPipeline:
    """Orchestrates episode reconstruction → slicing → N JSONL records."""

    @staticmethod
    def generate(context: PipelineContext) -> PipelineResult:
        """Execute the full pipeline."""
        stats = ConversationStatistics()
        diagnostics: list[str] = []

        try:
            missing_inputs = tuple(
                name for name in REQUIRED_PROTOCOL_KEYS if not context.input_protocols.get(name)
            )
            if missing_inputs:
                return PipelineResult(
                    success=False,
                    diagnostics=[
                        f"Missing required upstream artifact: {name}" for name in missing_inputs
                    ],
                )

            episodes = EpisodeReconstructor.reconstruct(context.input_protocols)
            if not episodes:
                return PipelineResult(
                    success=False,
                    diagnostics=["No conversation episodes reconstructed from upstream datasets"],
                )

            slices = DialogueSlicer.slice_many(episodes)
            if len(slices) < MIN_PRODUCTION_RECORDS:
                return PipelineResult(
                    success=False,
                    diagnostics=[
                        "Conversation production dataset rejected: "
                        f"only {len(slices)} record(s); "
                        f"minimum is {MIN_PRODUCTION_RECORDS} "
                        "(single integrated conversation grain forbidden)"
                    ],
                )

            writer = DatasetWriter(
                output_dir=Path(context.output_dir),
                stats=stats,
                filename="conversation_dataset.jsonl",
                dataset_name="conversation",
            )

            for training_slice in slices:
                record = SliceRecordBuilder.build(
                    training_slice,
                    base_metadata=context.metadata,
                )
                writer.write_record(record)

            stats.episodes_generated = len(episodes)
            stats.training_examples = len(slices)

            writer.export_manifest("conversation_manifest.json")
            writer.export_statistics("conversation_statistics.json")

            return PipelineResult(
                success=True,
                statistics=stats,
                diagnostics=diagnostics,
                record_count=len(slices),
                episode_count=len(episodes),
            )

        except Exception as e:
            return PipelineResult(success=False, diagnostics=[f"Pipeline failed: {str(e)}"])
