"""CLI configuration builder."""

import argparse
from types import MappingProxyType
from generators.execution.config.generator_config import GeneratorConfig
from generators.execution.config.export_config import ExportConfig
from generators.execution.config.runtime_config import RuntimeConfig
from generators.execution.integration.pipeline_context import PipelineContext
from generators.execution.integration.pipeline_statistics import PipelineStatistics


def build_pipeline_context(args: argparse.Namespace) -> PipelineContext:
    """Build the immutable pipeline context from arguments."""

    gen_config = GeneratorConfig(custom_settings=MappingProxyType({"source_dir": args.source_dir}))

    exp_config = ExportConfig(output_directory=args.output_dir)

    rt_config = RuntimeConfig(
        debug_mode=args.debug, fail_fast=args.fail_fast, log_level="DEBUG" if args.debug else "INFO"
    )

    return PipelineContext(
        generator_config=gen_config,
        export_config=exp_config,
        runtime_config=rt_config,
        discovery_result={
            "source_dir": args.source_dir,
            "repository_context": getattr(args, "repository_context", None),
            "protocol_context": getattr(args, "protocol_context", None)
        },
        pipeline_statistics=PipelineStatistics(),
    )
