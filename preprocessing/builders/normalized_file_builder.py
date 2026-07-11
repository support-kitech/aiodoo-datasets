"""NormalizedFile builder."""

from preprocessing.processors.base import ProcessorContext
from preprocessing.domain.file import NormalizedFile, DuplicateStatus


class NormalizedFileBuilder:
    """Builds an immutable NormalizedFile from a final ProcessorContext."""

    @staticmethod
    def build(context: ProcessorContext) -> NormalizedFile:
        dup_status_str = str(context.metadata.get("duplicate_status", "UNIQUE"))
        try:
            dup_status = DuplicateStatus(dup_status_str)
        except ValueError:
            dup_status = DuplicateStatus.UNIQUE

        return NormalizedFile(
            file_path=context.file_path,
            normalized_path=context.normalized_path,
            language=context.language,
            raw_content=context.raw_content,
            normalized_content=context.current_content,
            duplicate_status=dup_status,
            metadata=context.metadata,
            warnings=context.warnings,
            statistics=context.statistics,
        )
