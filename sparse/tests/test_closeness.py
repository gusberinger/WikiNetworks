from random import random
from sparse import random_sparse_graph, breadth_first_search_level
import numpy as np
import unittest
import networkx as nx
from collections import OrderedDict

class TestCloseness(unittest.TestCase):

    def test_random_subgraph_graph(self):
        graph = random_sparse_graph(1000, .01)
        subgraph = graph.get_largest_component()
        order = breadth_first_search_level(subgraph, 10)
        self.assertEqual(np.sum(order == 0), 1)
        self.assertEqual(np.sum(order < 0), 0)
        self.assertEqual(len(order), graph.size)

    # def compare_to_networkx(self):

if __name__ == "__main__":
    # unittest.main()
    # test_random_graph()
    graph = random_sparse_graph(50, .1)
    subgraph = graph.get_largest_component()
    nx_graph = subgraph.to_networkx()

    # print(nx_graph.nodes())
    # exit()
    print(nx_graph)
    nx_level_dict = OrderedDict(sorted(nx.single_source_shortest_path(nx_graph, 10).items()))
    print(nx_level_dict)
    # nx_level = [len(nx_level_dict[k]) for k in sorted(nx_level_dict)]
    # order = breadth_first_search_level(subgraph, 10)
    # print(list(zip(order, nx_level)))
    # print(nx_level)