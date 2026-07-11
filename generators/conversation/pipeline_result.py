"""Pipeline result for Conversation Generator."""

from dataclasses import dataclass, field
from typing import List
from aiodoo_datasets.generators.conversation.statistics.conversation_statistics import (
    ConversationStatistics,
)


@dataclass
class PipelineResult:
    """Output summary of a pipeline execution."""

    success: bool
    diagnostics: List[str] = field(default_factory=list)
    statistics: ConversationStatistics = None
