import numpy as np


class ConvergenceError(Exception):
    def __init__(self, iterations: int) -> None:
        super().__init__(f"Failed to converage after {iterations} iterations.")

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
    last_error = -float("inf")
    for iter_step in range(max_iter):
        print(f"power iteration step: {iter_step=}")
        current = alpha * A.dot(last) + beta * e
        error = sum((abs(current[i] - last[i]) for i in range(n)))
        if error > last_error:
            raise ConvergenceError(iter_step)
        last_error = error
        if error < n * tol:
            centrality = current.flatten().tolist()
            if normalized:
                norm = np.sign(sum(centrality)) * np.linalg.norm(centrality)
                return map(float, centrality / norm)
            else:
                return centrality
        last = current.copy()

    raise ValueError(f"Failed to converge in {max_iter} iterations.")
