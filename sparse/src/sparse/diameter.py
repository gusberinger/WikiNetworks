import random
from scipy import rand
from .breadth_first_search import distance_from


def estimate_diameter(graph, k):
    U = {}
    n = graph.size
    for i in range(1, k+1):
        if i == 1:
            v = random.randint(0, n-1)
        else:
            pass
        U[v] = distance_from(graph, v)
