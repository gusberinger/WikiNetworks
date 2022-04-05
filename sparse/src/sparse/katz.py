import pandas as pd
from .random_graph import random_sparse_graph
from sknetwork.ranking import Katz
import random

def katz_centrality(graph, damping_factor: float = 0.5):
    close = Katz(damping_factor=damping_factor, path_length=40)
    scores = close.fit_transform(graph.adjacency)
    rows = [(graph.labels.find_title_from_index(i),
             graph.labels.find_article_id_from_index(i),
             score) for i, score in enumerate(scores)]
    df = pd.DataFrame(rows, columns=["title", "article_id", "score"])
    return df