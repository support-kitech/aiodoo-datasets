"""High-performance ETL Pipeline Orchestrator."""

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, Any, Type
import copyreg
from types import MappingProxyType
from pydantic import BaseModel


def _pickle_mappingproxy(mp: MappingProxyType) -> tuple:
    return MappingProxyType, (dict(mp),)


copyreg.pickle(MappingProxyType, _pickle_mappingproxy)


logger = logging.getLogger(__name__)


class SharedPipelineOrchestrator:
    """Generic orchestrator for AIODOO dataset generation pipelines."""

    def __init__(
        self,
        repository_context: Any,
        writer: Any,
        deduplicator: Any,
        core_validator: Any,
        checkpoint: Any,
        worker_fn: Callable[[Any], list[dict]],  # type: ignore[type-arg]
        record_class: Type[BaseModel],
        validation_method: str,
        checkpoint_strategy: str = "module",
        stats_filename: str = "statistics.json",
        manifest_filename: str = "manifest.json",
        workers: int = 4,
        resume: bool = False,
    ) -> None:
        self.repository_context = repository_context
        self.writer = writer
        self.deduplicator = deduplicator
        self.core_validator = core_validator
        self.checkpoint = checkpoint
        self.worker_fn = worker_fn
        self.record_class = record_class
        self.validation_method = validation_method
        self.checkpoint_strategy = checkpoint_strategy
        self.stats_filename = stats_filename
        self.manifest_filename = manifest_filename
        self.workers = workers
        self.resume = resume

    def run(self) -> None:
        """Execute the pipeline across all configured repositories."""
        all_modules = [m for r in self.repository_context.repositories for m in r.modules]
        logger.info("Discovered %d modules in total.", len(all_modules))

        if self.resume:
            modules = [
                m for m in all_modules if not self.checkpoint.is_module_fully_processed(m.name)
            ]
            logger.info(
                "Resuming generation. Skipping %d processed modules. %d remaining.",
                len(all_modules) - len(modules),
                len(modules),
            )
        else:
            modules = all_modules

        validator_fn = getattr(self.core_validator, self.validation_method)

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            future_to_module = {executor.submit(self.worker_fn, mod): mod for mod in modules}

            for future in as_completed(future_to_module):
                mod = future_to_module[future]
                try:
                    records_data = future.result()
                    for data in records_data:
                        payload_dict = data["output"]
                        protocol_hash = data["metadata"]["protocol_hash"]

                        if self.checkpoint_strategy == "artifact":
                            scenario_name = data["metadata"]["scenario"][0]
                            repo = data["metadata"]["repository"]
                            if self.resume and self.checkpoint.is_processed(
                                repo, mod.name, scenario_name, protocol_hash
                            ):
                                continue

                        if self.deduplicator.is_unique(protocol_hash):
                            try:
                                record = self.record_class(**data)
                                validator_fn(payload_dict)
                                self.writer.write_record(record)

                                if self.checkpoint_strategy == "artifact":
                                    self.checkpoint.save(
                                        repo,
                                        mod.name,
                                        scenario_name,
                                        protocol_hash,
                                        self.writer.written_count,
                                    )
                            except ValueError as val_exc:
                                logger.error(
                                    "Core validation rejected sample for %s: %s", mod.name, val_exc
                                )
                                self.writer.record_validation_failure()
                        else:
                            self.writer.record_duplicate()

                    if self.checkpoint_strategy == "module":
                        self.checkpoint.save(mod.name, self.writer.written_count)

                except Exception as exc:
                    logger.error("Module %s crashed unexpectedly: %s", mod.name, exc)
                    raise RuntimeError(f"Pipeline crashed on module {mod.name}") from exc

        self.writer.export_statistics(self.stats_filename)
        self.writer.export_manifest(self.manifest_filename)
        logger.info("Pipeline complete. Wrote %d unique records.", self.writer.written_count)
