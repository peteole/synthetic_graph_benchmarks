from synthetic_graph_benchmarks.dataset import Dataset
from synthetic_graph_benchmarks.spectre_utils import PlanarSamplingMetrics




def test_benchmarks_run():
    ds = Dataset.load_sbm()
    print(f"Loaded dataset with {len(ds.train_graphs)} training graphs")
    metrics = PlanarSamplingMetrics(ds)
    # Here you would set up your test graphs and run the metrics
    # For now, we just assert that the metrics object is created
    assert metrics is not None
    val_metrics = metrics.forward(ds.train_graphs,test=False)
    test_metrics = metrics.forward(ds.train_graphs, test=True)
    print(metrics.forward(ds.val_graphs[:20], ref_metrics={"val": val_metrics, "test": test_metrics}, test=False))