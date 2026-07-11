"""Tests for Provenance Metadata generation."""

import pytest
from pathlib import Path
from generators.planner.export.metadata import build_metadata
from generators.planner.discovery.scanner import OdooModule, ManifestInfo
from generators.planner.discovery.classifier import Scenario
from generators.planner.validation.schema import PlanPayload, Analysis

def test_build_metadata_provenance(tmp_path):
    # Mock module path with some fake files
    module_dir = tmp_path / "test_module"
    module_dir.mkdir()
    
    (module_dir / "__manifest__.py").touch()
    (module_dir / "models.py").touch()
    (module_dir / "views.xml").touch()
    
    mod = OdooModule(
        name="test_module",
        path=module_dir,
        version="17.0",
        edition="community",
        manifest=ManifestInfo(name="Test Mod"),
        module_hash="mod_hash",
        manifest_hash="man_hash"
    )
    
    scenario = Scenario(name="Portal Interface")
    
    payload = PlanPayload(
        goal="Test Goal",
        workspace="src/test_mod",
        analysis=Analysis(summary="sum", risks=[]),
        tasks=[],
        execution=[],
        summary="sum"
    )
    
    metadata = build_metadata(mod, scenario, payload)
    
    # Assert Provenance Fields
    assert metadata["repository"] == "odoo/community"
    assert metadata["repository_version"] == "17.0"
    assert metadata["edition"] == "community"
    assert metadata["module"] == "test_module"
    assert metadata["module_path"] == str(module_dir.absolute())
    assert metadata["manifest_path"] == str(module_dir / "__manifest__.py")
    
    # Assert File tracking
    assert "models.py" in metadata["python_files"]
    assert "views.xml" in metadata["xml_files"]
    
    # Assert hashes and versions
    assert metadata["module_hash"] == "mod_hash"
    assert metadata["manifest_hash"] == "man_hash"
    assert metadata["generator_version"] == "0.1.0"
    assert metadata["protocol_version"] == "1.0"
    assert "generation_timestamp" in metadata
