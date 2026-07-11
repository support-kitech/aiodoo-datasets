"""Main orchestration pipeline for the Preprocessing Framework."""

import time
import hashlib
from datetime import datetime, timezone
from types import MappingProxyType

from preprocessing.constants.framework import PREPROCESSING_FRAMEWORK_VERSION
from preprocessing.cache.cache_key import CacheKey
from preprocessing.cache.cache_metadata import CacheMetadata
from preprocessing.cache.store import CacheStore
from preprocessing.cache.invalidator import CacheInvalidator
from preprocessing.cache.serializer import Serializer
from preprocessing.cache.deserializer import Deserializer
from preprocessing.pipeline.pipeline_context import PipelineContext
from preprocessing.pipeline.pipeline_result import PipelineResult
from preprocessing.pipeline.pipeline_statistics import PipelineStatistics
from preprocessing.validation.stage1_validator import Stage1Validator
from preprocessing.validation.stage2_validator import Stage2Validator
from preprocessing.processors.registry import ProcessorRegistry
from preprocessing.processors.pipeline import ProcessorPipeline as InnerProcessorPipeline
from preprocessing.processors.base import ProcessorContext
from preprocessing.builders.context_builder import ContextBuilder
from preprocessing.builders.repository_builder import RepositoryBuilder
from preprocessing.builders.normalized_file_builder import NormalizedFileBuilder
from preprocessing.domain.file import Language
from preprocessing.exceptions import PreprocessingError, PreprocessingValidationError


class PreprocessingPipeline:
    """
    Coordinates the full lifecycle of preprocessing.
    Stage 1 Validate -> Cache hit? -> inner processor pipeline -> Stage 2 Validate -> Serialize -> Return.
    """
    
    def __init__(self, cache_store: CacheStore, registry: ProcessorRegistry):
        self._cache_store = cache_store
        self._registry = registry
        self._inner_pipeline = InnerProcessorPipeline(self._registry)
        
    def execute(self, p_context: PipelineContext) -> PipelineResult:
        start_total = time.perf_counter()
        
        try:
            # 1. Stage 1 Validation
            t0 = time.perf_counter()
            Stage1Validator.validate(p_context.source_context)
            t_val1 = time.perf_counter() - t0
            
            # 2. Cache Validation & Fetch
            t0 = time.perf_counter()
            # Generate a deterministic hash based on repository names and versions
            context_hash = hashlib.md5(str([r.name + str(r.version) for r in p_context.source_context.repositories]).encode()).hexdigest()
            cache_key = p_context.cache_key or CacheKey(source_context_hash=context_hash)
            cached_data = self._cache_store.get(cache_key) if not p_context.options.skip_cache else None
            
            if cached_data and not p_context.options.force_reprocess:
                payload, metadata = cached_data
                invalidation = CacheInvalidator.validate(metadata)
                if invalidation.is_valid:
                    # Cache Hit
                    t1 = time.perf_counter()
                    deserialized_context = Deserializer.deserialize(payload)
                    t_deser = time.perf_counter() - t1
                    
                    stats = PipelineStatistics(
                        cache_hit=True,
                        cache_miss=False,
                        files_processed=sum(len(m.files) for r in deserialized_context.repositories for m in r.modules),
                        repositories_processed=len(deserialized_context.repositories),
                        total_duration=time.perf_counter() - start_total,
                        validation_time=t_val1,
                        cache_lookup_time=t1 - t0,
                        processing_time=0.0,
                        builder_time=0.0,
                        serialization_time=0.0,
                        deserialization_time=t_deser,
                        cache_write_time=0.0
                    )
                    return PipelineResult(
                        success=True,
                        context=deserialized_context,
                        statistics=stats
                    )
            
            t_cache_lookup = time.perf_counter() - t0
            
            # 3. Processing
            if p_context.options.validate_only:
                return PipelineResult(
                    success=True,
                    context=None,
                    statistics=PipelineStatistics(
                        validation_time=t_val1,
                        cache_lookup_time=t_cache_lookup,
                        total_duration=time.perf_counter() - start_total
                    )
                )
                
            t0 = time.perf_counter()
            preprocessed_repos = []
            files_processed = 0
            
            for source_repo in p_context.source_context.repositories:
                preprocessed_modules = []
                for source_module in source_repo.modules:
                    preprocessed_files = []
                    
                    # For phase 3 we simulate file discovery since Source module doesn't contain files.
                    # We just discover all text-like files in the module path.
                    # (In a real system, the generator would do this or it would use manifest).
                    # Here we just find all files with known extensions.
                    valid_extensions = {".py", ".xml", ".csv", ".json", ".md", ".txt"}
                    all_files = [f for f in source_module.path.rglob("*") if f.is_file() and f.suffix in valid_extensions]
                    
                    for raw_file in all_files:
                        try:
                            raw_content = raw_file.read_text(encoding="utf-8")
                        except UnicodeDecodeError:
                            continue
                            
                        language_map = {
                            ".py": Language.PYTHON,
                            ".xml": Language.XML,
                            ".json": Language.JSON,
                            ".csv": Language.CSV,
                            ".md": Language.MARKDOWN,
                            ".txt": Language.TEXT
                        }
                        language = language_map.get(raw_file.suffix, Language.UNKNOWN)
                        
                        proc_ctx = ProcessorContext(
                            file_path=raw_file,
                            normalized_path=raw_file.relative_to(source_module.path),
                            language=language,
                            raw_content=raw_content,
                            current_content=raw_content
                        )
                        
                        final_proc_ctx = self._inner_pipeline.execute(proc_ctx)
                        norm_file = NormalizedFileBuilder.build(final_proc_ctx)
                        preprocessed_files.append(norm_file)
                        files_processed += 1
                        
                    metadata = {
                        "technical_name": source_module.technical_name,
                        "version": source_module.version,
                        "depends": list(source_module.depends),
                        "license": source_module.license,
                        "installable": source_module.installable,
                        "application": source_module.application,
                        "auto_install": source_module.auto_install,
                        "path": str(source_module.path),
                        "manifest_path": str(source_module.manifest_path),
                    }
                    module = RepositoryBuilder.build_module(source_module.name, tuple(preprocessed_files), metadata)
                    preprocessed_modules.append(module)
                    
                repo = RepositoryBuilder.build(source_repo, tuple(preprocessed_modules))
                preprocessed_repos.append(repo)
                
            final_context = ContextBuilder.build(p_context.source_context, tuple(preprocessed_repos))
            t_proc = time.perf_counter() - t0
            t_builder = 0.0 # Could refine if needed, but keeping simple
            
            # 4. Stage 2 Validation
            t0 = time.perf_counter()
            Stage2Validator.validate(final_context)
            t_val2 = time.perf_counter() - t0
            
            # 5. Serialization & Persistence
            t0 = time.perf_counter()
            payload = Serializer.serialize(final_context)
            t_ser = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            if not p_context.options.skip_cache:
                import sys
                from preprocessing.constants.serialization import SERIALIZATION_FORMAT
                
                cache_meta = CacheMetadata(
                    cache_key=cache_key.value,
                    created_at_iso=datetime.now(timezone.utc).isoformat(),
                    framework_version=PREPROCESSING_FRAMEWORK_VERSION,
                    python_version=sys.version.split(" ")[0],
                    cache_schema_version="1.0",
                    serializer_version=SERIALIZATION_FORMAT,
                    repository_context_hash=context_hash,
                    preprocessed_context_hash=hashlib.sha256(payload.encode()).hexdigest(),
                    processor_registry_hash=hashlib.sha256(str(self._registry).encode()).hexdigest(),
                    statistics=MappingProxyType({"files_processed": files_processed})
                )
                self._cache_store.set(cache_key, payload, cache_meta)
            t_cache_write = time.perf_counter() - t0
            
            stats = PipelineStatistics(
                cache_hit=False,
                cache_miss=True,
                files_processed=files_processed,
                repositories_processed=len(preprocessed_repos),
                total_duration=time.perf_counter() - start_total,
                validation_time=t_val1 + t_val2,
                cache_lookup_time=t_cache_lookup,
                processing_time=t_proc,
                builder_time=t_builder,
                serialization_time=t_ser,
                deserialization_time=0.0,
                cache_write_time=t_cache_write
            )
            
            return PipelineResult(
                success=True,
                context=final_context,
                statistics=stats
            )
            
        except PreprocessingValidationError as e:
            return PipelineResult(
                success=False,
                context=None,
                statistics=PipelineStatistics(total_duration=time.perf_counter() - start_total),
                error_message=str(e)
            )
        except PreprocessingError as e:
            return PipelineResult(
                success=False,
                context=None,
                statistics=PipelineStatistics(total_duration=time.perf_counter() - start_total),
                error_message=str(e)
            )
        except Exception as e:
            return PipelineResult(
                success=False,
                context=None,
                statistics=PipelineStatistics(total_duration=time.perf_counter() - start_total),
                error_message=f"Unexpected error: {e}"
            )
