"""Tests for the Instruction Templating Engine."""

import pytest
from pathlib import Path

from aiodoo_datasets.generators.planner.synthetics.instruction import InstructionEngine
from aiodoo_datasets.generators.planner.discovery.scanner import OdooModule, ManifestInfo
from aiodoo_datasets.generators.planner.discovery.classifier import Scenario


@pytest.fixture
def mock_templates_dir(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    (templates_dir / "test_portal.yaml").write_text(\"\"\"
"Portal Interface":
  - "Build portal for {module_name} in tech {module_tech_name} v{version}."
\"\"\")
    
    (templates_dir / "test_wizard.yaml").write_text(\"\"\"
"Create Wizard":
  - "Wizard for {module_tech_name}."
  - "Alternative Wizard for {module_tech_name}."
\"\"\")

    return templates_dir


def test_instruction_engine_loads_templates(mock_templates_dir):
    engine = InstructionEngine(templates_dir=mock_templates_dir)
    assert "Portal Interface" in engine.templates
    assert "Create Wizard" in engine.templates
    assert len(engine.templates["Create Wizard"]) == 2


def test_instruction_engine_deterministic_rendering(mock_templates_dir):
    engine = InstructionEngine(templates_dir=mock_templates_dir)
    
    mod = OdooModule(
        name="my_test_mod",
        path=Path("/tmp"),
        version="17.0",
        edition="community",
        manifest=ManifestInfo(name="My Test Mod")
    )
    
    scenario_portal = Scenario(name="Portal Interface")
    instruction = engine.generate(mod, scenario_portal)
    assert instruction == "Build portal for My Test Mod in tech my_test_mod v17.0."
    
    # Test deterministic random choice for multiple templates
    scenario_wizard = Scenario(name="Create Wizard")
    instruction1 = engine.generate(mod, scenario_wizard)
    instruction2 = engine.generate(mod, scenario_wizard)
    
    # Same module + scenario should yield identical instruction every time
    assert instruction1 == instruction2


def test_instruction_engine_fallback(mock_templates_dir):
    engine = InstructionEngine(templates_dir=mock_templates_dir)
    mod = OdooModule(
        name="my_test_mod",
        path=Path("/tmp"),
        version="17.0",
        edition="community",
        manifest=ManifestInfo(name="My Test Mod")
    )
    
    scenario_unknown = Scenario(name="Unknown Architecture")
    instruction = engine.generate(mod, scenario_unknown)
    assert "Build the My Test Mod module" in instruction
