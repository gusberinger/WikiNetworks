from distutils.sysconfig import customize_compiler
import sparse
import unittest
import networkx as nx
from scipy.stats import pearsonr


class TestCloseness(unittest.TestCase):

    def test_closeness_small(self):
        G = sparse.random_graph.small_sample_graph()
        cu_nx_dict = nx.closeness_centrality(G.to_networkx())
        cu_nx = [cu_nx_dict[k] for k in sorted(cu_nx_dict)]
        cu_sparse = sparse.closeness_centrality(300, G)
        cor = pearsonr(cu_nx, cu_sparse)[0]
        self.assertGreater(cor, .95)


    def test_closeness_big(self):
        G = sparse.random_sparse_graph(1000, .005, 100)
        G = G.get_largest_component()
        cu_sparse = sparse.closeness_centrality(300, G)
        cu_nx_dict = nx.closeness_centrality(G.to_networkx())
        cu_nx = [cu_nx_dict[k] for k in sorted(cu_nx_dict)]
        cor = pearsonr(cu_nx, cu_sparse)[0]
        self.assertGreater(cor, .95)



if __name__ == "__main__":
    unittest.main()