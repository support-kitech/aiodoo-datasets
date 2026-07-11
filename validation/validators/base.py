"""Base validator abstraction."""

import abc

from validation.domain.models import ValidationContext
from validation.domain.results import ValidationResult


class BaseValidator(abc.ABC):
    """Abstract base class for all validators."""

    @abc.abstractmethod
    def validate(self, context: ValidationContext) -> ValidationResult:
        """Execute validation and return an immutable result."""
