from load_wiki import load_wikipedia
from helpers import REPORT_PATH
import sparse

DEGREE_REPORT = REPORT_PATH.joinpath("degree_centrality.parquet")

if __name__ == "__main__":
    G = load_wikipedia()
    G = G.get_largest_component()
    G.compute_degree()
    df = G.labels._internal_df
    df["in_degree"] = G._in_degree
    df["out_degree"] = G._out_degree
    df.to_parquet(DEGREE_REPORT)

