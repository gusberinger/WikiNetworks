from load_wiki import load_wikipedia
from helpers import REPORT_PATH
import sparse

DEGREE_REPORT = REPORT_PATH.joinpath("degree_centrality.parquet")

if __name__ == "__main__":
    G = load_wikipedia()
    G = G.get_largest_component()
    scores = sparse.katz_centrality(G, alpha=.1, max_iter=5)
    df = G.labels._internal_df
    df["katz_centrality"] = scores
    df.to_parquet(DEGREE_REPORT)
