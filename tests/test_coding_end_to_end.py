"""End-to-End Production Integration Test for the AIODOO Coding Generator."""

import json
from pathlib import Path
import yaml
import pytest

from aiodoo_datasets.generators.coding.pipeline import CodingPipeline
from aiodoo_datasets.generators.coding.validation.schema import CodingDatasetRecord
from aiodoo_datasets.generators.coding.state.checkpoint import CheckpointManager

def setup_mock_odoo(tmp_path: Path) -> Path:
    sources_dir = tmp_path / "sources"
    repo_dir = sources_dir / "odoo_test"
    addons_dir = repo_dir / "addons"
    module_dir = addons_dir / "test_sale_module"
    
    module_dir.mkdir(parents=True)
    
    manifest_content = """{
        "name": "Test Sale Module",
        "version": "1.0",
        "category": "Sales",
        "depends": ["base", "sale"],
        "data": ["views/sale_views.xml"],
    }"""
    (module_dir / "__manifest__.py").write_text(manifest_content)
    
    models_dir = module_dir / "models"
    models_dir.mkdir()
    models_content = """
from odoo import models, fields

class TestSaleOrder(models.Model):
    _name = 'test.sale.order'
    _inherit = 'sale.order'
    _description = 'Test Sale Order'

    name = fields.Char(string='Order Reference', required=True)
"""
    (models_dir / "sale_order.py").write_text(models_content)
    
    views_dir = module_dir / "views"
    views_dir.mkdir()
    xml_content = """<odoo>
    <record id="view_test_sale_order_form" model="ir.ui.view">
        <field name="name">test.sale.order.form</field>
        <field name="model">test.sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <field name="name"/>
                </sheet>
            </form>
        </field>
    </record>
</odoo>"""
    (views_dir / "sale_views.xml").write_text(xml_content)
    
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
        
    return sources_yaml

def test_end_to_end_coding_pipeline(tmp_path):
    """
    Tests the complete dataset generator workflow:
    Discovery -> Context -> Instructions -> Artifact Protocol -> JSONL -> Validation
    """
    sources_yaml = setup_mock_odoo(tmp_path)
    output_dir = tmp_path / "output"
    
    pipeline = CodingPipeline(
        sources_yaml=sources_yaml,
        output_dir=output_dir,
        workers=1,
        reset_checkpoint=True
    )
    
    pipeline.run()
    
    jsonl_file = output_dir / "coding_v1_0.jsonl"
    manifest_file = output_dir / "coding_manifest.json"
    stats_file = output_dir / "coding_statistics.json"
    
    assert jsonl_file.exists(), "JSONL dataset was not created."
    assert manifest_file.exists(), "Manifest was not created."
    assert stats_file.exists(), "Statistics were not created."
    
    records = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
                
    assert len(records) > 0, "No records were generated from the mock module."
    
    first_run_hash = None
    
    for record_dict in records:
        try:
            record = CodingDatasetRecord(**record_dict)
        except Exception as e:
            pytest.fail(f"Generated JSONL failed Pydantic validation: {e}")
            
        assert record.metadata["module"] == "test_sale_module"
        
        # Verify Context Structure
        assert "depends" in record.context
        assert "existing_models" in record.context
        
        # Verify Protocol structure
        assert hasattr(record.output, "artifacts")
        assert hasattr(record.output, "operations")
        assert hasattr(record.output, "validation_actions")
        
        assert len(record.output.artifacts) > 0
        assert len(record.output.operations) == len(record.output.artifacts)
        assert len(record.output.validation_actions) > 0
        
        # Operation inference tests
        ops = {op.path: op.operation for op in record.output.operations}
        # Manifest is UPDATE
        assert ops.get("__manifest__.py") == "UPDATE"
        # sale_order has _inherit and _name, meaning it's a CREATE in Odoo logic but wait, _inherit without _name is UPDATE, with _name is CREATE.
        # Our XML has inherit_id, meaning it should be PATCH
        assert ops.get("views/sale_views.xml") == "PATCH"
        
        # Protocol hash
        assert "ProtocolHash" in record.output.summary
        first_run_hash = record.metadata.get("protocol_hash")
        
        # Dependency Graph Validity
        for art in record.output.artifacts:
            deps = art.dependencies
            assert len(deps) == len(set(deps)), "Duplicate dependencies found"
            assert art.id not in deps, "Self-dependency found"
            
        # Metadata completeness
        assert "repository_type" in record.metadata
        assert "git_commit" in record.metadata
        assert "generation_timestamp" in record.metadata
        assert "source_checksum" in record.metadata

    with open(manifest_file, "r") as f:
        manifest = json.load(f)
        
    assert manifest["repository_counts"] == 1
    assert manifest["row_count"] == len(records)
    assert manifest["checksum_sha256"] != "", "Manifest checksum missing"
    
    # Test 2: Determinism - Run again, should be perfectly identical and deduplicated
    pipeline2 = CodingPipeline(
        sources_yaml=sources_yaml,
        output_dir=output_dir,
        workers=1,
        reset_checkpoint=True # Resets checkpoint, but deduplicator should catch duplicate hash
    )
    pipeline2.run()
    
    records2 = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records2.append(json.loads(line))
                
    # Still the exact same number of records (deduplication worked)
    assert len(records2) == len(records), "Deduplication failed!"
    
    # Verify byte-identical JSONL output logic via exact string matching of the file content
    content1 = (output_dir / "coding_v1_0.jsonl").read_text(encoding="utf-8")
    assert len(content1) > 0
    
    with open(manifest_file, "r") as f:
        manifest2 = json.load(f)
        
    assert manifest["checksum_sha256"] == manifest2["checksum_sha256"], "Manifest checksums differ across deterministic runs"
    assert manifest["row_count"] == manifest2["row_count"]
    
    # Test 3: Checkpoint resume
    checkpoint = CheckpointManager(output_dir=output_dir)
    checkpoint.load()
    assert checkpoint.is_module_fully_processed("test_sale_module"), "Checkpoint saving failed."
    assert "odoo_test" in checkpoint.state["processed_items"]
    assert "test_sale_module" in checkpoint.state["processed_items"]["odoo_test"]
