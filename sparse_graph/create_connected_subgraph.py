import logging
from re import sub
from typing import List, Optional
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
    labels.remove_indices(unconnected_indices)
    sub_matrix = _delete_from_csr(mat, unconnected_indices)
    return sub_matrix, labels

def out_degree(mat, index : Optional[int] = None):
    if index:
        return np.count_nonzero(mat[index, :].toarray()[0])
    else:
        out_degree, _ = np.histogram(mat.nonzero()[0], np.arange(mat.shape[0] + 1))
        return out_degree
    

def in_degree(mat, index : Optional[int] = None):
    if index:
        return np.count_nonzero(mat[:, index].toarray()[0])
    else:
        out_degree, _ = np.histogram(mat.nonzero()[1], np.arange(mat.shape[0] + 1))
        return out_degree

if __name__ == "__main__":
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