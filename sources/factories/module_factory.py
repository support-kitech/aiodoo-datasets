"""Instantiates immutable OdooModule domain objects."""

from sources.domain.module import OdooModule
from sources.domain.interpreted_module import InterpretedModule


class ModuleFactory:
    """Owns creation of immutable OdooModule objects."""

    @staticmethod
    def create(interpreted: InterpretedModule) -> OdooModule:
        """
        Create a normalized OdooModule from interpreted data.

        Args:
            interpreted: The InterpretedModule extracted by RepositoryInterpreter.

        Returns:
            An immutable OdooModule instance.
        """
        # Ensure depends is sorted deterministically
        depends = tuple(sorted(interpreted.depends))
        
        # Name defaults to technical_name if not provided in raw_metadata
        name = interpreted.raw_metadata.get("name", interpreted.technical_name)

        return OdooModule(
            name=str(name),
            technical_name=interpreted.technical_name,
            path=interpreted.module_path,
            manifest_path=interpreted.manifest_path,
            version=interpreted.version,
            depends=depends,
            license=str(interpreted.license) if interpreted.license else "LGPL-3",
            installable=interpreted.installable,
            application=interpreted.application,
            auto_install=interpreted.auto_install,
        )
