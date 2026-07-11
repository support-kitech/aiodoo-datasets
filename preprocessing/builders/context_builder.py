"""Context builder."""

from sources.domain.context import RepositoryContext
from preprocessing.domain.context import PreprocessedRepositoryContext
from preprocessing.domain.repository import PreprocessedRepository


class ContextBuilder:
    """Builds an immutable PreprocessedRepositoryContext."""

    @staticmethod
    def build(
        source_context: RepositoryContext, repositories: tuple[PreprocessedRepository, ...]
    ) -> PreprocessedRepositoryContext:
        """Constructs the context ensuring deterministic ordering of repositories."""
        sorted_repos = tuple(sorted(repositories, key=lambda r: r.name))

        return PreprocessedRepositoryContext(repositories=sorted_repos)
