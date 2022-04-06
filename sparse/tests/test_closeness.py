from sparse import random_graph, random_sparse_graph, distance_from
import numpy as np
import unittest

class TestCloseness(unittest.TestCase):

    def test_random_subgraph_graph(self):
        graph = random_sparse_graph(1000, .01)
        subgraph = graph.get_largest_component()
        order = distance_from(subgraph, 10)
        self.assertEqual(np.sum(order == 0), 1)
        self.assertEqual(np.sum(order < 0), 0)
        self.assertEqual(len(order), graph.size)

    def compare_to_networkx(self):
        G = random_graph.small_sample_graph()
        distances = distance_from(G, 4)
        self.assertEqual([2, 1, 3, 4, 0], list(distances))

if __name__ == "__main__":

    unittest.main()