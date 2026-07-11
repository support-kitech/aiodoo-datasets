"""Stage 2 Validator: Post-processing integrity validation."""

from preprocessing.domain.context import PreprocessedRepositoryContext
from preprocessing.exceptions import PreprocessingValidationError


class Stage2Validator:
    """Validates the final PreprocessedRepositoryContext to ensure integrity."""
    
    @staticmethod
    def validate(context: PreprocessedRepositoryContext) -> None:
        """
        Verify the processed context is healthy and constraints are met.
        
        Args:
            context: The fully preprocessed context graph.
            
        Raises:
            PreprocessingValidationError: If validation fails.
        """
        if not context.repositories:
            raise PreprocessingValidationError("PreprocessedRepositoryContext contains no repositories.")
            
        repo_names = [r.name for r in context.repositories]
        if repo_names != sorted(repo_names):
            raise PreprocessingValidationError("Repositories are not deterministically ordered.")
            
        for repo in context.repositories:
            module_names = [m.name for m in repo.modules]
            if module_names != sorted(module_names):
                raise PreprocessingValidationError(f"Modules in repo {repo.name} are not deterministically ordered.")
                
            for module in repo.modules:
                file_paths = [f.normalized_path for f in module.files]
                if file_paths != sorted(file_paths):
                    raise PreprocessingValidationError(f"Files in module {module.name} are not deterministically ordered.")
                    
                for file_node in module.files:
                    if len(file_node.raw_content) > 0 and len(file_node.normalized_content) == 0:
                        if file_node.raw_content.strip() != "":
                            raise PreprocessingValidationError(
                                f"File {file_node.file_path} was normalized to 0 bytes but contained non-whitespace data."
                            )
