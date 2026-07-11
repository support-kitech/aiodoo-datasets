"""Markdown syntax normalization processor."""

from preprocessing.constants.framework import SYNTAX_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class MarkdownProcessor(BaseProcessor):
    """Normalizes Markdown syntax."""
    
    @property
    def priority(self) -> int:
        return SYNTAX_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        return context
