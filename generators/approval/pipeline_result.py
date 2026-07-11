"""Pipeline result for the Approval Generator."""

from dataclasses import dataclass, field
from typing import Tuple, Mapping, Any
from types import MappingProxyType
from aiodoo_datasets.generators.approval.protocol.domain.approval_protocol import ApprovalProtocol


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """The complete result of the approval pipeline."""

    success: bool
    approval_protocol: ApprovalProtocol
    statistics: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)
    exported_files: Tuple[str, ...] = field(default_factory=tuple)
