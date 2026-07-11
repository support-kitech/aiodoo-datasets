"""Base reporter abstraction."""

import abc
from pathlib import Path

from validation.domain.results import ValidationReport


class BaseReporter(abc.ABC):
    """Abstract base class for all validation reporters."""

    @abc.abstractmethod
    def report(self, report: ValidationReport, output_dir: Path) -> None:
        """Format and output the validation report."""
