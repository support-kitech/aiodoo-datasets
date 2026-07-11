import unittest
from pathlib import Path
from types import MappingProxyType
from generators.execution.validation.export_validator import ExportValidator
from generators.execution.export.export_context import ExportContext
from generators.execution.export.export_statistics import ExportStatistics
from generators.execution.protocol.protocol_result import ProtocolResult


class TestExportValidator(unittest.TestCase):
    def test_validation_failure(self) -> None:
        ctx = ExportContext(
            protocol_result=ProtocolResult(success=False),
            protocol_statistics=None,
            export_configuration=MappingProxyType({}),
            output_directory=Path("/tmp"),
            export_statistics=ExportStatistics(),
        )

        violations = ExportValidator.validate(ctx)
        self.assertTrue(len(violations) > 0)
        self.assertIn("Cannot export: Protocol mapping failed.", violations)


if __name__ == "__main__":
    unittest.main()
