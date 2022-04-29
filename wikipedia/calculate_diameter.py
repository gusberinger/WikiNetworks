from load_wiki import load_wikipedia
from helpers import REPORT_PATH
import sparse

CENTRALITY_REPORT = REPORT_PATH.joinpath("centrality.parquet.new")

if __name__ == "__main__":
    G = load_wikipedia()
    G = G.get_largest_component()
    diameter = sparse.estimate_diameter(G, 4)
    print(diameter)

