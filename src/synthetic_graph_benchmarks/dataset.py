
from dataclasses import dataclass

import networkx
import pickle

from synthetic_graph_benchmarks.utils import download_file


@dataclass
class Dataset:
    """A simple dataset class to hold train, validation, and test graphs."""
    train_graphs: list[networkx.Graph]
    val_graphs: list[networkx.Graph]
    test_graphs: list[networkx.Graph] | None = None
    
    
    @classmethod
    def load_from_pickle_url(cls, url: str, cache_dir: str = "data") -> "Dataset":
        """
        Load a dataset from a pickle file available at the given URL.
        
        Args:
            url (str): The URL of the pickle file containing the dataset.
        
        Returns:
            Dataset: An instance of the Dataset class with loaded graphs.
        """
        res = download_file(url, cache_dir)
        with open(res, "rb") as f:
            data = pickle.load(f)
        return cls(
            train_graphs=data['train'],
            val_graphs=data['val'],
            test_graphs=data.get('test', None)
        )
    @classmethod
    def load_sbm(cls, cache_dir: str = "data") -> "Dataset":
        """Load a dataset of Stochastic Block Model (SBM) graphs."""
        return cls.load_from_pickle_url("https://raw.githubusercontent.com/AndreasBergmeister/graph-generation/main/data/sbm.pkl", cache_dir)
    
    @classmethod
    def load_planar(cls, cache_dir: str = "data") -> "Dataset":
        """Load a dataset of planar graphs."""
        return cls.load_from_pickle_url("https://raw.githubusercontent.com/AndreasBergmeister/graph-generation/main/data/planar.pkl", cache_dir)

    @classmethod
    def load_tree(cls, cache_dir: str = "data") -> "Dataset":
        """Load a dataset of tree graphs."""
        return cls.load_from_pickle_url("https://raw.githubusercontent.com/AndreasBergmeister/graph-generation/main/data/tree.pkl", cache_dir)