import numpy as np
import scipy as sp
import unittest
import networkx as nx
from sparse import random_graph
from sparse.katz import katz_centrality
from scipy.stats import pearsonr

class TestKatzCentrality(unittest.TestCase):

    def test_example(self):
        adj = np.array([[0, 1, 1, 1, 0], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 0], [0, 1, 1, 0, 0]])
        nxG = nx.from_numpy_array(adj)
        G = random_graph.from_networkx(nxG)
        sparse_scores = katz_centrality(G, alpha=0.25, beta=0.2, normalized=False)
        real_scores = [1.1428571428571426, 1.3142857142857138, 1.3142857142857138, 1.1428571428571426, 0.857142857142857]
        cor = pearsonr(sparse_scores, real_scores)[0]
        self.assertGreater(cor, .99)

    def test_kite(self):
        nx_graph = nx.krackhardt_kite_graph()
        graph = random_graph.from_networkx(nx_graph)

        sparse_scores = list(katz_centrality(graph, alpha=.1, beta=1))
        nx_scores = list(nx.katz_centrality(nx_graph).values())
        cor = pearsonr(sparse_scores, nx_scores)[0]
        self.assertGreater(cor, .9999)

if __name__ == "__main__":
    unittest.main()