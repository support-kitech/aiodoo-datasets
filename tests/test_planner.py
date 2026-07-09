"""Tests for the Planner Dataset Generator Pipeline."""

import json
from pathlib import Path

import pytest
from aiodoo_datasets.generators.planner.pipeline import PlannerPipeline

@pytest.fixture
def temp_workspace(tmp_path):
    """Creates a temporary workspace with a mock Odoo module."""
    # Create module
    valid_mod = tmp_path / "my_planner_test"
    valid_mod.mkdir()
    
    # Manifest
    (valid_mod / "__manifest__.py").write_text("{'name': 'Planner Test', 'depends': ['base']}")
    
    # Python Models
    py_content = \"\"\"
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
    name = fields.Char()
\"\"\"
    (valid_mod / "models.py").write_text(py_content)
    
    # XML View
    xml_content = \"\"\"
<odoo>
    <record id="view_my_model_form" model="ir.ui.view">
        <field name="name">my.model.form</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <form>
                <field name="name"/>
            </form>
        </field>
    </record>
</odoo>
\"\"\"
    (valid_mod / "views.xml").write_text(xml_content)

    # sources.yaml
    sources_yaml = tmp_path / "sources.yaml"
    sources_yaml.write_text(f\"\"\"
repositories:
  test_repo:
    "17.0":
      root: "{tmp_path}"
      addons: ["."]
\"\"\")
    
    return tmp_path, sources_yaml


def test_planner_pipeline_end_to_end(temp_workspace):
    """Test the complete generation pipeline from discovery to JSONL export."""
    tmp_path, sources_yaml = temp_workspace
    output_dir = tmp_path / "output"
    
    # Run the pipeline synchronously with 1 worker to ensure exceptions surface directly in tests
    pipeline = PlannerPipeline(sources_yaml=sources_yaml, output_dir=output_dir, workers=1)
    pipeline.run()
    
    jsonl_file = output_dir / "planner_v1_0.jsonl"
    assert jsonl_file.exists()
    
    with open(jsonl_file, "r") as f:
        lines = f.readlines()
        
    assert len(lines) >= 1
    
    # Parse the first record and validate structure
    record = json.loads(lines[0])
    
    assert "instruction" in record
    assert "input" in record
    assert "output" in record
    assert "metadata" in record
    
    # Ensure it mapped to V1 Protocol
    output = record["output"]
    assert "goal" in output
    assert "tasks" in output
    assert "execution" in output
    
    # Check tasks derived from AST/XML
    task_titles = [t["title"] for t in output["tasks"]]
    assert any("Create Model: my.model" in t for t in task_titles)
    assert any("Form View" in t for t in task_titles)
    
    # Check deduplication
    assert pipeline.writer.written_count == len(lines)
