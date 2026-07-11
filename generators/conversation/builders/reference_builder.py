"""Reference builder for Conversation Generator."""

from typing import Tuple
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence
from aiodoo_datasets.generators.conversation.domain.reference import Reference


class ReferenceBuilder:
    """Extracts references directly from analysis evidence."""

    @staticmethod
    def build_from_evidence(evidence: ExtractedEvidence) -> Tuple[Reference, ...]:
        return evidence.references  # type: ignore[no-any-return]
