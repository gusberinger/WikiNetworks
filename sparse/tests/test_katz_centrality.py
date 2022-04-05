import numpy as np
import scipy as sp
import unittest
import networkx as nx
from sparse import random_graph
from sparse.katz import katz_centrality
from scipy.stats import pearsonr

class TestKatzCentrality(unittest.TestCase):

    def test_kite(self):
        nx_graph = nx.krackhardt_kite_graph()
        graph = random_graph.from_networkx(nx_graph)

        sparse_scores = list(katz_centrality(graph, alpha=.1, beta=1))
        nx_scores = list(nx.katz_centrality(nx_graph).values())
        cor = pearsonr(sparse_scores, nx_scores)[0]
        self.assertGreater(cor, .9999)

if __name__ == "__main__":
    unittest.main()