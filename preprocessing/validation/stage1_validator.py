"""Stage 1 Validator: Pre-processing input validation."""

from sources.domain.context import RepositoryContext
from preprocessing.exceptions import PreprocessingValidationError


class Stage1Validator:
    """Validates the incoming RepositoryContext before preprocessing begins."""

    @staticmethod
    def validate(context: RepositoryContext) -> None:
        """
        Verify the raw context is healthy.

        Args:
            context: The raw Sources Framework RepositoryContext.

        Raises:
            PreprocessingValidationError: If validation fails.
        """
        if not context.repositories:
            raise PreprocessingValidationError("RepositoryContext contains no repositories.")

        repo_names = [repo.name for repo in context.repositories]
        if len(set(repo_names)) != len(repo_names):
            raise PreprocessingValidationError(
                "RepositoryContext contains duplicate repository names."
            )

        for repo in context.repositories:
            for module in repo.modules:
                if not module.path.exists():
                    raise PreprocessingValidationError(f"Module path {module.path} does not exist.")
