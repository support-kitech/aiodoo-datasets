"""Python syntax normalization processor."""

from preprocessing.constants.framework import SYNTAX_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class PythonProcessor(BaseProcessor):
    """
    Normalizes Python syntax.
    Currently acts as a pass-through to avoid stripping comments via AST.
    """
    
    @property
    def priority(self) -> int:
        return SYNTAX_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        # Future enhancement: Safe AST formatting (e.g., using Black API)
        return context
