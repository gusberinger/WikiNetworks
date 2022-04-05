import numpy as np
import pandas as pd
import scipy
from .random_graph import random_sparse_graph
from sknetwork.ranking import Katz
import scipy.sparse
import scipy.sparse.linalg


def katz_centrality(graph, alpha: float = 0.1, beta: float = 1):
    """Adapted from networkx for sparse matrices"""
    n = graph.size
    A = graph.adjacency
    b = np.ones((n, 1)) * float(beta)
    term = scipy.sparse.eye(n, n) - (alpha * A)
    centrality = scipy.sparse.linalg.spsolve(scipy.sparse.eye(n, n) - (alpha * A), b)
    norm = np.sign(sum(centrality)) * np.linalg.norm(centrality)
    return map(float, centrality / norm)