import itertools
from re import sub
import string
import scipy.sparse as sp
import networkx as nx
import create_connected_subgraph


def _column_name_generator():
    for i in itertools.count(1):
        for p in itertools.product(string.ascii_uppercase, repeat=i):
            yield ''.join(p)

G = nx.binomial_graph(1000, .1, directed = True)
adj_array = nx.adjacency_matrix(G).toarray()
adj = sp.csr_matrix(adj_array)

gen_labels = _column_name_generator()
labels = [next(gen_labels) for _ in range(adj.shape[0])]

sub_adj = create_connected_subgraph.get_largest_component(adj, labels)

print(sub_adj)