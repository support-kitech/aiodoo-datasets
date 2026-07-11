"""Attachment domain model for Evaluation Generator."""

from dataclasses import dataclass
from typing import Optional
from aiodoo_datasets.generators.evaluation.enums import AttachmentType

@dataclass(frozen=True, slots=True)
class EvaluationAttachment:
    """Immutable evaluation attachment (e.g. diffs, logs, code)."""
    attachment_id: str
    attachment_type: AttachmentType
    content: str
    file_path: Optional[str] = None
