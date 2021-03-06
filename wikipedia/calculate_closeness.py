from load_wiki import load_wikipedia
from helpers import REPORT_PATH
import sparse

CENTRALITY_REPORT = REPORT_PATH.joinpath("closeness_centrality.parquet")

if __name__ == "__main__":
    G = load_wikipedia()
    G = G.get_largest_component()
    scores = sparse.closeness_centrality(60, G)
    df = G.labels._internal_df
    df["closeness"] = scores
    df.to_parquet(CENTRALITY_REPORT)