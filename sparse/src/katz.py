import pandas as pd
from random_graph import random_sparse_graph
from sknetwork.ranking import Katz


def katz_centrality(graph):
    close = Katz()
    scores = close.fit_transform(graph.adjacency)
    rows = [(graph.labels.find_title_from_index(i),
             graph.labels.find_article_id_from_index(i),
             score) for i, score in enumerate(scores)]
    df = pd.DataFrame(rows, columns=["title", "article_id", "score"])
    return df


if __name__ == "__main__":
    graph = random_sparse_graph(100, .1)
    report = katz_centrality(graph)
    print(report)
