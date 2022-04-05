import itertools
import random
import string
import networkx as nx
import pandas as pd
from .sparse_graph import SparseGraph


def titles():
    """Generator: 'A', 'B', 'C', ..., 'AA', 'AB',... """
    for i in itertools.count(1):
        for p in itertools.product(string.ascii_uppercase, repeat=i):
            yield ''.join(p)


def random_integers():
    while True:
        yield random.randint(0, 9000000)


def random_sparse_graph(nodes, p):
    G = nx.binomial_graph(nodes, p, directed=True)
    adj = nx.adjacency_matrix(G).to_scipy_sparse_matrix()
    titles = titles()
    article_ids = random_integers()
    rows = itertools.islice(zip(titles, article_ids), nodes)
    label_df = pd.DataFrame(rows)
    graph = SparseGraph(adj, label_df)
    return graph

if __name__ == "__main__":
    graph = random_sparse_graph(100, .01)
    print(graph)


