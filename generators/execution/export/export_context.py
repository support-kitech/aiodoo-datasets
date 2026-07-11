"""Immutable context for the Export pipeline."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any
from pathlib import Path
from aiodoo_datasets.generators.execution.protocol.protocol_result import ProtocolResult
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics


@dataclass(frozen=True, slots=True)
class ExportContext:
    """
    Context carrying only necessary data for export.

    Attributes:
        protocol_result: The result of the protocol mapping phase.
        protocol_statistics: Statistics from the protocol mapping phase.
        export_configuration: Export-specific configuration.
        output_directory: The base path where the dataset will be written.
        export_statistics: Mutable statistics container for the export phase.
    """

    protocol_result: ProtocolResult
    protocol_statistics: ProtocolStatistics
    export_configuration: MappingProxyType[str, Any]
    output_directory: Path
    export_statistics: ExportStatistics
