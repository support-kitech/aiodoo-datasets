"""Deserializes JSON strings into immutable Domain models."""

import json
from pathlib import Path
from typing import Any

from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.repository import RepositoryConfiguration, Repository
from sources.domain.module import OdooModule
from sources.domain.manifest import RepositoryManifest, RepositoryFingerprint


class RepositoryDeserializer:
    """Handles parsing of JSON strings back into immutable domain models."""

    @staticmethod
    def deserialize_repository(json_str: str) -> Repository:
        """
        Reconstruct the immutable Repository from JSON dict.
        
        Args:
            json_str: The serialized JSON string.
            
        Returns:
            An immutable Repository instance.
        """
        data: dict[str, Any] = json.loads(json_str)
        
        # 1. Configuration
        conf_data = data["configuration"]
        config = RepositoryConfiguration(
            repository_name=conf_data["repository_name"],
            repo_type=RepositoryType(conf_data["repo_type"]),
            version=OdooVersion(conf_data["version"]),
            root_path=Path(conf_data["root_path"]),
            addons_paths=tuple(Path(p) for p in conf_data["addons_paths"]),
        )

        # 2. Modules
        modules = []
        for mod_data in data["modules"]:
            mod = OdooModule(
                name=mod_data["name"],
                technical_name=mod_data["technical_name"],
                path=Path(mod_data["path"]),
                manifest_path=Path(mod_data["manifest_path"]),
                version=mod_data["version"],
                depends=tuple(mod_data["depends"]),
                license=mod_data["license"],
                installable=mod_data["installable"],
                application=mod_data["application"],
                auto_install=mod_data["auto_install"],
            )
            modules.append(mod)

        # 3. Manifest
        man_data = data["manifest"]
        fing_data = man_data["fingerprint"]
        fingerprint = RepositoryFingerprint(
            configuration_hash=fing_data["configuration_hash"],
            manifest_hash=fing_data["manifest_hash"],
            repository_hash=fing_data["repository_hash"],
        )
        manifest = RepositoryManifest(
            repository_name=man_data["repository_name"],
            repository_type=RepositoryType(man_data["repository_type"]),
            repository_version=man_data["repository_version"],
            module_count=man_data["module_count"],
            addons_count=man_data["addons_count"],
            fingerprint=fingerprint,
        )

        return Repository(
            name=data["name"],
            configuration=config,
            modules=tuple(modules),
            manifest=manifest,
        )
