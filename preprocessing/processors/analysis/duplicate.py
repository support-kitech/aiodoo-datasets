"""Duplicate analysis processor."""

from preprocessing.constants.framework import ANALYSIS_PROCESSOR_PRIORITY
import hashlib
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class DuplicateProcessor(BaseProcessor):
    """
    Computes duplicate status by hashing the normalized content.
    Never deletes files, only classifies them.
    """
    
    def __init__(self):
        # Maps content_hash -> canonical_file_path
        self._seen_hashes: dict[str, str] = {}
        
    @property
    def priority(self) -> int:
        return ANALYSIS_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        content = context.current_content
        if not content:
            content_hash = hashlib.sha256(b"").hexdigest()
        else:
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            
        file_path_str = context.normalized_path.as_posix()
        is_duplicate = content_hash in self._seen_hashes
        
        if is_duplicate:
            canonical = self._seen_hashes[content_hash]
            status = "DUPLICATE"
        else:
            self._seen_hashes[content_hash] = file_path_str
            canonical = file_path_str
            status = "UNIQUE"
        
        new_meta = dict(context.metadata)
        new_meta["duplicate_status"] = status
        new_meta["duplicate_group_id"] = content_hash
        new_meta["canonical_file"] = canonical
        new_meta["reference_target"] = canonical if is_duplicate else None
        
        from types import MappingProxyType
        
        new_stats = context.statistics.add(duplicates_detected=1 if is_duplicate else 0)
        
        return context.with_update(
            metadata=MappingProxyType(new_meta),
            statistics=new_stats
        )
