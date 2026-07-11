"""JSON syntax normalization processor."""

from preprocessing.constants.framework import SYNTAX_PROCESSOR_PRIORITY
import json
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class JSONProcessor(BaseProcessor):
    """Normalizes JSON syntax (e.g., standard indentation)."""
    
    @property
    def priority(self) -> int:
        return SYNTAX_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        original = context.current_content
        if not original.strip():
            return context
            
        try:
            data = json.loads(original)
            normalized = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
            return context.with_update(current_content=normalized)
        except json.JSONDecodeError:
            # If invalid JSON, do not modify
            return context
