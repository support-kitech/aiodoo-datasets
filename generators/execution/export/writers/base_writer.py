"""Base class for export writers."""

from abc import ABC, abstractmethod
import os
import tempfile
from pathlib import Path
from aiodoo_datasets.generators.execution.export.export_context import ExportContext

class BaseWriter(ABC):
    """
    Abstract base class for dataset writers.
    Enforces atomic file writes via temporary files.
    """

    @property
    @abstractmethod
    def writer_type(self) -> str:
        """Type of the writer."""
        pass

    @abstractmethod
    def generate_content(self, context: ExportContext) -> str:
        """Generate the content string to be written."""
        pass

    def write(self, target_path: Path, context: ExportContext) -> None:
        """
        Write content atomically to the target path.
        
        Args:
            target_path: Final destination path.
            context: Export context.
            
        Raises:
            WriterError: If writing fails.
        """
        from aiodoo_datasets.generators.execution.export.exceptions import WriterError
        
        content = self.generate_content(context)
        content_bytes = content.encode("utf-8")
        
        # Ensure parent directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Atomic write
        temp_path = None
        try:
            fd, temp_path_str = tempfile.mkstemp(
                dir=str(target_path.parent),
                prefix=f".tmp_{target_path.name}_"
            )
            temp_path = Path(temp_path_str)
            
            # Write and fsync
            with os.fdopen(fd, 'wb') as f:
                f.write(content_bytes)
                f.flush()
                os.fsync(f.fileno())
                
            # Atomic rename
            os.replace(temp_path, target_path)
            
            # Update stats
            context.export_statistics.exported_files += 1
            context.export_statistics.exported_bytes += len(content_bytes)
            context.export_statistics.writer_execution_count += 1
            
        except Exception as e:
            if temp_path and temp_path.exists():
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
            raise WriterError(f"Atomic write failed for {target_path}: {e}")
