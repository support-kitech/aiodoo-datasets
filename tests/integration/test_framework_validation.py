"""End-to-end integration tests for the Planner and Coding Generators."""

import tempfile
import yaml
from pathlib import Path
import pytest

# Inject legacy planner discovery submodules because Planner has not been internally migrated yet
import sys
from generators.common.discovery import scanner, ast_parser, xml_parser, classifier
sys.modules['generators.planner.discovery.scanner'] = scanner
sys.modules['generators.planner.discovery.ast_parser'] = ast_parser
sys.modules['generators.planner.discovery.xml_parser'] = xml_parser
sys.modules['generators.planner.discovery.classifier'] = classifier

from generators.planner.pipeline import PlannerPipeline
from generators.coding.pipeline import CodingPipeline
from .utils import verify_output_files, verify_jsonl_records

@pytest.mark.integration
def test_framework_validation():
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_path = Path(temp_dir)
        
        sources_dir = tmp_path / "sources"
        repo_dir = sources_dir / "odoo_test"
        addons_dir = repo_dir / "addons"
        module_dir = addons_dir / "test_module"
        
        module_dir.mkdir(parents=True)
        
        manifest_content = """{
            "name": "Test Module",
            "version": "1.0",
            "category": "Sales",
            "depends": ["base"],
            "data": ["views/test_views.xml"],
        }"""
        (module_dir / "__manifest__.py").write_text(manifest_content)
        
        models_dir = module_dir / "models"
        models_dir.mkdir()
        models_content = """
from odoo import models, fields

class TestModel(models.Model):
    _name = 'test.model'
    name = fields.Char(required=True)
"""
        (models_dir / "test_model.py").write_text(models_content)
        
        views_dir = module_dir / "views"
        views_dir.mkdir()
        xml_content = """<odoo>
    <record id="view_test_form" model="ir.ui.view">
        <field name="name">test.form</field>
        <field name="model">test.model</field>
        <field name="arch" type="xml">
            <form><field name="name"/></form>
        </field>
    </record>
</odoo>"""
        (views_dir / "test_views.xml").write_text(xml_content)
        
        sources_yaml = tmp_path / "sources.yaml"
        sources_config = {
            "repositories": {
                "enterprise": {
                    "17.0": {
                        "root": str(repo_dir),
                        "addons": ["addons"]
                    }
                }
            }
        }
        with open(sources_yaml, "w") as f:
            yaml.dump(sources_config, f)
            
        output_dir = tmp_path / "output"
        
        # Validating Planner Generator
        planner = PlannerPipeline(sources_yaml=sources_yaml, output_dir=output_dir, workers=1, reset_checkpoint=True)
        planner.run()
        
        verify_output_files(output_dir, "planner")
        planner_records = verify_jsonl_records(output_dir, "planner")
        assert len(planner_records) > 0
        
        # Validating Coding Generator
        coding = CodingPipeline(sources_yaml=sources_yaml, output_dir=output_dir, workers=1, reset_checkpoint=True)
        coding.run()
        
        verify_output_files(output_dir, "coding")
        coding_records = verify_jsonl_records(output_dir, "coding")
        assert len(coding_records) > 0
