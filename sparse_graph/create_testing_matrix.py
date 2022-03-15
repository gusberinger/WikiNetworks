import itertools
from re import sub
import string
import scipy.sparse as sp
import networkx as nx
from create_connected_subgraph import SparseGraph
from helpers import *

def _column_name_generator():
    for i in itertools.count(1):
        for p in itertools.product(string.ascii_uppercase, repeat=i):
            yield ''.join(p)


if __name__ == "__main__":
    G = nx.binomial_graph(200, 5 / 200, directed = True)
    adj = nx.adjacency_matrix(G).to_scipy_sparse_matrix()
    gen_labels = _column_name_generator()
    labels = NodeList([next(gen_labels) for _ in range(adj.shape[0])])
    mainGraph = SparseGraph(adj, labels)
    sub_adj, sub_labels = mainGraph.get_largest_component()


    with open(TESTING_MATRIX_PATH, "wb") as f:
        pickle.dump((sub_adj, sub_labels), f)

