"""Discovers Odoo modules, parses manifests, and calculates incremental cache hashes."""

import ast
import hashlib
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ManifestInfo:
    """Strongly typed model for Odoo module manifests."""

    name: str = ""
    technical_name: str = ""
    version: str = "1.0"
    category: str = "Uncategorized"
    summary: str = ""
    description: str = ""
    author: str = ""
    website: str = ""
    depends: list[str] = field(default_factory=list)
    data: list[str] = field(default_factory=list)
    demo: list[str] = field(default_factory=list)
    assets: dict[str, list[str]] = field(default_factory=dict)
    installable: bool = True
    application: bool = False
    auto_install: bool | list[str] = False
    license: str = "LGPL-3"


@dataclass(slots=True)
class OdooModule:
    """Represents a discovered Odoo module with incremental hashing."""

    name: str
    path: Path
    version: str
    edition: str
    manifest: ManifestInfo
    module_hash: str = ""
    manifest_hash: str = ""
    file_count: int = 0
    last_modified: float = 0.0


class ModuleScanner:
    """Scans directories for Odoo modules, supporting local caching and incremental checks."""

    def __init__(self, config_path: Path, cache_dir: Path | None = None) -> None:
        self.config_path = config_path
        self.cache_dir = cache_dir or Path(".aiodoo_cache/discovery")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = self.cache_dir / "module_hashes.json"
        self._cache = self._load_cache()

    def discover_modules(self) -> list[OdooModule]:
        """Read configuration and discover all valid Odoo modules."""
        modules = []
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except Exception as exc:
            logger.error("Failed to load sources configuration from %s: %s", self.config_path, exc)
            return []

        repositories = config.get("repositories", {})
        for edition, versions in repositories.items():
            for version, data in versions.items():
                root_path_str = data.get("root")
                addons_paths = data.get("addons", [])

                if not root_path_str:
                    logger.warning("Missing root path for %s %s. Skipping.", edition, version)
                    continue

                root_path = Path(root_path_str)
                if not root_path.exists():
                    logger.warning("Configured path %s does not exist. Skipping.", root_path)
                    continue

                if not addons_paths:
                    modules.extend(self._scan_directory(root_path, edition, version))
                else:
                    for addon_rel_path in addons_paths:
                        addon_dir = root_path / addon_rel_path
                        if addon_dir.exists():
                            modules.extend(self._scan_directory(addon_dir, edition, version))
                        else:
                            logger.warning("Addon path %s does not exist. Skipping.", addon_dir)

        self._save_cache()
        return modules

    def is_cached(self, module: OdooModule) -> bool:
        """Check if the module's hash matches the local cache."""
        return self._cache.get(str(module.path)) == module.module_hash

    def update_cache(self, module: OdooModule) -> None:
        """Update the local cache with the module's hash after successful parsing."""
        self._cache[str(module.path)] = module.module_hash

    def _load_cache(self) -> dict[str, str]:
        if self._cache_file.exists():
            try:
                with open(self._cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)  # type: ignore[no-any-return]
            except Exception as exc:
                logger.warning("Cache file corrupted, starting fresh: %s", exc)
        return {}

    def _save_cache(self) -> None:
        try:
            with open(self._cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f)
        except Exception as exc:
            logger.error("Failed to write discovery cache: %s", exc)

    def _scan_directory(self, target_dir: Path, edition: str, version: str) -> list[OdooModule]:
        modules = []
        for child in target_dir.iterdir():
            if not child.is_dir():
                continue

            manifest_path = child / "__manifest__.py"
            if not manifest_path.exists():
                manifest_path = child / "__openerp__.py"

            if manifest_path.exists():
                manifest_data = self._read_manifest(manifest_path)
                if manifest_data is not None:
                    manifest_info = self._build_manifest_info(child.name, manifest_data)
                    mod = OdooModule(
                        name=child.name,
                        path=child.resolve(),
                        version=version,
                        edition=edition,
                        manifest=manifest_info,
                    )
                    self._compute_module_hashes(mod)
                    modules.append(mod)
        return modules

    def _build_manifest_info(self, technical_name: str, data: dict[str, Any]) -> ManifestInfo:
        return ManifestInfo(
            name=data.get("name", technical_name),
            technical_name=technical_name,
            version=data.get("version", "1.0"),
            category=data.get("category", "Uncategorized"),
            summary=data.get("summary", ""),
            description=data.get("description", ""),
            author=data.get("author", ""),
            website=data.get("website", ""),
            depends=data.get("depends", []),
            data=data.get("data", []),
            demo=data.get("demo", []),
            assets=data.get("assets", {}),
            installable=data.get("installable", True),
            application=data.get("application", False),
            auto_install=data.get("auto_install", False),
            license=data.get("license", "LGPL-3"),
        )

    def _read_manifest(self, manifest_path: Path) -> dict[str, Any] | None:
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()
            data = ast.literal_eval(content)
            if isinstance(data, dict):
                return data
            logger.warning("Manifest %s does not contain a Python dictionary.", manifest_path)
        except Exception as exc:
            logger.error("Failed to parse manifest %s: %s", manifest_path, exc)
        return None

    def _compute_module_hashes(self, module: OdooModule) -> None:
        """Compute structural hash, file count, and latest modification time."""
        hasher = hashlib.sha256()
        file_count = 0
        latest_mod = 0.0

        manifest_path = module.path / "__manifest__.py"
        if not manifest_path.exists():
            manifest_path = module.path / "__openerp__.py"

        if manifest_path.exists():
            with open(manifest_path, "rb") as f:
                content = f.read()
                module.manifest_hash = hashlib.sha256(content).hexdigest()
                hasher.update(content)
                stat = manifest_path.stat()
                if stat.st_mtime > latest_mod:
                    latest_mod = stat.st_mtime
                file_count += 1

        # Hash important files only (Python, XML, CSV) to avoid cache busting on unrelated changes
        for file_path in module.path.rglob("*"):
            if file_path.is_file() and file_path.suffix in (".py", ".xml", ".csv"):
                if file_path == manifest_path:
                    continue
                try:
                    with open(file_path, "rb") as f:
                        hasher.update(f.read())
                    stat = file_path.stat()
                    if stat.st_mtime > latest_mod:
                        latest_mod = stat.st_mtime
                    file_count += 1
                except Exception:
                    continue

        module.module_hash = hasher.hexdigest()
        module.file_count = file_count
        module.last_modified = latest_mod


class ContextModuleScanner:
    """
    Adapter that implements the discovery interface of ModuleScanner
    but retrieves modules directly from the centralized PreprocessedRepositoryContext,
    bypassing the filesystem.
    """

    def __init__(self, context: Any) -> None:
        """Initialize with an already loaded PreprocessedRepositoryContext."""
        self.repository_context = context

    def discover_modules(self) -> list[OdooModule]:
        """Convert domain OdooModules to discovery OdooModules."""
        modules = []
        for repo in self.repository_context.repositories:
            for domain_mod in repo.modules:
                manifest_info = ManifestInfo(
                    name=domain_mod.name,
                    technical_name=domain_mod.technical_name,
                    version=domain_mod.version,
                    depends=list(domain_mod.depends),
                    license=domain_mod.license,
                    installable=domain_mod.installable,
                    application=domain_mod.application,
                    auto_install=domain_mod.auto_install,
                    # We inject dummy values for unused UI fields since AIODOO doesn't care
                    category="Uncategorized",
                    summary="",
                    description="",
                    author="",
                    website="",
                    data=[],
                    demo=[],
                    assets={},
                )
                
                mod = OdooModule(
                    name=domain_mod.name,
                    path=domain_mod.path,
                    version=repo.version.value,
                    edition=repo.repository_type.value,
                    manifest=manifest_info,
                    module_hash="",  # Cache hashing is now handled globally
                    manifest_hash="",
                    file_count=0,
                    last_modified=0.0,
                )
                modules.append(mod)
        return modules

    def is_cached(self, module: OdooModule) -> bool:
        """Caching is now transparently handled by RepositoryManager."""
        return False

    def update_cache(self, module: OdooModule) -> None:
        """No-op. Global cache handles this."""
        pass
