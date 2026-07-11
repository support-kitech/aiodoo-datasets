"""Whitespace normalization processor."""

from preprocessing.constants.framework import TEXT_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class WhitespaceProcessor(BaseProcessor):
    """
    Normalizes trailing whitespace and blank lines.
    Removes trailing whitespace from each line.
    """
    
    @property
    def priority(self) -> int:
        return TEXT_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        original = context.current_content
        if not original:
            return context
            
        lines = original.splitlines()
        normalized_lines = [line.rstrip() for line in lines]
        
        # If the original ended with a newline, preserve one trailing newline
        normalized_content = "\n".join(normalized_lines)
        if original.endswith(("\n", "\r\n")):
            normalized_content += "\n"
            
        removed_bytes = len(original) - len(normalized_content)
        
        new_stats = context.statistics.add(whitespace_removed_bytes=max(0, removed_bytes))
        
        return context.with_update(
            current_content=normalized_content,
            statistics=new_stats
        )
