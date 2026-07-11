#!/usr/bin/env python3
"""
Performance Benchmark for AIODOO Sources Framework.
Measures cold load, warm load, and cache efficiency.
"""

import time
import argparse
from pathlib import Path

from sources.core.manager import RepositoryManager
from sources.pipeline.pipeline_options import PipelineOptions


def run_benchmark(config_path: Path, cache_db: Path) -> None:
    print("=" * 50)
    print("Sources Framework v1.0.0 Performance Benchmark")
    print("=" * 50)

    # 1. Clear Cache
    print("\n[1] Clearing Cache...")
    if cache_db.exists():
        cache_db.unlink()
    print("Cache cleared.")

    manager = RepositoryManager(cache_db)

    # 2. Cold Load
    print("\n[2] Performing Cold Load (Forced File I/O)...")
    options_cold = PipelineOptions(force_rescan=True, skip_cache=False)

    start_cold = time.time()
    result_cold = manager.load(config_path, options_cold)
    end_cold = time.time()

    if not result_cold.success:
        print("Cold load failed!")
        return

    duration_cold = end_cold - start_cold
    stats_cold = result_cold.statistics

    print(f"Cold Load completed in {duration_cold:.3f}s")
    print(f"Repositories Scanned: {stats_cold.repositories_scanned}")
    print(f"Modules Discovered: {stats_cold.modules_discovered}")
    print(f"Cache Hit: {stats_cold.cache_hit}")

    # 3. Warm Load
    print("\n[3] Performing Warm Load (Cache Only)...")
    options_warm = PipelineOptions(force_rescan=False, skip_cache=False)

    start_warm = time.time()
    result_warm = manager.load(config_path, options_warm)
    end_warm = time.time()

    if not result_warm.success:
        print("Warm load failed!")
        return

    if not result_warm.statistics.cache_hit:
        print(
            f"Validation Reason: {result_warm.cache_validation.reason.value if result_warm.cache_validation else 'NONE'}"
        )
        if result_warm.warnings:
            print(f"Warnings: {result_warm.warnings}")

    duration_warm = end_warm - start_warm
    stats_warm = result_warm.statistics

    print(f"Warm Load completed in {duration_warm:.3f}s")
    print(f"Cache Hit: {stats_warm.cache_hit}")

    # 4. Results
    print("\n" + "=" * 50)
    print("Benchmark Results Summary")
    print("=" * 50)
    print(f"Repositories: {stats_cold.repositories_loaded}")
    print(f"Modules: {stats_cold.modules_loaded}")
    print(f"Cold Load Time: {duration_cold:.3f} seconds")
    print(f"Warm Load Time: {duration_warm:.3f} seconds")

    if duration_cold > 0:
        improvement = (duration_cold - duration_warm) / duration_cold * 100
        speedup = duration_cold / duration_warm if duration_warm > 0 else 0
        print(f"Cache Efficiency: {improvement:.1f}% faster ({speedup:.1f}x speedup)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sources Framework benchmarks.")
    parser.add_argument(
        "--config", type=Path, default=Path("config/sources.yaml"), help="Path to sources.yaml"
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path(".aiodoo_cache/sources.sqlite"),
        help="Path to test cache DB",
    )

    args = parser.parse_args()
    run_benchmark(args.config, args.cache)
