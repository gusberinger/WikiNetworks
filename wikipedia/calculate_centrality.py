import sparse
from load_wiki import load_wikipedia
import logging
from helpers import REPORT_PATH

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    log = logging.Logger(__file__)
    G = load_wikipedia()
    log.info("Loaded wikipedia graph.")
    print("assigned graph")
    scores = sparse.katz_centrality(G)
    print("calculated")
    log.info("calculated")
    report = G.labels._internal_df
    report['katz'] = scores
    report.to_parquet(REPORT_PATH)
