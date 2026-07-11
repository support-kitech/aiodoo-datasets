"""Pipeline result for the Approval Generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Mapping, Tuple

# Removed ApprovalProtocol import
if TYPE_CHECKING:
    from generators.common.pipeline.status import PipelineStatus


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """The complete result of the approval pipeline."""

    success: bool
    approval_protocol: Any = None
    statistics: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)
    exported_files: Tuple[str, ...] = field(default_factory=tuple)

    @property
    def status(self) -> PipelineStatus:
        from generators.common.pipeline.status import PipelineStatus

        return PipelineStatus.SUCCESS if self.success else PipelineStatus.FAILED
