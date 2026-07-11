"""Path normalization processor."""

from preprocessing.constants.framework import METADATA_PROCESSOR_PRIORITY
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class PathNormalizer(BaseProcessor):
    """
    Normalizes the file path to a canonical OS-independent format.
    """
    
    @property
    def priority(self) -> int:
        return METADATA_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        # pathlib.Path already normalizes paths, we just ensure it is canonical 
        # relative to some root, but for now we just use the as_posix() format.
        # Actually, normalized_path is a Path. We just ensure it is clean.
        normalized = context.normalized_path.resolve() if context.normalized_path.exists() else context.normalized_path
        
        return context.with_update(normalized_path=normalized)
