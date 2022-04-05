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


def from_networkx(G):
    n = len(G)
    adj = nx.to_scipy_sparse_array(G).astype(bool)
    article_titles = titles()
    article_ids = random_integers()
    rows = itertools.islice(zip(article_titles, article_ids), n)
    label_df = pd.DataFrame(rows, columns=["title", "article_id"])
    graph = SparseGraph(adj, label_df)
    return graph


def random_sparse_graph(nodes, p, seed=None):
    if seed is not None:
        random.seed(seed)
    G = nx.binomial_graph(nodes, p, directed=True)
    return from_networkx(G)


if __name__ == "__main__":
    graph = random_sparse_graph(100, .01)
    print(graph)
