from load_wiki import load_wikipedia
from helpers import REPORT_PATH
import sparse

CENTRALITY_REPORT = REPORT_PATH.joinpath("centrality.parquet.new")

if __name__ == "__main__":
    G = load_wikipedia()
    G = G.get_largest_component()
    scores = sparse.closeness_centrality(15, G)
    df = G.labels._internal_df
    df["closness"] = scores
    df.to_parquet(CENTRALITY_REPORT)