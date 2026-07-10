# Execution Generator Pipeline

The pipeline processes input through strict phases. Each phase consumes ONLY the immutable result of the preceding phase.

## Flow Chart

```text
1. CLI Invocation -> `PipelineContext`
2. `ExecutionAnalyzer.analyze()` -> `AnalysisResult`
3. `BuildPipeline.execute()` -> `BuildPipelineResult`
4. `GraphBuilder.build()` -> `GraphBuildResult`
5. `Planner.plan()` -> `PlanningResult`
6. `Protocol.map_protocol()` -> `ProtocolResult`
7. `Exporter.export()` -> `ExportResult`
8. `PipelineValidator.validate()` -> Final `PipelineResult`
```

## Fault Tolerance
If a phase fails, it immediately returns a `Result` with `success=False` and appends `diagnostics`. The integration orchestrator will halt and return the failed result, bypassing subsequent phases.
