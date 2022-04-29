import scipy.sparse.linalg
from load_wiki import load_wikipedia
from helpers import REPORT_PATH, US_ARTICLE_ID
import sparse

CENTRALITY_REPORT = REPORT_PATH.joinpath("closeness_centrality.parquet")

if __name__ == "__main__":
    G = load_wikipedia()
    G.compute_degree()
    n0 = G.adjacency.shape[0]
    print(n0)
    in_degree = enumerate(G._in_degree)
    top_in_degree = sorted(in_degree, key=lambda x: x[1], reverse=True)[:100000]
    # print(top_in_degree)
    top_indices = [x[0] for x in top_in_degree]
    top_articles = [G.labels.find_article_id_from_index(x) for x in top_indices]
    article_to_remove = set(top_articles)# - {US_ARTICLE_ID}
    indices_to_remove = [G.labels.find_index_from_article_id(x) for x in article_to_remove]
    G = G.remove_indices(indices_to_remove)
    G = G.get_largest_component()
    n1 = G.adjacency.shape[0]
    print(n1)
    print(n1 / n0)
    print(sparse.estimate_diameter(G, 1))