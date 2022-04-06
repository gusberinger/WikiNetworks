import numpy as np
import pandas as pd
import scipy
from .random_graph import random_sparse_graph
from sknetwork.ranking import Katz
import scipy.sparse
import scipy.sparse.linalg
import logging


def katz_centrality(graph, alpha: float = 0.1, beta: float = 1,
                    max_iter = 1000, tol=1.0e-6, normalized = True):
    A = graph.adjacency.transpose()
    n = graph.size
    e = np.ones((n, 1))
    last = e.copy()
    for k in range(max_iter):
        current = alpha * A * last + beta * e
        error = sum((current[i] - last[i] for i in range(n)))
        if error < n * tol:
            logging.info(f"Converged in {k} iterations")
            if normalized:
                norm = np.sign(sum(current)) * np.linalg.norm(current)
                return map(float, current / norm)

            else:
                return current

    raise ValueError(f"Failed to converge in {max_iter} iterations.")