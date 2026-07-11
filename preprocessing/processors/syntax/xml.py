"""XML syntax normalization processor."""

from preprocessing.constants.framework import SYNTAX_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class XMLProcessor(BaseProcessor):
    """Normalizes XML syntax."""
    
    @property
    def priority(self) -> int:
        return SYNTAX_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        return context
