from sparse import random_graph, random_sparse_graph, distance_from
import numpy as np
import unittest
import networkx as nx
import matplotlib.pyplot as plt
import sparse

class TestBFS(unittest.TestCase):

    def test_random_subgraph_graph(self):
        graph = random_sparse_graph(1000, .01, seed = 100)
        graph = graph.get_largest_component()
        order = distance_from(graph, 10)
        self.assertEqual(np.sum(order == 0), 1)
        self.assertEqual(np.sum(order < 0), 0)
        self.assertEqual(len(order), graph.size)

    def test_sample_graph_single_source(self):
        G = random_graph.small_sample_graph()
        distances = distance_from(G, 4)
        self.assertEqual([2, 1, 3, 4, 0], list(distances))

    def test_sample_graph_multi_source(self):
        G = random_graph.small_sample_graph()
        distances = distance_from(G, [3, 0])
        self.assertEqual([0, 1, 1, 0, 2], list(distances))

    def test_compare_with_networkx_single_source(self):
        G = random_graph.random_sparse_graph(100, .1, seed = 100)
        G = G.get_largest_component()
        nxG = G.to_networkx()
        nx_paths = nx.shortest_path(nxG, source=10)
        nx_order = [len(nx_paths[k])-1 for k in sorted(nx_paths.keys())]
        sparse_order = distance_from(G, 10)
        self.assertEqual(nx_order, list(sparse_order))


    # def test_compare_with_networkx_multi_source(self):
    #     G = random_graph.random_sparse_graph(100, .1, seed = 100)
    #     G = G.get_largest_component()
    #     nxG = G.to_networkx()
    #     nx_paths = nx.shortest_path(nxG, source=10)
    #     nx_order = [len(nx_paths[k])-1 for k in sorted(nx_paths.keys())]
    #     sparse_order = distance_from(G, 10)
    #     self.assertEqual(nx_order, list(sparse_order))


if __name__ == "__main__":
    # G = random_graph.small_sample_graph()
    # distances = distance_from(G, 4)
    unittest.main()
    # TestBFS.test_compare_with_networkx_single_source()
    # TestCloseness.compare_with_networkx_single_source()