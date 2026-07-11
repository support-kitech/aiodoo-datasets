import unittest
from dataclasses import FrozenInstanceError
from generators.execution.builders.build_pipeline_context import (
    BuildPipelineContext,
)
from generators.execution.builders.builder_context import BuilderContext
from generators.execution.analysis.context import AnalysisContext
from generators.execution.analysis.knowledge.execution_knowledge import (
    ExecutionKnowledge,
)
from generators.execution.statistics.builder_statistics import BuilderStatistics
from generators.common.discovery.scanner import OdooModule
from generators.common.discovery.ast_parser import PythonKnowledge
from generators.common.discovery.xml_parser import XMLKnowledge
from generators.execution.registries.builder_registry import BuilderRegistry
from generators.execution.registries.factory_registry import FactoryRegistry
from generators.execution.builders.diagnostics.builder_diagnostics import (
    BuilderDiagnostics,
)


class TestBuildPipelineContext(unittest.TestCase):
    def test_immutability(self) -> None:
        ac = AnalysisContext(
            module=OdooModule(
                name="test", path="", version="17.0", edition="community", manifest={}
            ),
            python_knowledge=PythonKnowledge(),
            xml_knowledge=XMLKnowledge(),
        )
        ek = ExecutionKnowledge()
        bc = BuilderContext(
            generator_version="1.0",
            global_config={},
            analysis_context=ac,
            execution_knowledge=ek,
            statistics=BuilderStatistics(),
        )
        ctx = BuildPipelineContext(
            builder_context=bc,
            builder_registry=BuilderRegistry(),
            factory_registry=FactoryRegistry(),
            diagnostics=BuilderDiagnostics(),
        )

        with self.assertRaises(FrozenInstanceError):
            ctx.builder_registry = BuilderRegistry()


if __name__ == "__main__":
    unittest.main()
