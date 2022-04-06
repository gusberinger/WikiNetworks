import numpy as np


def katz_centrality(
    graph,
    alpha: float = 0.1,
    beta: float = 1,
    max_iter: int = 10000,
    tol: float = 1.0e-6,
    normalized: bool = True
):
    A = graph.adjacency.transpose()
    n = graph.size
    e = np.ones((n, 1))
    last = e.copy()
    for _ in range(max_iter):
        current = alpha * A.dot(last) + beta * e
        error = sum((abs(current[i] - last[i]) for i in range(n)))
        if error < n * tol:
            centrality = current.flatten().tolist()
            if normalized:
                norm = np.sign(sum(centrality)) * np.linalg.norm(centrality)
                return map(float, centrality / norm)
            else:
                return centrality
        last = current.copy()

    raise ValueError(f"Failed to converge in {max_iter} iterations.")
