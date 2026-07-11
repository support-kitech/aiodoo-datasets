"""Central orchestrator for the Sources Framework."""

import time
import hashlib
from pathlib import Path
from typing import Optional, Type

from sources.constants.framework import SOURCES_FRAMEWORK_VERSION
from sources.constants.cache import CACHE_SCHEMA_VERSION
from sources.core.loader import RepositoryLoader
from sources.core.scanner import RepositoryScanner
from sources.core.interpreter import RepositoryInterpreter
from sources.factories.module_factory import ModuleFactory
from sources.builders.repository_builder import RepositoryBuilder
from sources.index.repository_index import RepositoryIndex

from sources.domain.repository import ConfigurationSet
from sources.domain.context import RepositoryContext

from sources.cache.cache_key import CacheKey
from sources.cache.cache_metadata import CacheMetadata
from sources.cache.store import CacheStore
from sources.cache.invalidator import CacheInvalidator

from sources.pipeline.pipeline_options import PipelineOptions
from sources.pipeline.pipeline_result import PipelineResult
from sources.pipeline.pipeline_statistics import PipelineStatistics
from sources.exceptions import SourcesError


class SourcesPipeline:
    """Orchestrates configuration, discovery, interpretation, and caching."""

    def __init__(
        self,
        cache_db_path: Path,
        loader_cls: Type[RepositoryLoader] = RepositoryLoader,
        scanner_cls: Type[RepositoryScanner] = RepositoryScanner,
        interpreter_cls: Type[RepositoryInterpreter] = RepositoryInterpreter,
        cache_store_cls: Type[CacheStore] = CacheStore,
    ):
        self._loader_cls = loader_cls
        self._scanner_cls = scanner_cls
        self._interpreter_cls = interpreter_cls
        self._cache_store = cache_store_cls(cache_db_path)

    def _generate_configuration_hash(self, config_set: ConfigurationSet) -> str:
        """Deterministically hash the entire configuration set."""
        config_reprs = []
        for config in config_set.configurations:
            addons_str = ",".join(str(p.resolve()) for p in sorted(config.addons_paths))
            config_repr = (
                f"{config.repository_name}:{config.repo_type.value}:"
                f"{config.version.value}:{str(config.root_path.resolve())}:"
                f"{addons_str}"
            )
            config_reprs.append(config_repr)
            
        combined_input = "|".join(sorted(config_reprs))
        return hashlib.sha256(combined_input.encode("utf-8")).hexdigest()

    def _build_context_from_filesystem(self, config_set: ConfigurationSet) -> RepositoryContext:
        """Scan and build the complete repository context from scratch."""
        built_repositories = []
        
        for config in config_set.configurations:
            # 1. Scan filesystem
            discovered_modules = self._scanner_cls.scan(config)
            
            # 2. Interpret manifests
            interpreted_modules = []
            for discovered in discovered_modules:
                interpreted = self._interpreter_cls.interpret(discovered)
                interpreted_modules.append(interpreted)
                
            # 3. Create domain objects
            odoo_modules = []
            for interpreted in interpreted_modules:
                odoo_module = ModuleFactory.create(interpreted)
                odoo_modules.append(odoo_module)
                
            # 4. Assemble Repository
            repo = RepositoryBuilder.build(config, tuple(odoo_modules))
            built_repositories.append(repo)
            
        # 5. Build Global Index
        repo_tuple = tuple(built_repositories)
        index = RepositoryIndex(repo_tuple)
        
        return RepositoryContext(
            repositories=repo_tuple,
            repository_index=index.repositories,
        )

    def _compute_repository_hash(self, context: RepositoryContext) -> str:
        """Aggregate repository hashes into a single context hash."""
        repo_hashes = [repo.manifest.fingerprint.repository_hash for repo in context.repositories]
        combined = "|".join(sorted(repo_hashes))
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def execute(self, config_path: Path, options: PipelineOptions) -> PipelineResult:
        """
        Execute the full framework pipeline deterministically.

        Args:
            config_path: Path to the root YAML configuration.
            options: Pipeline execution options.

        Returns:
            An immutable PipelineResult representing the execution outcome.
        """
        t0 = time.time()
        warnings: list[str] = []
        errors: list[str] = []
        
        stats = {
            "repositories_loaded": 0,
            "repositories_scanned": 0,
            "modules_discovered": 0,
            "modules_loaded": 0,
            "cache_hit": False,
            "cache_miss": False,
            "scan_duration": 0.0,
            "cache_duration": 0.0,
        }

        try:
            # Stage 1: Load Configuration
            config_set = self._loader_cls.load_sources(config_path)
            stats["repositories_loaded"] = len(config_set.configurations)
            
            config_hash = self._generate_configuration_hash(config_set)
            
            # Stage 2: Cache Check
            cache_key = CacheKey(
                repository_name="all",
                configuration_hash=config_hash,
                repository_hash="", # Not known before hit
                framework_version=SOURCES_FRAMEWORK_VERSION,
                python_version=CacheInvalidator.get_python_version(),
                cache_schema_version=CACHE_SCHEMA_VERSION,
            )
            
            context: Optional[RepositoryContext] = None
            cache_val = None

            t_cache_start = time.time()
            if not options.skip_cache and not options.force_rescan:
                try:
                    cached_context, metadata = self._cache_store.load()
                    
                    # Update key to include the expected repository hash from metadata to validate fully
                    cache_key = CacheKey(
                        repository_name=cache_key.repository_name,
                        configuration_hash=cache_key.configuration_hash,
                        repository_hash=metadata.repository_hash,
                        framework_version=cache_key.framework_version,
                        python_version=cache_key.python_version,
                        cache_schema_version=cache_key.cache_schema_version,
                    )
                    
                    cache_val = CacheInvalidator.validate(cache_key, metadata)
                    
                    if cache_val.is_valid:
                        context = cached_context
                        stats["cache_hit"] = True
                        
                        # Populate remaining stats
                        stats["repositories_scanned"] = metadata.repository_count
                        stats["modules_discovered"] = metadata.module_count
                        stats["modules_loaded"] = metadata.module_count
                    else:
                        stats["cache_miss"] = True
                        
                except SourcesError as e:
                    stats["cache_miss"] = True
                    warnings.append(f"Cache miss or load failure: {e}")
            else:
                stats["cache_miss"] = True

            stats["cache_duration"] = time.time() - t_cache_start

            # Stage 3: Filesystem Discovery (if cache miss)
            t_scan_start = time.time()
            if context is None:
                context = self._build_context_from_filesystem(config_set)
                
                # Update stats
                stats["repositories_scanned"] = len(context.repositories)
                total_modules = sum(len(repo.modules) for repo in context.repositories)
                stats["modules_discovered"] = total_modules
                stats["modules_loaded"] = total_modules
                
                # Stage 4: Persist Cache
                if not options.skip_cache:
                    repo_hash = self._compute_repository_hash(context)
                    new_metadata = CacheMetadata(
                        sources_framework_version=SOURCES_FRAMEWORK_VERSION,
                        cache_schema_version=CACHE_SCHEMA_VERSION,
                        python_version=CacheInvalidator.get_python_version(),
                        repository_count=stats["repositories_scanned"],
                        module_count=total_modules,
                        configuration_hash=config_hash,
                        repository_hash=repo_hash,
                        creation_time=time.time(),
                        last_validation=time.time(),
                    )
                    try:
                        self._cache_store.save(context, new_metadata)
                    except SourcesError as e:
                        warnings.append(f"Failed to save cache: {e}")

            stats["scan_duration"] = time.time() - t_scan_start
            
            pipeline_stats = PipelineStatistics(
                repositories_loaded=stats["repositories_loaded"],
                repositories_scanned=stats["repositories_scanned"],
                modules_discovered=stats["modules_discovered"],
                modules_loaded=stats["modules_loaded"],
                cache_hit=stats["cache_hit"],
                cache_miss=stats["cache_miss"],
                scan_duration=stats["scan_duration"],
                cache_duration=stats["cache_duration"],
                total_duration=time.time() - t0,
                warnings=len(warnings),
                errors=len(errors),
            )

            return PipelineResult(
                success=True,
                context=context,
                cache_validation=cache_val,
                statistics=pipeline_stats,
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        except SourcesError as e:
            errors.append(str(e))
            
            pipeline_stats = PipelineStatistics(
                total_duration=time.time() - t0,
                warnings=len(warnings),
                errors=len(errors),
            )
            
            return PipelineResult(
                success=False,
                context=None,
                cache_validation=None,
                statistics=pipeline_stats,
                warnings=tuple(warnings),
                errors=tuple(errors),
            )
