import itertools
import random
import string
import networkx as nx
from helpers import *

def titles():
    """Generator: 'A', 'B', 'C', ..., 'AA', 'AB',... """
    for i in itertools.count(1):
        for p in itertools.product(string.ascii_uppercase, repeat=i):
            yield ''.join(p)


def random_integers():
    while True:
        yield random.randint(0, 9000000)



def create_sparse_graph():
    G = nx.binomial_graph(200, 5 / 200, directed = True)
    adj = nx.adjacency_matrix(G).to_scipy_sparse_matrix()
    titles = titles()
    article_ids = random_integers()



