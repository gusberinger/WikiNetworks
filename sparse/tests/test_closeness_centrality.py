import sparse
import unittest
import networkx as nx


class TestCloseness(unittest.TestCase):

    def test_closeness():
        G = sparse.random_graph.small_sample_graph()
        cu_nx_dict = nx.closeness_centrality(G.to_networkx())
        cu_nx = [cu_nx_dict[k] for k in sorted(cu_nx_dict)]
        cu_sparse = sparse.closeness_centrality(3000, G)
        print(cu_nx)
        print(cu_sparse)


if __name__ == "__main__":
    TestCloseness.test_closeness()