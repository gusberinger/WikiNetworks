import logging
from re import sub
from typing import Any, List, Optional
from scipy import sparse
from scipy.sparse import load_npz
import numpy as np
from helpers import *

log = logging.getLogger(__name__)

def _delete_from_csr(mat, indices : List[int]):
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

    def __init__(self, adjacency, labels : list[Any] | NodeList) -> None:
        self.adjacency = adjacency
        self.labels = NodeList(labels) if not isinstance(labels, NodeList) else labels
        self.in_degrees = None
        self.out_degrees = None

    def get_largest_component(self, directed : bool = True, connection : str = "strong"):
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
        self.labels.remove_indices(unconnected_indices)
        sub_matrix = _delete_from_csr(self.adjacency, unconnected_indices)
        sub_graph = (sub_matrix, self.labels)
        return sub_graph

    def compute_degree(self) -> None:
        """
        Fills in the degrees for self.in_degree and self.out_degree
        """
        self.in_degree = np.sum(self.adjacency, axis = 0)
        self.out_degree = np.sum(self.adjacency, axis = 1)
        
    def in_degree(self, index : int) -> int:
        return self.in_degree

    def out_degree(self, index : int) -> int:
        return self.out_degree

    def outgoing(self, index : int) -> list[int]:
        nodes = self.adjacency[index,:].toarray()[0]
        return nodes[nodes != 0]

    def incoming(self, index : int) -> list[int]:
        nodes = self.adjacency[index,:].toarray()[0]
        return nodes[nodes != 0]


if __name__ == "__main__":
    # US_ARTICLE_ID = 12
    mat = load_npz(SPARSE_MATRIX_PATH)
    node_list = load_node_list()

    us_index = node_list.find_index(US_ARTICLE_ID)
    print("us index: ", us_index)
    # print(mat[row, col])

    print("out deg:", out_degree(mat, us_index))
    print("in deg:", in_degree(mat, us_index))

    log.info("getting subgraph")
    sub_graph, sub_labels = get_largest_component(mat, node_list)
    print(len(sub_labels) / mat.shape[0])
    print(len(node_list))
    us_index = sub_labels.find_index(US_ARTICLE_ID)
    print("us index: ", us_index)

    print("out deg:", out_degree(sub_graph, us_index))
    print("in deg:", in_degree(sub_graph, us_index))