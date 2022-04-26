import random
import numpy as np
from .breadth_first_search import distance_from


def estimate_diameter(graph, k: int):
    random.seed(10)
    n = graph.size
    distances = [float("inf")] * n
    diameter_estimate = -float("inf")
    for i in range(1, k + 1):
        if i == 1:
            v = random.randint(0, n - 1)
        else:
            # choose furthest from set of proccessed nodes
            v = np.argmax(distances)

        bfs_result = distance_from(graph, v)  # bfs
        distances = list(map(min, zip(bfs_result, distances)))
        diameter_estimate = max(diameter_estimate, max(bfs_result))
    return diameter_estimate

# TODO: eliminate code repition
def estimate_radius(graph, k: int):
    random.seed(10)
    n = graph.size
    distances = [float("inf")] * n
    radius_estimate = float("inf")
    for i in range(1, k + 1):
        if i == 1:
            v = random.randint(0, n - 1)
        else:
            # choose furthest from set of proccessed nodes
            v = np.argmax(distances)

        bfs_result = distance_from(graph, v)  # bfs
        distances = list(map(min, zip(bfs_result, distances)))
        radius_estimate = min(radius_estimate, max(bfs_result))
    return radius_estimate
