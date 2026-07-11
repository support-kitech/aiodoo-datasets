import logging
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from generators.context.pipeline import ContextPipeline
from preprocessing.domain.repository import PreprocessedModule

logging.basicConfig(level=logging.DEBUG)


class MockASTParser:
    def parse_module(self, path):
        from generators.common.discovery.ast_parser import (
            ModuleKnowledgeList,
            PythonKnowledge,
            OdooModelDef,
        )

        k = PythonKnowledge()
        k.models["res.partner"] = OdooModelDef(name="res.partner")

        return ModuleKnowledgeList([k], {"models/res_partner.py": k})


class MockXMLParser:
    def parse_module(self, path):
        from generators.common.discovery.xml_parser import (
            ModuleKnowledgeList,
            XMLKnowledge,
            OdooViewDef,
        )

        k = XMLKnowledge()
        k.views.append(OdooViewDef(id="view_partner_form", model="res.partner", view_type="form"))

        return ModuleKnowledgeList([k], {"views/res_partner_views.xml": k})


class TestEndToEnd(unittest.TestCase):
    @patch(
        "generators.context.pipeline.ProcessPoolExecutor",
        new_callable=lambda: __import__("concurrent.futures").futures.ThreadPoolExecutor,
    )
    @patch("generators.context.pipeline.OdooASTParser", MockASTParser)
    @patch("generators.context.pipeline.OdooXMLParser", MockXMLParser)
    def test_end_to_end_determinism(self, mock_process) -> None:
        with tempfile.TemporaryDirectory() as tempdir:

            class DummyId:
                hash_value = "mock_hash"

            class DummyDataset:
                identifier = DummyId()

            class DummyProtocolContext:
                dataset = DummyDataset()

            mock_protocol_context = DummyProtocolContext()

            mock_repo_context = MagicMock()
            mock_repo = MagicMock()
            mock_repo.modules = [
                PreprocessedModule(
                    name="mock_module",
                    files=tuple(),
                    metadata={"path": str(Path(__file__).parent), "depends": ["base"]},
                )
            ]
            mock_repo_context.repositories = [mock_repo]

            # Run 1
            pipeline1 = ContextPipeline(
                repository_context=mock_repo_context,
                protocol_context=mock_protocol_context,
                output_dir=tempdir,
                workers=1,
            )
            pipeline1.run()

            output_file = Path(tempdir) / "context_v1_0.jsonl"
            self.assertTrue(output_file.exists())

            with open(output_file, "r") as f:
                run1_content = f.read()

            # Rename file for Run 2
            output_file.rename(Path(tempdir) / "context_v1_0_run1.jsonl")

            # Run 2
            pipeline2 = ContextPipeline(
                repository_context=mock_repo_context,
                protocol_context=mock_protocol_context,
                output_dir=tempdir,
                workers=1,
            )
            pipeline2.run()

            with open(output_file, "r") as f:
                run2_content = f.read()

            # Outputs MUST be identical
            self.assertEqual(
                run1_content, run2_content, "Output datasets are not byte-for-byte deterministic!"
            )

            # Verify records were generated
            records = run1_content.strip().split("\n")
            self.assertTrue(len(records) > 0, "No records were generated!")


if __name__ == "__main__":
    unittest.main()
