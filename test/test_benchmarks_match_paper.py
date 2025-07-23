from typing import Literal
import numpy as np
import pytest
import torch
from synthetic_graph_benchmarks.dataset import Dataset
from synthetic_graph_benchmarks.spectre_utils import PlanarSamplingMetrics, SBMSamplingMetrics
from synthetic_graph_benchmarks.utils import download_file
import networkx as nx



def load_spectre_planar():
    url = "https://github.com/AndreasBergmeister/graph-generation/raw/refs/heads/main/data/spectre/planar_64_200.pt"

    path = download_file(url, "data")
    with open(path, "rb") as f:
        data = torch.load(f)
    graphs = data[0]
    return [nx.from_numpy_array(graph.numpy()) for graph in graphs]

def load_spectre_sbm():
    url = "https://github.com/AndreasBergmeister/graph-generation/raw/refs/heads/main/data/spectre/sbm_200.pt"

    path = download_file(url, "data")
    with open(path, "rb") as f:
        data = torch.load(f)
    graphs = data[0]
    return [nx.from_numpy_array(graph.numpy()) for graph in graphs]

def load_digress_planar():
    url = "https://github.com/cvignac/DiGress/raw/refs/heads/main/generated_samples/generated_planar_adj_matrices.npz"
    res = download_file(url, "data")
    with np.load(res) as data:
        adjacency_matrices = [data[key] for key in sorted(data.files)]
    graphs = [nx.from_numpy_array(adj) for adj in adjacency_matrices]
    return graphs

def load_digress_sbm():
    url = "https://github.com/cvignac/DiGress/raw/refs/heads/main/generated_samples/generated_samples_sbm.txt"
    res = download_file(url, "data")
    with open(res, "r") as f:
        lines = f.readlines()
    graphs = []
    N: int | None = None
    X: list[int] = []
    E: list[list[int]] = []
    state: Literal["N", "X", "E"] = "N"
    for line in lines:
        line = line.strip()
        if line.startswith("N="):
            if N is not None:
                # Save the previous graph
                graphs.append((N, X, np.array(E)))
            N = int(line.split("=")[1])
            state = "N"
            continue
        elif line == "X:":
            state = "X"
            X = []
            continue
        elif line == "E:":
            state = "E"
            E = []
            continue
        if state == "X":
            X = list(map(int, line.split()))
        elif state == "E":
            if line:
                E.append(list(map(int, line.split())))
    if N is not None:
        # Save the last graph
        graphs.append((N, X, np.array(E)))
    return [nx.from_numpy_array(E) for N, X, E in graphs if len(E) > 0]

def test_planar_benchmarks():
    print("Testing Planar benchmarks")
    digress_graphs = load_digress_planar()
    # print(digress_graphs)
    ds = Dataset.load_planar()
    print(f"Loaded dataset with {len(ds.train_graphs)} training graphs")
    metrics = PlanarSamplingMetrics(ds)
    # Here you would set up your test graphs and run the metrics
    # For now, we just assert that the metrics object is created
    assert metrics is not None
    val_metrics = metrics.forward(ds.train_graphs,test=False)
    print("val metrics: ", val_metrics)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    print("test metrics: ", test_metrics)
    assert pytest.approx(0.0002, rel=0.05) == test_metrics['degree'], "Degree metric does not match expected value"
    assert pytest.approx(0.0310, rel=0.05) == test_metrics['clustering'], "Clustering metric does not match expected value"
    assert pytest.approx(0.0005, rel=0.1) == test_metrics['orbit'], "Orbit metric does not match expected value"
    assert pytest.approx(0.0038, rel=0.05) == test_metrics['spectre'], "Spectral metric does not match expected value"
    assert pytest.approx(0.0012, rel=0.05) == test_metrics['wavelet'], "Wavelet metric does not match expected value"

    print("test metrics with ratios: ",metrics.forward(ds.train_graphs, ref_metrics={"val": val_metrics, "test": test_metrics}, test=True))
    print("digress metrics: ",metrics.forward(digress_graphs, ref_metrics={"val": val_metrics, "test": test_metrics}, test=True))
    # spectre_graphs = load_spectre_planar()
    # print("spectre metrics: ", metrics.forward(spectre_graphs, ref_metrics={"val": val_metrics, "test": test_metrics}, test=True))
    
def test_sbm_benchmarks():
    print("Testing SBM benchmarks")
    digress_graphs = load_digress_sbm()
    ds = Dataset.load_sbm()
    print(f"Loaded dataset with {len(ds.train_graphs)} training graphs")
    metrics = SBMSamplingMetrics(ds)
    # Here you would set up your test graphs and run the metrics
    # For now, we just assert that the metrics object is created
    assert metrics is not None
    val_metrics = metrics.forward(ds.train_graphs,test=False)
    print("val metrics: ", val_metrics)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    print("test metrics: ", test_metrics)
    assert pytest.approx(0.0008	, rel=0.1) == test_metrics['degree'], "Degree metric does not match expected value"
    assert pytest.approx(0.0332	, rel=0.05) == test_metrics['clustering'], "Clustering metric does not match expected value"
    assert pytest.approx(0.0255, rel=0.1) == test_metrics['orbit'], "Orbit metric does not match expected value"
    assert pytest.approx(0.0027, rel=0.05) == test_metrics['spectre'], "Spectral metric does not match expected value"
    assert pytest.approx(0.0007, rel=0.05) == test_metrics['wavelet'], "Wavelet metric does not match expected value"
    print("test metrics with ratios: ",metrics.forward(ds.train_graphs, ref_metrics={ "test": test_metrics}, test=True))
    
    print("digress metrics: ",metrics.forward(digress_graphs, ref_metrics={"val": val_metrics, "test": test_metrics}, test=True))


def test_tree_benchmarks():
    print("Testing Tree benchmarks")
    ds = Dataset.load_tree()
    print(f"Loaded dataset with {len(ds.train_graphs)} training graphs")
    metrics = PlanarSamplingMetrics(ds)  # Assuming tree uses same metrics as planar
    # Here you would set up your test graphs and run the metrics
    # For now, we just assert that the metrics object is created
    assert metrics is not None
    val_metrics = metrics.forward(ds.train_graphs, test=False)
    print("val metrics: ", val_metrics)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    print("test metrics: ", test_metrics)
    assert pytest.approx(0.0001, rel=0.15) == test_metrics['degree'], "Degree metric does not match expected value"
    assert pytest.approx(0.0000, abs=1e-4) == test_metrics['clustering'], "Clustering metric does not match expected value"
    assert pytest.approx(0.0000, abs=1e-4) == test_metrics['orbit'], "Orbit metric does not match expected value"
    assert pytest.approx(0.0075, rel=0.05) == test_metrics['spectre'], "Spectral metric does not match expected value"
    assert pytest.approx(0.0030, rel=0.05) == test_metrics['wavelet'], "Wavelet metric does not match expected value"
    
    print("test metrics with ratios: ", metrics.forward(ds.train_graphs, ref_metrics={"val": val_metrics, "test": test_metrics}, test=True))
