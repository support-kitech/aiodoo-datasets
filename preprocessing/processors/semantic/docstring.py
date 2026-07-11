"""Docstring normalization processor."""

from preprocessing.constants.framework import SEMANTIC_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class DocstringProcessor(BaseProcessor):
    """
    Normalizes docstrings without rewriting meaning.
    Currently acts as a pass-through.
    """

    @property
    def priority(self) -> int:
        return SEMANTIC_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        return context
