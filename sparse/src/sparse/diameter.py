import random
import numpy as np
from .breadth_first_search import distance_from


def estimate_diameter(graph, k):
    random.seed(10)
    eccentricity = {}
    end = {}
    n = graph.size
    diameter_estimate = -float("inf")
    for i in range(1, k + 1):
        if i == 1:
            v = random.randint(0, n - 1)
        else:
            # choose furthest from set of proccessed nodes
            # set of proccesesd nodes are the keys in eccentricity
            # hence, the furthest from set of processed nodes is the leaf with largest eccentricity
            # the location of the leaf is held in the end dictionary
            v = end[max(eccentricity.items(), key=lambda x: x[1])[0]]

        distances = distance_from(graph, v)  # bfs
        furthest = np.argmax(distances)
        end[v] = furthest
        eccentricity[v] = max(distance_from(graph, v))
        diameter_estimate = max(diameter_estimate, eccentricity[v])
    return diameter_estimate
