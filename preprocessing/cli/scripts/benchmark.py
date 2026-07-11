"""CLI benchmark script."""

import time
from preprocessing.core.manager import PreprocessingManager
from preprocessing.pipeline.pipeline_options import PipelineOptions
from sources.core.manager import RepositoryManager

def run_benchmark():
    print("--- Preprocessing Benchmark ---")
    
    from pathlib import Path
    repo_manager = RepositoryManager(Path("config/sources.sqlite"))
    from sources.pipeline.pipeline_options import PipelineOptions as SourcesOptions
    result = repo_manager.load(Path("config/sources.yaml"), SourcesOptions())
    if not result.success or not result.context:
        print("Failed to load sources context.")
        return
    source_context = result.context
    
    manager = PreprocessingManager()
    manager.clear_cache()
    
    # Cold Run
    print("Running Cold Preprocessing...")
    t0 = time.perf_counter()
    res_cold = manager.normalize(source_context, PipelineOptions(force_reprocess=True, skip_cache=False))
    t_cold = time.perf_counter() - t0
    
    print(f"Cold preprocessing time: {t_cold:.4f} sec")
    
    # Warm Run (Cache hit)
    print("Running Warm Preprocessing (Cache Hit)...")
    t0 = time.perf_counter()
    res_warm = manager.normalize(source_context, PipelineOptions(force_reprocess=False, skip_cache=False))
    assert res_warm.success
    t_warm = time.perf_counter() - t0
    
    print(f"Warm preprocessing time: {t_warm:.4f} sec")
    
    if t_warm > 0:
        print(f"Cache hit speedup: {t_cold / t_warm:.2f}x faster")
        
    if res_cold.success:
        files_sec = res_cold.statistics.files_processed / t_cold if t_cold > 0 else 0
        print(f"Throughput: {files_sec:.2f} files/sec (Cold)")

if __name__ == "__main__":
    run_benchmark()
