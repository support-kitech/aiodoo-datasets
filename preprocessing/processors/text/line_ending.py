"""Line ending normalization processor."""

from preprocessing.constants.framework import TEXT_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class LineEndingProcessor(BaseProcessor):
    """
    Normalizes line endings to Unix style (LF).
    """

    @property
    def priority(self) -> int:
        return TEXT_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        original = context.current_content
        if not original:
            return context

        # Replace CRLF and CR with LF
        normalized_content = original.replace("\r\n", "\n").replace("\r", "\n")

        return context.with_update(current_content=normalized_content)
