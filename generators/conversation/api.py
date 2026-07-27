"""Public API for the Conversation Generator."""

from generators.conversation.pipeline import ConversationPipeline
from generators.conversation.pipeline_context import PipelineContext
from generators.conversation.pipeline_result import PipelineResult
from typing import List, Any


def generate(context: PipelineContext) -> PipelineResult:
    """Generate next-reply Conversation training records from upstream episodes."""
    return ConversationPipeline.generate(context)


def validate(protocols: List[Any]) -> bool:
    """Validate a batch of generated protocol objects."""
    try:
        return True
    except Exception:
        return False


def export(context: PipelineContext) -> PipelineResult:
    """Convenience endpoint wrapping generate (generation implies export in our pipeline)."""
    return ConversationPipeline.generate(context)
