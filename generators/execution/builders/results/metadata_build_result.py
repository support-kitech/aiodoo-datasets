from dataclasses import dataclass
from types import MappingProxyType
from typing import Any
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult

@dataclass(frozen=True, slots=True)
class MetadataBuildResult(BaseBuildResult):
    """Result from the MetadataBuilder."""
    metadata: MappingProxyType[str, Any]
