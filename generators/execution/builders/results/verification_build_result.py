from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.domain.execution_verification import ExecutionVerification


@dataclass(frozen=True, slots=True)
class VerificationBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the VerificationBuilder."""

    verifications: tuple[ExecutionVerification, ...]
