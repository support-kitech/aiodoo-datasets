"""Public API for the Conversation Generator."""

from aiodoo_datasets.generators.conversation.pipeline import ConversationPipeline
from aiodoo_datasets.generators.conversation.pipeline_context import PipelineContext
from aiodoo_datasets.generators.conversation.pipeline_result import PipelineResult
from aiodoo_datasets.generators.conversation.validation.dataset_validator import DatasetValidator
from aiodoo_datasets.generators.conversation.protocol.domain.conversation_protocol import (
    ConversationProtocol,
)
from typing import List


def generate(context: PipelineContext) -> PipelineResult:
    """Generate a conversation dataset entry."""
    return ConversationPipeline.generate(context)


def validate(protocols: List[ConversationProtocol]) -> bool:
    """Validate a batch of generated protocol objects."""
    try:
        DatasetValidator.validate_all(protocols)
        return True
    except Exception:
        return False


def export(context: PipelineContext) -> PipelineResult:
    """Convenience endpoint wrapping generate (generation implies export in our pipeline)."""
    return ConversationPipeline.generate(context)
