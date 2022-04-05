import numpy as np
import scipy as sp
import sparse
import unittest
import networkx as nx
from sparse.katz import katz_centrality


if __name__ == "__main__":
    graph = sparse.random_sparse_graph(100, .01)
    report = list(katz_centrality(graph, damping_factor=0.1).score)
    nx_graph = graph.to_networkx()
    nx_scores = nx.katz_centrality(nx_graph).values()
    # for x, y in zip(report, nx_scores, strict=True):
    #     print(x, y)
    cor = np.corrcoef(report, list(nx_scores))
    print(cor)