from __future__ import annotations
import logging
import pickle
import sqlite3
import pandas as pd
import numpy as np
from typing import Dict, List
from scipy import sparse
from helpers import *

log = logging.getLogger(__name__)


class SparseLabels:

    def __init__(self, new_df: pd.DataFrame) -> None:

        self._internal_df = new_df
        article_id_from_index_dict: Dict[int, int] = dict(zip(new_df.index, new_df["article_id"]))
        index_from_article_id_dict: Dict[int, int] = {v: k for k, v in article_id_from_index_dict.items()}
        title_from_index_dict: Dict[int, int] = dict(zip(new_df.index, new_df["title"]))
        title_from_article_id: Dict[int, int] = dict(zip(new_df["article_id"], new_df["title"]))

        self.find_index_from_article_id = index_from_article_id_dict.get
        self.find_article_id_from_index = article_id_from_index_dict.get
        self.find_title_from_index = title_from_index_dict.get
        self.find_title_from_article_id = title_from_article_id.get

    def remove_indices(self, indices) -> SparseLabels:
        new_df = self._internal_df.drop(indices, axis = 0)
        new_df = new_df.reset_index(drop=True)
        return SparseLabels(new_df)


def _delete_from_csr(mat: sparse.csr_matrix, indices: List[int]) -> sparse.csr_matrix:
    """
    Parameters
    ---
    mat:
        The csr sparse adjacency matrix of the graph.
    indices:
        The indices of the nodes in the graph that will be removed.

    Returns
    ---
    mat:
        The sparse adjacency matrix of the graph with the nodes removed.
    """
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("Matrix must be square.")

    mask = np.ones(mat.shape[0], dtype=bool)
    mask[indices] = False
    return mat[mask][:,mask]

class SparseGraph:

    def __init__(self, adjacency: sparse.csr_matrix,
                       labels: SparseLabels) -> None:
        self.adjacency = adjacency
        self.labels = labels
        self._in_degree = None
        self._out_degree = None

    def get_largest_component(self, directed: bool = True, connection: str = "strong") -> SparseGraph:
        """
        Parameters
        ---
        matrix:
            The sparse adjacency matrix of the graph.
        labels:
            The labels of each node in the graph. The index of the list corresponds to the index in the adjacency matrix.
        direct:
            If ``True`` the graph is treated as directed.
        connection:
            If ``"strong"``, the connected components will all be strongly connected together, if ``"weak"`` the connected components will be weakly connected. If ``directed == False`` the parameter is ignored.

        Returns
        ---
        sub_matrix:
            The sparse adjacency matrix of the largest strongly connected subgraph.
        sub_labels:
            The labels of each node in the subgraph.
        """
        _, component_labels = sparse.csgraph.connected_components(self.adjacency, directed=directed, connection=connection)
        unique_component_labels, count = np.unique(component_labels, return_counts=True)
        largest = unique_component_labels[np.argmax(count)]
        indices = np.where(component_labels == largest)[0]
        unconnected_indices = list(set(range(self.adjacency.shape[0])) - set(indices))
        subgraph = self.remove_indices(unconnected_indices)
        return subgraph

    def compute_degree(self) -> None:
        """
        Fills in the degrees for self.in_degree and self.out_degree
        """
        self._in_degree = np.array(np.sum(self.adjacency, axis=0))[0]
        self._out_degree = np.array(np.sum(self.adjacency, axis=1).transpose())[0]

    def in_degree(self, index: int) -> int:
        if self._in_degree is None:
            raise ValueError("Degrees not computed. Must call self.compute_degree on instance first.")
        else:
            return self._in_degree[index]


    def out_degree(self, index: int) -> int:
        if self._out_degree is None:
            raise ValueError("Degrees not computed. Must call self.compute_degree on instance first.")
        else:
            return self._out_degree[index]

    def outgoing_neighbors(self, index: int) -> np.ndarray:
        nodes = self.adjacency[index,:].toarray()[0]
        return np.nonzero(nodes)[0]

    def incoming_neighbors(self, index: int) -> np.ndarray:
        nodes = self.adjacency[:, index].toarray()[0]
        return np.nonzero(nodes)[0]

    def remove_indices(self, indices: List[int]) -> SparseGraph:
        new_adjacency = _delete_from_csr(self.adjacency, indices)
        new_labels = self.labels.remove_indices(indices)
        return SparseGraph(new_adjacency, new_labels)



def load_wiki_labels(from_scratch = False) -> SparseLabels:
    # load pickled to avoid generating every time.
    if not from_scratch and Path(SPARSE_LABEL_PATH).is_file():
        with open(SPARSE_LABEL_PATH, "rb") as f:
            return pickle.load(f)
    else:
        log.warning("Node list file not found. Generating...")

        if not Path(DATABASE_PATH).is_file():
            raise IOError('Specified SQLite file "{0}" does not exist.'.format(DATABASE_PATH))

        sdow_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        labels_df = pd.read_sql("SELECT id, title FROM pages where is_redirect=0", sdow_conn)
        labels_df = labels_df.rename(columns={"id": "article_id"})
        labels_df = labels_df.sort_values(by = ["article_id"])
        labels = SparseLabels(labels_df)

        with open(SPARSE_LABEL_PATH, "wb") as f:
            pickle.dump(labels, f)

        return labels

def load_wiki_graph() -> SparseGraph:
    labels: SparseLabels = load_wiki_labels()
    with open(SPARSE_MATRIX_PATH, "rb") as f:
        matrix: sparse.csr_matrix = sparse.load_npz(f)
    graph = SparseGraph(matrix, labels)
    return graph




if __name__ == "__main__":
    graph = load_wiki_graph()
    graph.compute_degree()
    N_0 = graph.adjacency.shape[0]
    us_index = graph.labels.find_index_from_article_id(US_ARTICLE_ID)
    print(graph.in_degree(us_index))
    print(graph.labels._internal_df.head(100))
    print("----")

    subgraph = graph.get_largest_component()
    subgraph.compute_degree()
    N_1 = subgraph.adjacency.shape[0]
    print(subgraph.labels._internal_df.head(100))
    us_index = subgraph.labels.find_index_from_article_id(US_ARTICLE_ID)
    print(subgraph.in_degree(us_index))