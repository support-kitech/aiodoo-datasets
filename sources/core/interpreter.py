"""Interprets raw discovered modules into structured data."""

import ast
from types import MappingProxyType

from sources.domain.discovered_module import DiscoveredModule
from sources.domain.interpreted_module import InterpretedModule
from sources.exceptions import ScannerError


class RepositoryInterpreter:
    """Understands Odoo manifests and interprets raw discovery data."""

    @staticmethod
    def interpret(discovered: DiscoveredModule) -> InterpretedModule:
        """
        Parse the raw __manifest__.py content and extract fields.

        Args:
            discovered: The raw discovered module.

        Returns:
            An InterpretedModule containing the extracted fields.

        Raises:
            ScannerError: If the manifest cannot be parsed as a valid Python dictionary.
        """
        try:
            # Odoo manifests are Python dict literals.
            manifest_dict = ast.literal_eval(discovered.raw_manifest)
        except (SyntaxError, ValueError) as e:
            raise ScannerError(f"Malformed manifest in {discovered.manifest_path}: {e}")

        if not isinstance(manifest_dict, dict):
            raise ScannerError(f"Manifest is not a dictionary in {discovered.manifest_path}")

        # Extract dependencies
        depends_raw = manifest_dict.get("depends", [])
        if isinstance(depends_raw, list):
            depends = tuple(depends_raw)
        elif isinstance(depends_raw, tuple):
            depends = depends_raw
        else:
            depends = tuple()

        return InterpretedModule(
            technical_name=discovered.module_path.name,
            module_path=discovered.module_path,
            manifest_path=discovered.manifest_path,
            version=str(manifest_dict.get("version", "1.0")),
            depends=depends,
            license=manifest_dict.get("license", "LGPL-3"),
            installable=bool(manifest_dict.get("installable", True)),
            application=bool(manifest_dict.get("application", False)),
            auto_install=bool(manifest_dict.get("auto_install", False)),
            raw_metadata=MappingProxyType(manifest_dict),
        )
