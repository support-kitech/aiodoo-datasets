"""Metadata normalization processor."""

from preprocessing.constants.framework import METADATA_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class MetadataProcessor(BaseProcessor):
    """
    Attaches deterministic metadata.
    """
    
    @property
    def priority(self) -> int:
        return METADATA_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        new_meta = dict(context.metadata)
        new_meta["processed_by_framework"] = True
        
        from types import MappingProxyType
        return context.with_update(metadata=MappingProxyType(new_meta))
