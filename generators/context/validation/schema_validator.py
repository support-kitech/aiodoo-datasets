"""Schema Validator for Context Protocol V1."""

import logging
from pydantic import ValidationError

from generators.context.protocol.schema import ContextTask
from generators.context.validation.result import ValidationResult

logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    Validates strict Pydantic V2 structural schema integrity.
    Reports validation errors. Never modifies the data.
    """

    def validate(self, task: ContextTask) -> ValidationResult:
        """
        Validates the Pydantic schema structure.

        Args:
            task: The ContextTask to validate.

        Returns:
            ValidationResult containing status and any errors.
        """
        errors = []
        try:
            ContextTask.model_validate(task.model_dump())
            return ValidationResult(valid=True, validator=self.__class__.__name__)
        except ValidationError as e:
            errors.append(str(e))
            logger.error("Schema Validation Failed for Task %s: %s", task.id, e)
            return ValidationResult(valid=False, validator=self.__class__.__name__, errors=errors)
        except Exception as e:
            errors.append(str(e))
            logger.error("Unexpected error during Schema Validation: %s", e)
            return ValidationResult(valid=False, validator=self.__class__.__name__, errors=errors)
