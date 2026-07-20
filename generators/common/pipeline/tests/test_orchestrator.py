"""Tests for ACT-102: checkpoint semantics in SharedPipelineOrchestrator.

Regression coverage for
"Fix datasets resume checkpoint semantics" (`ecosystem-v2-certification/
MASTER_ACTION_LIST.md`): a module that contributes zero written records in a
run must **not** be marked as processed, so a future ``--resume`` run retries
it instead of permanently treating "empty result" as "module done".

``ProcessPoolExecutor`` pickles ``worker_fn`` and each module across the
process boundary, so both are plain, picklable, module-level definitions —
not closures or ``Mock`` objects — even though ``writer``/``checkpoint``/
``deduplicator``/``core_validator`` stay in the parent process and can be
simple in-process fakes.
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict

from generators.common.pipeline.orchestrator import SharedPipelineOrchestrator


@dataclass(frozen=True, slots=True)
class _FakeModule:
    name: str


@dataclass(frozen=True, slots=True)
class _FakeRepo:
    modules: tuple[_FakeModule, ...]


@dataclass(frozen=True, slots=True)
class _FakeRepositoryContext:
    repositories: tuple[_FakeRepo, ...]


class _FakeRecord(BaseModel):
    model_config = ConfigDict(extra="allow")


def worker_returns_records_for_populated(module: _FakeModule) -> list[dict]:  # type: ignore[type-arg]
    """Picklable top-level worker: returns one record for "populated", none otherwise."""
    if module.name != "populated":
        return []
    return [
        {
            "output": {"goal": "g"},
            "metadata": {"protocol_hash": f"hash-{module.name}", "module": module.name},
        }
    ]


class _FakeWriter:
    def __init__(self) -> None:
        self.written_count = 0
        self.records: list[dict] = []  # type: ignore[type-arg]

    def write_record(self, record) -> None:  # type: ignore[no-untyped-def]
        self.records.append(record)
        self.written_count += 1

    def record_duplicate(self) -> None:
        pass

    def record_validation_failure(self) -> None:
        pass

    def export_statistics(self, filename: str) -> None:
        pass

    def export_manifest(self, filename: str) -> None:
        pass


class _FakeDeduplicator:
    def is_unique(self, protocol_hash: str) -> bool:
        return True


class _FakeCoreValidator:
    def validate_plan(self, payload_dict) -> None:  # type: ignore[no-untyped-def]
        return None


class _FakeCheckpoint:
    def __init__(self) -> None:
        self.saved_modules: list[str] = []

    def save(self, module_name: str, written_rows: int) -> None:
        self.saved_modules.append(module_name)

    def is_module_fully_processed(self, module_name: str) -> bool:
        return module_name in self.saved_modules


def _build_orchestrator(
    module_names: list[str], checkpoint: _FakeCheckpoint, writer: _FakeWriter
) -> SharedPipelineOrchestrator:
    context = _FakeRepositoryContext(
        repositories=(_FakeRepo(modules=tuple(_FakeModule(name=n) for n in module_names)),)
    )
    return SharedPipelineOrchestrator(
        repository_context=context,
        writer=writer,
        deduplicator=_FakeDeduplicator(),
        core_validator=_FakeCoreValidator(),
        checkpoint=checkpoint,
        worker_fn=worker_returns_records_for_populated,
        record_class=_FakeRecord,
        validation_method="validate_plan",
        checkpoint_strategy="module",
        workers=2,
    )


class TestModuleCheckpointStrategy:
    def test_module_with_zero_written_records_is_not_checkpointed(self) -> None:
        checkpoint = _FakeCheckpoint()
        writer = _FakeWriter()
        orchestrator = _build_orchestrator(["empty"], checkpoint, writer)

        orchestrator.run()

        assert checkpoint.saved_modules == []
        assert writer.written_count == 0

    def test_module_with_written_records_is_checkpointed(self) -> None:
        checkpoint = _FakeCheckpoint()
        writer = _FakeWriter()
        orchestrator = _build_orchestrator(["populated"], checkpoint, writer)

        orchestrator.run()

        assert checkpoint.saved_modules == ["populated"]
        assert writer.written_count == 1

    def test_mixed_modules_only_populated_ones_are_checkpointed(self) -> None:
        checkpoint = _FakeCheckpoint()
        writer = _FakeWriter()
        orchestrator = _build_orchestrator(["empty", "populated"], checkpoint, writer)

        orchestrator.run()

        assert checkpoint.saved_modules == ["populated"]
        assert writer.written_count == 1
