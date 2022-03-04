import logging
from typing import List
from scipy import sparse
from scipy.sparse import load_npz
import numpy as np
from helpers import *

log = logging.getLogger(__name__)

def _delete_from_csr(mat, indices : List[int]):
    """
    Remove the indices from the CSR sparse matrix ``mat``.
    """
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("Matrix must be square.")

    mask = np.ones(mat.shape[0], dtype=bool)
    mask[indices] = False
    return mat[mask][:,mask]



def get_largest_component(matrix, labels, 
    directed : bool = True, connection : str = "strong"):
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
    _, component_labels = sparse.csgraph.connected_components(matrix, directed=directed, connection=connection)
    unique_component_labels, count = np.unique(component_labels, return_counts=True)
    largest = unique_component_labels[np.argmax(count)]
    indices = np.where(component_labels == largest)[0]
    unconnected_indices = list(set(range(mat.shape[0])) - set(indices))
    # sub_labels = list(np.delete(labels, unconnected_indeces))
    labels.remove_indices(unconnected_indices)
    sub_matrix = _delete_from_csr(mat, unconnected_indices)
    return sub_matrix, labels


if __name__ == "__main__":
    # log = logging.getLogger(__name__)
    log.info("test1")
    log.warning("test")
    mat = load_npz(SPARSE_MATRIX_PATH)
    node_list = load_node_list()
    log.info("getting subgraph")
    sub_graph, sub_labels = get_largest_component(mat, node_list)
    print(len(sub_labels))
    print(len(node_list))