import logging
from re import sub
from typing import Any, List, Optional, Union
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

    def __init__(self, adjacency, labels : Union[List[Any], NodeList]) -> None:
        self.adjacency = adjacency
        # self.adjacency_csc = adjacency.tocsc()
        self.labels = NodeList(labels) if not isinstance(labels, NodeList) else labels
        self.in_degrees = None
        self.out_degrees = None

    def get_largest_component(self, directed : bool = True, connection : str = "strong") -> 'SparseGraph':
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
        sub_graph = SparseGraph(sub_matrix, self.labels)
        return sub_graph

    def compute_degree(self) -> None:
        """
        Fills in the degrees for self.in_degree and self.out_degree
        """
        self.in_degree = np.array(np.sum(self.adjacency, axis = 0))[0]
        self.out_degree = np.array(np.sum(self.adjacency, axis = 1).transpose())[0]
        

    def outgoing_neighbors(self, index : int) -> list[int]:
        nodes = self.adjacency[index,:].toarray()[0]
        return np.nonzero(nodes)[0]

    def incoming_neighbors(self, index : int) -> list[int]:
        nodes = self.adjacency[:, index].toarray()[0]
        return np.nonzero(nodes)[0]

    def remove_indices(self, indices : List[int]):
        new_adjacency = _delete_from_csr(self.adjacency, indices)
        new_labels = self.labels.remove_indices(indices)



if __name__ == "__main__":
    # US_ARTICLE_ID = 12
    adj = load_npz(SPARSE_MATRIX_PATH)
    node_list = load_node_list()
    graph = SparseGraph(adj, node_list)
    log.info("Imported graph")
    graph.compute_degree()
    log.info("Computed degrees.")
    print(graph.out_degree.shape)
    print(type(graph.out_degree))
    print(graph.out_degree)
    print(int(graph.out_degree[0]))
    us_index = node_list.find_index(US_ARTICLE_ID)
    