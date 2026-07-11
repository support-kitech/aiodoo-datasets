"""Unit tests for the Phase 3 Discovery Framework."""

import pytest
from pathlib import Path

from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.repository import RepositoryConfiguration
from sources.domain.discovered_module import DiscoveredModule
from sources.domain.interpreted_module import InterpretedModule
from sources.core.scanner import RepositoryScanner
from sources.core.interpreter import RepositoryInterpreter
from sources.factories.module_factory import ModuleFactory
from sources.builders.repository_builder import RepositoryBuilder
from sources.index.repository_index import RepositoryIndex
from sources.exceptions import ScannerError


@pytest.fixture
def mock_repository(tmp_path: Path) -> RepositoryConfiguration:
    """Creates a mock repository structure on disk."""
    root = tmp_path / "odoo"
    root.mkdir()

    addons = root / "addons"
    addons.mkdir()

    # Create module 1
    mod1 = addons / "base"
    mod1.mkdir()
    (mod1 / "__manifest__.py").write_text(
        "{\n"
        "    'name': 'Base',\n"
        "    'version': '1.0',\n"
        "    'depends': [],\n"
        "    'installable': True,\n"
        "}\n",
        encoding="utf-8",
    )

    # Create module 2
    mod2 = addons / "web"
    mod2.mkdir()
    (mod2 / "__manifest__.py").write_text(
        "{\n"
        "    'name': 'Web Core',\n"
        "    'version': '2.0',\n"
        "    'depends': ['base'],\n"
        "    'installable': True,\n"
        "}\n",
        encoding="utf-8",
    )

    return RepositoryConfiguration(
        repository_name="framework-17.0",
        repo_type=RepositoryType.FRAMEWORK,
        version=OdooVersion.V17,
        root_path=root,
        addons_paths=(addons,),
    )


def test_repository_scanner(mock_repository: RepositoryConfiguration):
    """Test the scanner successfully discovers modules without parsing them."""
    discovered = RepositoryScanner.scan(mock_repository)

    assert len(discovered) == 2
    for d in discovered:
        assert isinstance(d, DiscoveredModule)
        assert d.manifest_path.exists()
        assert d.raw_manifest.startswith("{")
        assert d.repository_path == mock_repository.root_path


def test_repository_interpreter(mock_repository: RepositoryConfiguration):
    """Test interpreter parses valid manifests into InterpretedModule."""
    discovered = RepositoryScanner.scan(mock_repository)
    base_module = next(d for d in discovered if d.module_path.name == "base")

    interpreted = RepositoryInterpreter.interpret(base_module)
    assert isinstance(interpreted, InterpretedModule)
    assert interpreted.raw_metadata["name"] == "Base"
    assert interpreted.technical_name == "base"
    assert interpreted.version == "1.0"
    assert interpreted.depends == ()


def test_repository_interpreter_malformed(tmp_path: Path):
    """Test interpreter raises ScannerError on invalid python literals."""
    mod = DiscoveredModule(
        module_path=tmp_path / "bad",
        manifest_path=tmp_path / "bad" / "__manifest__.py",
        raw_manifest="not a dict",
        repository_path=tmp_path,
    )
    with pytest.raises(ScannerError, match="Malformed manifest"):
        RepositoryInterpreter.interpret(mod)


def test_module_factory(mock_repository: RepositoryConfiguration):
    """Test ModuleFactory creates immutable OdooModules."""
    discovered = RepositoryScanner.scan(mock_repository)
    web_module = next(d for d in discovered if d.module_path.name == "web")

    interpreted = RepositoryInterpreter.interpret(web_module)
    module = ModuleFactory.create(interpreted)

    assert module.name == "Web Core"
    assert module.technical_name == "web"
    assert module.depends == ("base",)
    assert module.installable is True
    assert module.version == "2.0"


def test_repository_builder(mock_repository: RepositoryConfiguration):
    """Test RepositoryBuilder assembles the full repository."""
    discovered = RepositoryScanner.scan(mock_repository)

    modules = []
    for d in discovered:
        interpreted = RepositoryInterpreter.interpret(d)
        modules.append(ModuleFactory.create(interpreted))

    repo = RepositoryBuilder.build(mock_repository, tuple(modules))

    assert repo.name == "framework-17.0"
    assert len(repo.modules) == 2
    assert repo.manifest.module_count == 2
    assert repo.manifest.addons_count == 1
    assert repo.manifest.fingerprint.repository_hash != ""


def test_repository_index(mock_repository: RepositoryConfiguration):
    """Test RepositoryIndex lookups."""
    discovered = RepositoryScanner.scan(mock_repository)
    modules = []
    for d in discovered:
        interpreted = RepositoryInterpreter.interpret(d)
        modules.append(ModuleFactory.create(interpreted))

    repo = RepositoryBuilder.build(mock_repository, tuple(modules))
    index = RepositoryIndex((repo,))

    # find_repository
    found_repo = index.find_repository("framework-17.0")
    assert found_repo == repo

    # find_by_version
    assert len(index.versions[OdooVersion.V17]) == 1
    assert OdooVersion.V18 not in index.versions

    # find_module
    base_mods = index.find_module("base")
    assert len(base_mods) == 1
    assert base_mods[0].technical_name == "base"
