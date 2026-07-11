"""Attachment Factory for Evaluation Generator."""

import hashlib
from typing import Optional
from generators.evaluation.domain.attachment import EvaluationAttachment
from generators.evaluation.enums import AttachmentType


class AttachmentFactory:
    """Factory for creating immutable EvaluationAttachment objects."""

    @staticmethod
    def generate_id(case_id: str, attachment_type: AttachmentType, sequence_index: int) -> str:
        """Generate a deterministic attachment ID."""
        hash_input = f"ATT:{case_id}:{attachment_type.value}:{sequence_index}"
        att_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"ATT-{att_hash}"

    @staticmethod
    def create(
        case_id: str,
        attachment_type: AttachmentType,
        sequence_index: int,
        content: str,
        file_path: Optional[str] = None,
    ) -> EvaluationAttachment:
        """Create an attachment with a hash-based deterministic ID."""
        attachment_id = AttachmentFactory.generate_id(case_id, attachment_type, sequence_index)
        return EvaluationAttachment(
            attachment_id=attachment_id,
            attachment_type=attachment_type,
            content=content,
            file_path=file_path,
        )
