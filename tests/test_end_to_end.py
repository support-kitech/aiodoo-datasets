"""End-to-End Production Integration Test for the AIODOO Planner Generator."""

import json
from pathlib import Path
import yaml
import pytest

from generators.planner.pipeline import PlannerPipeline
from generators.planner.validation.schema import PlannerDatasetRecord

def test_end_to_end_planner_pipeline(tmp_path):
    """
    Tests the complete dataset generator workflow:
    Discovery -> Classification -> Instruction -> Task -> Protocol -> JSONL -> Validation
    """
    # 1. Setup mock Odoo module environment
    sources_dir = tmp_path / "sources"
    repo_dir = sources_dir / "odoo_test"
    addons_dir = repo_dir / "addons"
    module_dir = addons_dir / "test_sale_module"
    
    module_dir.mkdir(parents=True)
    
    # Write __manifest__.py
    manifest_content = """{
        "name": "Test Sale Module",
        "version": "1.0",
        "category": "Sales",
        "depends": ["base", "sale"],
        "data": ["views/sale_views.xml"],
    }"""
    (module_dir / "__manifest__.py").write_text(manifest_content)
    
    # Write Python model
    models_dir = module_dir / "models"
    models_dir.mkdir()
    models_content = """
from odoo import models, fields

class TestSaleOrder(models.Model):
    _name = 'test.sale.order'
    _description = 'Test Sale Order'

    name = fields.Char(string='Order Reference', required=True)
    amount = fields.Float(string='Total Amount')
"""
    (models_dir / "sale_order.py").write_text(models_content)
    
    # Write XML view
    views_dir = module_dir / "views"
    views_dir.mkdir()
    xml_content = """<odoo>
    <record id="view_test_sale_order_form" model="ir.ui.view">
        <field name="name">test.sale.order.form</field>
        <field name="model">test.sale.order</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="amount"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>"""
    (views_dir / "sale_views.xml").write_text(xml_content)
    
    # 2. Setup Sources YAML
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
    
    # 3. Execute the pipeline End-to-End
    pipeline = PlannerPipeline(
        sources_yaml=sources_yaml,
        output_dir=output_dir,
        workers=1,
        reset_checkpoint=True
    )
    
    # This invokes Scanner -> Parser -> Classifier -> Instruction -> Protocol -> Validation -> Writer
    pipeline.run()
    
    # 4. Assertions
    jsonl_file = output_dir / "planner_v1_0.jsonl"
    manifest_file = output_dir / "planner_manifest.json"
    stats_file = output_dir / "planner_statistics.json"
    
    assert jsonl_file.exists(), "JSONL dataset was not created."
    assert manifest_file.exists(), "Manifest was not created."
    assert stats_file.exists(), "Statistics were not created."
    
    # 5. Reload JSONL and Validate
    records = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
                
    assert len(records) > 0, "No records were generated from the mock module."
    
    for record_dict in records:
        # Pydantic Strict Validation
        try:
            record = PlannerDatasetRecord(**record_dict)
        except Exception as e:
            pytest.fail(f"Generated JSONL failed Pydantic validation: {e}")
            
        # Verify metadata
        assert record.metadata["module"] == "test_sale_module"
        assert record.metadata["odoo_version"] == "17.0"
        assert record.metadata["edition"] == "enterprise"
        assert "generation_timestamp" in record.metadata
        
        # Verify Protocol structure
        assert hasattr(record.output, "goal")
        assert len(record.output.tasks) > 0
        assert len(record.output.execution) > 0
        
        # Ensure dependencies form a DAG (topological)
        task_ids = set()
        for task in record.output.tasks:
            for dep in task.dependencies:
                assert dep in task_ids, f"Task {task.id} depends on {dep} which hasn't been defined yet."
            task_ids.add(task.id)
            
    # Verify Manifest
    with open(manifest_file, "r") as f:
        manifest = json.load(f)
        
    assert manifest["repository_counts"] == 1
    assert manifest["row_count"] == len(records)
    assert manifest["checksum_sha256"] != ""
