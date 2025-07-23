from typing import TypedDict
from synthetic_graph_benchmarks.dataset import Dataset
from synthetic_graph_benchmarks.spectre_utils import (
    SBMSamplingMetrics,
    PlanarSamplingMetrics,
    TreeSamplingMetrics,
)
import networkx as nx

class PlanarBenchmarkResults(TypedDict):
        degree: float
        wavelet: float
        spectre: float
        clustering: float
        orbit: float
        planar_acc: float
        degree_ratio: float
        clustering_ratio: float
        orbit_ratio: float
        spectre_ratio: float
        wavelet_ratio: float
        average_ratio: float

class SBMBenchmarkResults(TypedDict):
    degree: float
    wavelet: float
    spectre: float
    clustering: float
    orbit: float
    sbm_acc: float
    sampling_frac_unique: float
    sampling_frac_unique_non_iso: float
    sampling_frac_unic_non_iso_valid: float
    sampling_frac_non_iso: float
    degree_ratio: float
    clustering_ratio: float
    orbit_ratio: float
    spectre_ratio: float
    wavelet_ratio: float
    average_ratio: float

class TreeBenchmarkResults(TypedDict):
    degree: float
    wavelet: float
    spectre: float
    clustering: float
    orbit: float
    planar_acc: float
    sampling_frac_unique: float
    sampling_frac_unique_non_iso: float
    sampling_frac_unic_non_iso_valid: float
    sampling_frac_non_iso: float
    degree_ratio: float
    spectre_ratio: float
    wavelet_ratio: float
    average_ratio: float



def benchmark_sbm_results(generated_graphs: list[nx.Graph]) -> SBMBenchmarkResults:
    """Benchmark the results of generated graphs against the SBM dataset."""
    ds = Dataset.load_sbm()
    metrics = SBMSamplingMetrics(ds)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    return metrics.forward(
        generated_graphs, ref_metrics={"test": test_metrics}, test=True
    ) # type: ignore

def benchmark_planar_results(generated_graphs: list[nx.Graph]) -> PlanarBenchmarkResults:
    """Benchmark the results of generated graphs against the Planar dataset."""
    ds = Dataset.load_planar()
    metrics = PlanarSamplingMetrics(ds)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    return metrics.forward(
        generated_graphs, ref_metrics={"test": test_metrics}, test=True
    ) # type: ignore

def benchmark_tree_results(generated_graphs: list[nx.Graph]) -> TreeBenchmarkResults:
    """Benchmark the results of generated graphs against the Tree dataset."""
    ds = Dataset.load_tree()
    metrics = TreeSamplingMetrics(ds)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    return metrics.forward(
        generated_graphs, ref_metrics={"test": test_metrics}, test=True
    ) # type: ignore