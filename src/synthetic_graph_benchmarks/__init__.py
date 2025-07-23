from synthetic_graph_benchmarks.benchmarks import (
    benchmark_sbm_results,
    benchmark_planar_results,
    benchmark_tree_results,
)
from synthetic_graph_benchmarks.dataset import Dataset

__version__ = "0.1.1"

def main():
    """Main entry point for the CLI."""
    print("Synthetic Graph Benchmarks v" + __version__)
    print("For usage examples, see: https://github.com/peteole/synthetic_graph_benchmarks")
    print("Available benchmark functions:")
    print("  - benchmark_sbm_results()")
    print("  - benchmark_planar_results()") 
    print("  - benchmark_tree_results()")

__all__ = [
    "benchmark_sbm_results",
    "benchmark_planar_results", 
    "benchmark_tree_results",
    "__version__",
    "Dataset",
]