"""Conversation builder for Conversation Generator."""

from typing import List
from aiodoo_datasets.generators.conversation.analysis.result import AnalysisResult
from aiodoo_datasets.generators.conversation.domain.conversation import Conversation
from aiodoo_datasets.generators.conversation.domain.metadata import ConversationMetadata
from aiodoo_datasets.generators.conversation.domain.turn import Turn
from aiodoo_datasets.generators.conversation.enums import Role
from aiodoo_datasets.generators.conversation.builders.message_builder import MessageBuilder
from aiodoo_datasets.generators.conversation.builders.turn_builder import TurnBuilder
from aiodoo_datasets.generators.conversation.builders.reference_builder import ReferenceBuilder
from aiodoo_datasets.generators.conversation.builders.attachment_builder import AttachmentBuilder
from aiodoo_datasets.generators.conversation.factories.conversation_factory import (
    ConversationFactory,
)
from aiodoo_datasets.generators.conversation.factories.turn_factory import TurnFactory


class ConversationBuilder:
    """Builds Conversation objects from analysis results."""

    @staticmethod
    def build(
        analysis_result: AnalysisResult, metadata: ConversationMetadata, source_identifier: str
    ) -> Conversation:
        # Generate conversation ID deterministically
        conversation_id = ConversationFactory.generate_id(
            metadata.conversation_type.value, source_identifier
        )

        turns: List[Turn] = []

        # Simple generic conversation generation logic based on the evidence pool
        # In a real scenario, this would have complex routing based on ConversationType

        for idx, evidence in enumerate(analysis_result.evidence_pool):
            references = ReferenceBuilder.build_from_evidence(evidence)
            attachments = AttachmentBuilder.build_from_evidence(evidence)

            # Generate deterministic turn ID first
            turn_id = TurnFactory.generate_id(conversation_id, idx)

            # Create a simple user request and assistant response turn for the evidence
            user_msg = MessageBuilder.build(
                role=Role.USER,
                content=f"Please process the {evidence.protocol_name}.",
                turn_id=turn_id,
                sequence_index=0,
            )

            assistant_msg = MessageBuilder.build(
                role=Role.ASSISTANT,
                content=f"I have processed the {evidence.protocol_name} and extracted its contents.",
                turn_id=turn_id,
                sequence_index=1,
                references=references,
            )

            turn = TurnBuilder.build(
                conversation_id=conversation_id,
                sequence_index=idx,
                messages=(user_msg, assistant_msg),
                attachments=attachments,
            )

            turns.append(turn)

        return ConversationFactory.create(
            metadata=metadata, turns=tuple(turns), source_identifier=source_identifier
        )
