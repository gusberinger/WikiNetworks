from .breadth_first_search import distance_from
import random
import numpy as np


def closeness_centrality(k, graph):
    n = graph.size
    total = np.zeros(n)
    for _ in range(k):
        i = random.randint(0, n - 1)
        sssp = distance_from(graph, i)
        total += (n / (k * (n-1))) * sssp
    return 1 / total
