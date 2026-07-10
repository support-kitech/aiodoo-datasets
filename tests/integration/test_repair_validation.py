"""End-to-end integration tests for the Repair Generator."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

from aiodoo_datasets.generators.repair.pipeline import RepairPipeline
from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from .utils import verify_output_files

@pytest.mark.integration
def test_repair_validation():
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_path = Path(temp_dir)
        repo = tmp_path / "odoo_repo"
        repo.mkdir()
        
        # Create a mock module with deliberate anti-patterns
        module = repo / "bad_module"
        module.mkdir()
        
        # 1. Broken Python
        py_file = module / "models.py"
        py_file.write_text(
            "from odoo import models, api\n"
            "class BadModel(models.Model):\n"
            "    _name = 'bad.model'\n"
            "    @api.multi\n"
            "    def do_bad_stuff(self):\n"
            "        self.env.cr.execute('SELECT * FROM res_users')\n",
            encoding="utf-8"
        )
        
        # 2. Broken XML
        xml_file = module / "views.xml"
        xml_file.write_text(
            "<odoo>\n"
            "  <record id='view_id' model='ir.ui.view'>\n"
            "    <field name='arch' type='xml'>\n"
            "      <form>\n"
            "        <field name='name' attrs=\"{'invisible': [('name', '=', False)]}\"/>\n"
            "      </form>\n"
            "    </field>\n"
            "  </record>\n"
            "</odoo>\n",
            encoding="utf-8"
        )
        
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        mock_module = OdooModule(name="bad_module", path=module, version="17.0", edition="ce", manifest={"name": "bad_module"})
        
        dummy_yaml = tmp_path / "dummy.yaml"
        dummy_yaml.write_text("sources: []", encoding="utf-8")
        
        # Mock scanner to return our mock module
        with patch("aiodoo_datasets.generators.common.discovery.scanner.ModuleScanner.discover_modules") as mock_scan:
            mock_scan.return_value = [mock_module]
            
            pipeline = RepairPipeline(
                sources_yaml=dummy_yaml,
                output_dir=output_dir,
                workers=1
            )
            
            pipeline.run()
            
        jsonl_path = output_dir / "repair_v1_0.jsonl"
        assert jsonl_path.exists(), "JSONL output not found"
        
        with open(jsonl_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        assert len(lines) == 1, f"Expected 1 record, got {len(lines)}"
        record = json.loads(lines[0])
        
        assert "instruction" in record, "Missing instruction"
        assert "output" in record, "Missing output"
        assert "metadata" in record, "Missing metadata"
        
        payload = record["output"]
        assert "tasks" in payload, "Missing tasks in payload"
        
        tasks = payload["tasks"]
        assert len(tasks) == 3, f"Expected 3 tasks (1 api.multi, 1 cr.execute, 1 attrs), got {len(tasks)}"
        
        problems = [t["problem"]["description"] for t in tasks]
        assert any("SQL" in p for p in problems), "SQL repair missing"
        assert any("api.multi" in p for p in problems), "api.multi repair missing"
        assert any("attrs" in p for p in problems), "attrs repair missing"
        
        # Check that metadata and stats generated
        verify_output_files(output_dir, "repair")
        
        # Run second time to verify deterministic IDs
        output_dir_2 = tmp_path / "output_2"
        output_dir_2.mkdir()
        
        with patch("aiodoo_datasets.generators.common.discovery.scanner.ModuleScanner.discover_modules") as mock_scan_2:
            mock_scan_2.return_value = [mock_module]
            pipeline2 = RepairPipeline(
                sources_yaml=dummy_yaml,
                output_dir=output_dir_2,
                workers=1
            )
            pipeline2.run()
            
        jsonl_path_2 = output_dir_2 / "repair_v1_0.jsonl"
        with open(jsonl_path_2, "r", encoding="utf-8") as f:
            lines_2 = f.readlines()
            
        record_2 = json.loads(lines_2[0])
        tasks_2 = record_2["output"]["tasks"]
        
        for t1, t2 in zip(tasks, tasks_2):
            assert t1["id"] == t2["id"], f"Deterministic ID mismatch! {t1['id']} != {t2['id']}"
