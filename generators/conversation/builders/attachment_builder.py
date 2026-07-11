"""Attachment builder for Conversation Generator."""

from typing import Tuple
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.attachment import Attachment


class AttachmentBuilder:
    """Extracts attachments directly from analysis evidence."""

    @staticmethod
    def build_from_evidence(evidence: ExtractedEvidence) -> Tuple[Attachment, ...]:
        return evidence.attachments  # type: ignore[no-any-return]
