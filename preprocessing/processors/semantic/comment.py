"""Comment normalization processor."""

from preprocessing.constants.framework import SEMANTIC_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class CommentProcessor(BaseProcessor):
    """
    Normalizes comments without rewriting meaning.
    Currently acts as a pass-through until specific comment styles are standardized.
    """
    
    @property
    def priority(self) -> int:
        return SEMANTIC_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        return context
