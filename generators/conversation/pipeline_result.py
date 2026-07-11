"""Pipeline result for Conversation Generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from generators.common.pipeline.status import PipelineStatus
from generators.conversation.statistics.conversation_statistics import (
    ConversationStatistics,
)


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Output summary of a pipeline execution."""

    success: bool
    diagnostics: List[str] = field(default_factory=list)
    statistics: ConversationStatistics | None = None

    @property
    def status(self) -> PipelineStatus:
        if (
            not self.success
            and any("has no turns" in str(d).lower() for d in self.diagnostics)
        ):
            return PipelineStatus.SKIPPED

        return (
            PipelineStatus.SUCCESS
            if self.success
            else PipelineStatus.FAILED
        )