"""Attachment Builder for Evaluation Generator."""

from typing import Optional
from aiodoo_datasets.generators.evaluation.domain.attachment import EvaluationAttachment
from aiodoo_datasets.generators.evaluation.factories.attachment_factory import AttachmentFactory
from aiodoo_datasets.generators.evaluation.enums import AttachmentType


class AttachmentBuilder:
    """Builds EvaluationAttachment objects securely."""

    @staticmethod
    def build(
        case_id: str,
        attachment_type: AttachmentType,
        sequence_index: int,
        content: str,
        file_path: Optional[str] = None,
    ) -> EvaluationAttachment:
        """Build attachment by delegating ID generation to the factory."""
        # Factory strictly manages deterministic instantiation internally
        return AttachmentFactory.create(
            case_id=case_id,
            attachment_type=attachment_type,
            sequence_index=sequence_index,
            content=content,
            file_path=file_path,
        )
