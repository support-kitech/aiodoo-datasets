import logging
import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from aiodoo_datasets.generators.context.pipeline import ContextPipeline
from aiodoo_datasets.generators.common.discovery.scanner import OdooModule, ManifestInfo

logging.basicConfig(level=logging.DEBUG)

class MockModuleScanner:
    def __init__(self, *args, **kwargs):
        self.modules = [
            OdooModule(
                name="mock_module",
                path=Path(__file__).parent, # Point to tests dir just to have a valid path
                version="17.0",
                edition="ce",
                manifest=ManifestInfo(depends=["base"])
            )
        ]
        
    def discover_modules(self):
        return self.modules
        
    def update_cache(self, mod):
        pass

class MockASTParser:
    def parse_module(self, path):
        from aiodoo_datasets.generators.common.discovery.ast_parser import ModuleKnowledgeList, PythonKnowledge, OdooModelDef
        
        k = PythonKnowledge()
        k.models["res.partner"] = OdooModelDef(name="res.partner")
        
        return ModuleKnowledgeList([k], {"models/res_partner.py": k})
        
class MockXMLParser:
    def parse_module(self, path):
        from aiodoo_datasets.generators.common.discovery.xml_parser import ModuleKnowledgeList, XMLKnowledge, OdooViewDef
        
        k = XMLKnowledge()
        k.views.append(OdooViewDef(id="view_partner_form", model="res.partner", view_type="form"))
        
        return ModuleKnowledgeList([k], {"views/res_partner_views.xml": k})

class TestEndToEnd(unittest.TestCase):

    @patch('aiodoo_datasets.generators.context.pipeline.ModuleScanner', MockModuleScanner)
    @patch('aiodoo_datasets.generators.context.pipeline.OdooASTParser', MockASTParser)
    @patch('aiodoo_datasets.generators.context.pipeline.OdooXMLParser', MockXMLParser)
    def test_end_to_end_determinism(self):
        with tempfile.TemporaryDirectory() as tempdir:
            # Run 1
            pipeline1 = ContextPipeline(config_path="fake.yaml", output_dir=tempdir, workers=1)
            pipeline1.run()
            
            output_file = Path(tempdir) / "context_v1_0.jsonl"
            self.assertTrue(output_file.exists())
            
            with open(output_file, "r") as f:
                run1_content = f.read()
                
            # Rename file for Run 2
            output_file.rename(Path(tempdir) / "context_v1_0_run1.jsonl")
            
            # Run 2
            pipeline2 = ContextPipeline(config_path="fake.yaml", output_dir=tempdir, workers=1)
            pipeline2.run()
            
            with open(output_file, "r") as f:
                run2_content = f.read()
                
            # Outputs MUST be identical
            self.assertEqual(run1_content, run2_content, "Output datasets are not byte-for-byte deterministic!")
            
            # Verify records were generated
            records = run1_content.strip().split("\n")
            self.assertTrue(len(records) > 0, "No records were generated!")

if __name__ == '__main__':
    unittest.main()
