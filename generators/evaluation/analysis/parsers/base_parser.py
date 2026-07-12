"""Base Parser for Evaluation Generator."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseParser(ABC):
    """Abstract base class for all protocol parsers."""

    source_type = "unknown"

    @abstractmethod
    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Parse protocol into read-only deterministic extracted evidence."""
        pass

    def _aggregate_records(self, protocol_object: Any) -> Dict[str, Any]:
        records = (
            protocol_object if isinstance(protocol_object, (list, tuple)) else (protocol_object,)
        )
        sample_ids = []
        source_module = "unknown"
        for record in records[:10]:
            if not isinstance(record, dict):
                continue
            sample_ids.append(self._record_id(record))
            metadata = record.get("metadata", {})
            if isinstance(metadata, dict):
                source_module = str(
                    metadata.get("module") or metadata.get("source_module") or source_module
                )
        return {
            "source_type": self.source_type,
            "record_count": len(records),
            "sample_ids": tuple(sample_ids),
            "source_module": source_module,
        }

    @staticmethod
    def _record_id(record: Dict[str, Any]) -> str:
        for key in ("id", "review_id", "evaluation_id", "conversation_id"):
            value = record.get(key)
            if value:
                return str(value)
        metadata = record.get("metadata", {})
        if isinstance(metadata, dict) and metadata.get("protocol_hash"):
            return str(metadata["protocol_hash"])
        return "unknown"
