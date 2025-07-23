# Synthetic Graph Benchmarks

[![PyPI version](https://badge.fury.io/py/synthetic-graph-benchmarks.svg)](https://badge.fury.io/py/synthetic-graph-benchmarks)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package implementing standardized benchmarks for evaluating synthetic graph generation methods, based on the evaluation frameworks introduced in:

- [**SPECTRE: Spectral Conditioning Helps to Overcome the Expressivity Limits of One-shot Graph Generators**](https://arxiv.org/pdf/2204.01613) (ICML 2022)
- [**Efficient and Scalable Graph Generation through Iterative Local Expansion**](https://arxiv.org/html/2312.11529v4) (2023)

This package provides a unified interface for benchmarking graph generation algorithms against established datasets and metrics used in the graph generation literature.

## Features

- **Standardized Datasets**: Access to benchmark datasets including Stochastic Block Model (SBM), Planar graphs, and Tree graphs
- **Comprehensive Metrics**: Implementation of key evaluation metrics including:
  - Degree distribution comparison (MMD)
  - Clustering coefficient analysis  
  - Orbit count statistics (using ORCA)
  - Spectral properties analysis
  - Wavelet coefficient comparison
- **Validation Metrics**: Graph-type specific validation (planarity, tree properties, SBM likelihood)
- **Reproducible Evaluation**: Consistent benchmarking across different graph generation methods
- **Easy Integration**: Simple API for evaluating your own graph generation algorithms

## Installation

### From PyPI (recommended)

```bash
pip install synthetic-graph-benchmarks
```

### From Source

```bash
git clone https://github.com/peteole/synthetic_graph_benchmarks.git
cd synthetic_graph_benchmarks
pip install -e .
```

## Quick Start

```python
import networkx as nx
from synthetic_graph_benchmarks import (
    benchmark_planar_results,
    benchmark_sbm_results, 
    benchmark_tree_results
)

# Generate some example graphs (replace with your graph generation method)
generated_graphs = [nx.erdos_renyi_graph(64, 0.1) for _ in range(20)]

# Benchmark against planar graph dataset
results = benchmark_planar_results(generated_graphs)
print(f"Planar accuracy: {results['planar_acc']:.3f}")
print(f"Average metric ratio: {results['average_ratio']:.3f}")

# Benchmark against SBM dataset  
sbm_results = benchmark_sbm_results(generated_graphs)
print(f"SBM accuracy: {sbm_results['sbm_acc']:.3f}")

# Benchmark against tree dataset
tree_results = benchmark_tree_results(generated_graphs)
print(f"Tree accuracy: {tree_results['planar_acc']:.3f}")
```

## Datasets

The package provides access to three standard benchmark datasets:

### Stochastic Block Model (SBM)
- **Size**: 200 graphs
- **Properties**: 2-5 communities, 20-40 nodes per community
- **Edge probabilities**: 0.3 intra-community, 0.05 inter-community

### Planar Graphs  
- **Size**: 200 graphs with 64 nodes each
- **Generation**: Delaunay triangulation on random points in unit square
- **Properties**: Guaranteed planarity

### Tree Graphs
- **Size**: 200 graphs with 64 nodes each  
- **Properties**: Connected acyclic graphs (trees)

## Evaluation Metrics

### Graph Statistics
- **Degree Distribution**: Maximum Mean Discrepancy (MMD) between degree histograms
- **Clustering Coefficient**: Local clustering coefficient comparison
- **Orbit Counts**: 4-node orbit statistics using ORCA package
- **Spectral Properties**: Laplacian eigenvalue distribution analysis
- **Wavelet Coefficients**: Graph wavelet signature comparison

### Validity Metrics
- **Planar Accuracy**: Fraction of generated graphs that are planar
- **Tree Accuracy**: Fraction of generated graphs that are trees (acyclic)
- **SBM Accuracy**: Likelihood of graphs under fitted SBM parameters

### Quality Scores
- **Uniqueness**: Fraction of non-isomorphic graphs in generated set
- **Novelty**: Fraction of generated graphs not isomorphic to training graphs
- **Validity-Uniqueness-Novelty (VUN)**: Combined score for overall quality

## Advanced Usage

### Custom Evaluation

```python
from synthetic_graph_benchmarks.dataset import Dataset
from synthetic_graph_benchmarks.spectre_utils import PlanarSamplingMetrics

# Load dataset manually
dataset = Dataset.load_planar()
print(f"Training graphs: {len(dataset.train_graphs)}")
print(f"Validation graphs: {len(dataset.val_graphs)}")

# Use metrics directly
metrics = PlanarSamplingMetrics(dataset)
test_metrics = metrics.forward(dataset.train_graphs, test=True)
results = metrics.forward(generated_graphs, ref_metrics={"test": test_metrics}, test=True)
```

### Accessing Individual Metrics

```python
# Get detailed breakdown of all metrics
results = benchmark_planar_results(generated_graphs)

# Individual metric values
print(f"Degree MMD: {results['degree']:.6f}")
print(f"Clustering MMD: {results['clustering']:.6f}")  
print(f"Orbit MMD: {results['orbit']:.6f}")
print(f"Spectral MMD: {results['spectre']:.6f}")
print(f"Wavelet MMD: {results['wavelet']:.6f}")

# Ratios compared to training set
print(f"Degree ratio: {results['degree_ratio']:.3f}")
print(f"Average ratio: {results['average_ratio']:.3f}")
```

## Citing

If you use this package in your research, please cite the original papers:

```bibtex
@inproceedings{martinkus2022spectre,
  title={SPECTRE: Spectral Conditioning Helps to Overcome the Expressivity Limits of One-shot Graph Generators},
  author={Martinkus, Karolis and Loukas, Andreas and Perraudin, Nathanaël and Wattenhofer, Roger},
  booktitle={International Conference on Machine Learning},
  pages={15159--15202},
  year={2022},
  organization={PMLR}
}

@article{bergmeister2023efficient,
  title={Efficient and Scalable Graph Generation through Iterative Local Expansion},
  author={Bergmeister, Andreas and Martinkus, Karolis and Perraudin, Nathanaël and Wattenhofer, Roger},
  journal={arXiv preprint arXiv:2312.11529},
  year={2023}
}
```

## Dependencies

- Python ≥ 3.10
- NetworkX ≥ 3.4.2
- NumPy ≥ 2.2.6  
- SciPy ≥ 1.15.3
- PyGSP ≥ 0.5.1
- scikit-learn ≥ 1.7.1
- ORCA-graphlets ≥ 0.1.4
- PyTorch ≥ 2.3.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This package is based on evaluation frameworks developed by:
- Karolis Martinkus (SPECTRE paper)
- Andreas Bergmeister (Iterative Local Expansion paper)
- The original GRAN evaluation codebase
- NetworkX and PyGSP communities