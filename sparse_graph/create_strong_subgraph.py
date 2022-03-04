from scipy import sparse
from scipy.sparse import csr_matrix, load_npz
import numpy as np
from helpers import *
import find_from_big


def _delete_from_csr(mat : sparse.csr.csr_matrix, row_indices=[], col_indices=[]):
    """
    source: https://stackoverflow.com/questions/13077527
    Remove the rows (denoted by ``row_indices``) and columns (denoted by ``col_indices``) from the CSR sparse matrix ``mat``.
    """
    rows = []
    cols = []
    if row_indices:
        rows = list(row_indices)
    if col_indices:
        cols = list(col_indices)

    if len(rows) > 0 and len(cols) > 0:
        row_mask = np.ones(mat.shape[0], dtype=bool)
        row_mask[rows] = False
        col_mask = np.ones(mat.shape[1], dtype=bool)
        col_mask[cols] = False
        return mat[row_mask][:,col_mask]
    elif len(rows) > 0:
        mask = np.ones(mat.shape[0], dtype=bool)
        mask[rows] = False
        return mat[mask]
    elif len(cols) > 0:
        mask = np.ones(mat.shape[1], dtype=bool)
        mask[cols] = False
        return mat[:,mask]
    else:
        return mat


def get_largest_component(matrix : sparse.csr.csr_matrix, labels, 
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
    unconnected_indeces = list(set(range(mat.shape[0])) - set(indices))
    sub_labels = list(np.delete(labels, unconnected_indeces))
    sub_matrix = _delete_from_csr(mat, row_indices=unconnected_indeces, col_indices=unconnected_indeces)
    return sub_matrix, sub_labels


if __name__ == "__main__":
    mat = load_npz(SPARSE_MATRIX_PATH)
    node_list = find_from_big.node_list
    sub_graph, sub_labels = get_largest_component(mat, node_list)
    print(len(sub_labels))