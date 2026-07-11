"""Generic filesystem crawler for discovering modules."""

from pathlib import Path

from sources.domain.repository import RepositoryConfiguration
from sources.domain.discovered_module import DiscoveredModule
from sources.exceptions import ScannerError


class RepositoryScanner:
    """Crawls filesystems to discover modules without interpreting them."""

    @staticmethod
    def scan(config: RepositoryConfiguration) -> tuple[DiscoveredModule, ...]:
        """
        Scan a repository for Odoo modules.

        Args:
            config: The repository configuration to scan.

        Returns:
            A tuple of DiscoveredModule objects containing raw manifest strings.

        Raises:
            ScannerError: If filesystem operations fail.
        """
        discovered: list[DiscoveredModule] = []
        search_paths: list[Path] = list(config.addons_paths)

        if not search_paths:
            search_paths = [config.root_path]

        try:
            # Sort search paths for deterministic traversal
            for search_path in sorted(search_paths, key=lambda p: str(p)):
                if not search_path.exists() or not search_path.is_dir():
                    continue

                # Sort children for deterministic iteration
                for child in sorted(search_path.iterdir(), key=lambda c: str(c)):
                    if not child.is_dir():
                        continue

                    manifest_path = child / "__manifest__.py"
                    if manifest_path.exists() and manifest_path.is_file():
                        raw_content = manifest_path.read_text(encoding="utf-8")
                        discovered.append(
                            DiscoveredModule(
                                module_path=child,
                                manifest_path=manifest_path,
                                raw_manifest=raw_content,
                                repository_path=config.root_path,
                            )
                        )
        except OSError as e:
            raise ScannerError(f"Failed to scan repository '{config.repository_name}': {e}")

        # Final safety sort
        discovered.sort(key=lambda m: str(m.module_path))
        return tuple(discovered)
